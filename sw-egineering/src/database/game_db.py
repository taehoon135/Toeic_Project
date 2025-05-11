from typing import Dict, List, Optional, Tuple
from .base_db import BaseDatabase

class GameDB(BaseDatabase):
    # GameDB 인스턴스 초기화
    def __init__(self, db_path: str = 'toeic_vocabulary.db'):
        super().__init__(db_path)

    # 게임 점수 저장 (핵심 기능)
    def save_score(self, user_id: int, game_type: str, score: int) -> bool:
        try:
            self.execute("""
                INSERT INTO GameScore (user_id, game_type, score)
                VALUES (?, ?, ?)
            """, (user_id, game_type, score))
            self.commit()
            return True
        except Exception as e:
            self.rollback()
            return False

    # 사용자별 게임 점수 목록 조회
    def get_user_scores(self, user_id: int, game_type: Optional[str] = None) -> List[Dict]:
        try:
            if game_type:
                return self.fetch_all("""
                    SELECT score_id, game_type, score, created_at
                    FROM GameScore
                    WHERE user_id = ? AND game_type = ?
                    ORDER BY created_at DESC
                """, (user_id, game_type))
            else:
                return self.fetch_all("""
                    SELECT score_id, game_type, score, created_at
                    FROM GameScore
                    WHERE user_id = ?
                    ORDER BY created_at DESC
                """, (user_id,))
        except Exception as e:
            return []

    # 게임별 최고 점수(랭킹) 조회 (핵심 기능)
    def get_high_scores(self, game_type: str, limit: int = 10) -> List[Dict]:
        try:
            return self.fetch_all("""
                SELECT gs.user_id, u.username, gs.score, gs.created_at
                FROM GameScore gs
                JOIN User u ON gs.user_id = u.user_id
                WHERE gs.game_type = ?
                ORDER BY gs.score DESC
                LIMIT ?
            """, (game_type, limit))
        except Exception as e:
            return []

    # 사용자별 게임 통계 조회 (총 게임 수, 평균, 최고점 등)
    def get_user_statistics(self, user_id: int) -> Dict:
        try:
            total_stats = self.fetch_one("""
                SELECT 
                    COUNT(*) as total_games,
                    AVG(score) as average_score,
                    MAX(score) as highest_score
                FROM GameScore
                WHERE user_id = ?
            """, (user_id,))
            game_type_stats = self.fetch_all("""
                SELECT 
                    game_type,
                    COUNT(*) as game_count,
                    AVG(score) as average_score,
                    MAX(score) as highest_score
                FROM GameScore
                WHERE user_id = ?
                GROUP BY game_type
            """, (user_id,))
            result = {
                'total_games': total_stats['total_games'],
                'average_score': round(total_stats['average_score'], 2),
                'highest_score': total_stats['highest_score'],
                'game_types': {}
            }
            for stat in game_type_stats:
                result['game_types'][stat['game_type']] = {
                    'game_count': stat['game_count'],
                    'average_score': round(stat['average_score'], 2),
                    'highest_score': stat['highest_score']
                }
            return result
        except Exception as e:
            return {
                'total_games': 0,
                'average_score': 0.0,
                'highest_score': 0,
                'game_types': {}
            }

    # 사용자별 게임 점수 전체 삭제
    def delete_user_scores(self, user_id: int) -> bool:
        try:
            self.execute("""
                DELETE FROM GameScore
                WHERE user_id = ?
            """, (user_id,))
            self.commit()
            return True
        except Exception as e:
            self.rollback()
            return False

class GameScoreDB(BaseDatabase):
    # GameScore 테이블 생성 및 초기화
    def initialize_tables(self):
        self.execute("DROP TABLE IF EXISTS GameScore")
        self.execute("""
        CREATE TABLE IF NOT EXISTS GameScore (
            score_id INTEGER PRIMARY KEY AUTOINCREMENT,
            quiz_id INTEGER,
            user_id INTEGER,
            score INTEGER NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (quiz_id) REFERENCES quiz(quiz_id),
            FOREIGN KEY (user_id) REFERENCES User(user_id)
        )
        """)
        self.commit()

    # 퀴즈별 점수 저장
    def save_score(self, quiz_id, user_id, score):
        self.execute(
            "INSERT INTO GameScore (quiz_id, user_id, score) VALUES (?, ?, ?)",
            (quiz_id, user_id, score)
        )
        self.commit()
        return self.cursor.lastrowid

    # 사용자별 점수 목록 조회
    def get_scores_by_user(self, user_id):
        return self.fetch_all(
            "SELECT * FROM GameScore WHERE user_id = ?",
            (user_id,)
        )

    # 퀴즈별 랭킹(점수 내림차순)
    def get_ranking(self, quiz_id):
        return self.fetch_all(
            "SELECT * FROM GameScore WHERE quiz_id = ? ORDER BY score DESC",
            (quiz_id,)
        )

# GameDB 인스턴스 생성
game_db = GameDB() 