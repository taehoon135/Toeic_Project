from typing import Dict, List, Optional, Tuple
from .base_db import BaseDatabase
import random

class QuizDB(BaseDatabase):
    # 퀴즈 및 퀴즈 문제 테이블 생성 및 초기화
    def initialize_tables(self):
        self.execute("DROP TABLE IF EXISTS quiz")
        self.execute("DROP TABLE IF EXISTS quiz_question")
        self.execute("""
        CREATE TABLE IF NOT EXISTS quiz (
            quiz_id INTEGER PRIMARY KEY AUTOINCREMENT,
            quiz_type TEXT NOT NULL,
            category_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES Category(category_id)
        )
        """)
        self.execute("""
        CREATE TABLE IF NOT EXISTS quiz_question (
            question_id INTEGER PRIMARY KEY AUTOINCREMENT,
            quiz_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            options TEXT,
            hint TEXT,
            FOREIGN KEY (quiz_id) REFERENCES quiz(quiz_id)
        )
        """)
        self.commit()

    # 퀴즈 생성 (핵심 기능)
    def create_quiz(self, quiz_type: str, category_id: Optional[int] = None) -> int:
        self.execute(
            "INSERT INTO quiz (quiz_type, category_id) VALUES (?, ?)",
            (quiz_type, category_id)
        )
        self.commit()
        return self.cursor.lastrowid

    # 퀴즈에 문제 추가 (핵심 기능)
    def add_quiz_question(self, quiz_id: int, question: str, correct_answer: str, 
                         options: Optional[str] = None, hint: Optional[str] = None) -> int:
        self.execute(
            """
            INSERT INTO quiz_question (quiz_id, question, correct_answer, options, hint)
            VALUES (?, ?, ?, ?, ?)
            """,
            (quiz_id, question, correct_answer, options, hint)
        )
        self.commit()
        return self.cursor.lastrowid

    # 퀴즈 상세 정보(문제 포함) 조회
    def get_quiz(self, quiz_id: int) -> Dict:
        quiz = self.fetch_one("SELECT * FROM quiz WHERE quiz_id = ?", (quiz_id,))
        if quiz:
            questions = self.fetch_all(
                "SELECT * FROM quiz_question WHERE quiz_id = ?",
                (quiz_id,)
            )
            quiz['questions'] = questions
        return quiz

    # 카테고리별 퀴즈 목록 조회
    def get_quizzes_by_category(self, category_id: int) -> List[Dict]:
        quizzes = self.fetch_all(
            "SELECT * FROM quiz WHERE category_id = ?",
            (category_id,)
        )
        for quiz in quizzes:
            questions = self.fetch_all(
                "SELECT * FROM quiz_question WHERE quiz_id = ?",
                (quiz['quiz_id'],)
            )
            quiz['questions'] = questions
        return quizzes

    # 퀴즈용 랜덤 단어 목록 조회
    def get_random_words_for_quiz(self, count: int = 10, category_id: Optional[int] = None) -> List[Dict]:
        if category_id:
            return self.fetch_all(
                """
                SELECT w.*, c.name as category_name
                FROM Word w
                LEFT JOIN Category c ON w.category_id = c.category_id
                WHERE w.category_id = ?
                ORDER BY RANDOM()
                LIMIT ?
                """,
                (category_id, count)
            )
        else:
            return self.fetch_all(
                """
                SELECT w.*, c.name as category_name
                FROM Word w
                LEFT JOIN Category c ON w.category_id = c.category_id
                ORDER BY RANDOM()
                LIMIT ?
                """,
                (count,)
            )

    # 난이도별 단어 목록 조회 (wrong_count 기준)
    def get_words_by_difficulty(self, difficulty_level: int, count: int = 10) -> List[Dict]:
        return self.fetch_all(
            """
            SELECT w.*, c.name as category_name
            FROM Word w
            LEFT JOIN Category c ON w.category_id = c.category_id
            WHERE w.wrong_count >= ?
            ORDER BY RANDOM()
            LIMIT ?
            """,
            (difficulty_level, count)
        )

    # 퀴즈 결과 기록 (핵심 기능)
    def record_quiz_result(self, user_id: int, word_id: int, is_correct: bool) -> bool:
        try:
            self.execute(
                """
                INSERT INTO WordHistory (
                    user_id, word_id, is_correct, study_type
                ) VALUES (?, ?, ?, 'quiz')
                """,
                (user_id, word_id, 1 if is_correct else 0)
            )
            if not is_correct:
                self.execute(
                    """
                    UPDATE Word
                    SET wrong_count = wrong_count + 1
                    WHERE word_id = ?
                    """,
                    (word_id,)
                )
            return True
        except Exception as e:
            return False

    # 사용자별 퀴즈 이력 조회
    def get_user_quiz_history(self, user_id: int, limit: int = 50) -> List[Dict]:
        return self.fetch_all(
            """
            SELECT h.*, w.word, w.meaning, w.part_of_speech
            FROM WordHistory h
            JOIN Word w ON h.word_id = w.word_id
            WHERE h.user_id = ? AND h.study_type = 'quiz'
            ORDER BY h.studied_at DESC
            LIMIT ?
            """,
            (user_id, limit)
        )

    # 사용자 취약 단어 목록 조회
    def get_user_weak_words(self, user_id: int, limit: int = 10) -> List[Dict]:
        return self.fetch_all(
            """
            SELECT w.*, 
                   COUNT(CASE WHEN h.is_correct = 0 THEN 1 END) as wrong_count,
                   COUNT(h.history_id) as total_attempts,
                   CAST(COUNT(CASE WHEN h.is_correct = 1 THEN 1 END) AS FLOAT) / 
                   COUNT(h.history_id) * 100 as accuracy_rate
            FROM Word w
            JOIN WordHistory h ON w.word_id = h.word_id
            WHERE h.user_id = ? AND h.study_type = 'quiz'
            GROUP BY w.word_id
            HAVING accuracy_rate < 70
            ORDER BY accuracy_rate ASC
            LIMIT ?
            """,
            (user_id, limit)
        )

    # 사용자 퀴즈 통계 조회
    def get_quiz_statistics(self, user_id: int) -> Dict:
        return self.fetch_one(
            """
            SELECT 
                COUNT(DISTINCT h.word_id) as total_words_studied,
                COUNT(h.history_id) as total_attempts,
                COUNT(CASE WHEN h.is_correct = 1 THEN 1 END) as correct_answers,
                CAST(COUNT(CASE WHEN h.is_correct = 1 THEN 1 END) AS FLOAT) / 
                COUNT(h.history_id) * 100 as overall_accuracy
            FROM WordHistory h
            WHERE h.user_id = ? AND h.study_type = 'quiz'
            """,
            (user_id,)
        )

quiz_db = QuizDB() 