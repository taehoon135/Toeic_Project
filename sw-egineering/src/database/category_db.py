from typing import List, Dict, Optional
from .base_db import BaseDatabase

class CategoryDB(BaseDatabase):
    # 카테고리 및 카테고리-단어 관계 테이블 생성 및 초기화
    def initialize_tables(self):
        try:
            self.execute("DROP TABLE IF EXISTS Category")
            self.execute("""
            CREATE TABLE IF NOT EXISTS Category (
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES User(user_id)
            )
            """)
            self.execute("DROP TABLE IF EXISTS CategoryWord")
            self.execute("""
            CREATE TABLE IF NOT EXISTS CategoryWord (
                category_id INTEGER,
                word_id INTEGER,
                PRIMARY KEY (category_id, word_id),
                FOREIGN KEY (category_id) REFERENCES Category(category_id),
                FOREIGN KEY (word_id) REFERENCES Word(word_id)
            )
            """)
            self.commit()
            return True
        except Exception as e:
            return False

    # 카테고리 생성 (핵심 기능)
    def create_category(self, user_id: int, category_name: str) -> int:
        self.execute(
            "INSERT INTO Category (name, user_id) VALUES (?, ?)",
            (category_name, user_id)
        )
        self.commit()
        return self.cursor.lastrowid

    # 사용자별 카테고리 목록 조회
    def get_user_categories(self, user_id: int) -> List[Dict]:
        try:
            categories = self.fetch_all(
                "SELECT category_id, name FROM Category WHERE user_id = ?",
                (user_id,)
            )
            return categories
        except Exception as e:
            return []

    # 단어를 카테고리에 추가 (핵심 기능)
    def add_word_to_category(self, category_id: int, word_id: int) -> bool:
        try:
            self.execute(
                "INSERT OR IGNORE INTO CategoryWord (category_id, word_id) VALUES (?, ?)",
                (category_id, word_id)
            )
            self.commit()
            return True
        except Exception as e:
            return False
    
    # 카테고리에서 단어 제거
    def remove_word_from_category(self, category_id: int, word_id: int) -> bool:
        try:
            self.execute(
                "DELETE FROM CategoryWord WHERE category_id = ? AND word_id = ?",
                (category_id, word_id)
            )
            self.commit()
            return True
        except Exception as e:
            return False
    
    # 여러 카테고리의 단어 목록 조회
    def get_words_by_categories(self, category_ids: List[int]) -> List[Dict]:
        try:
            placeholders = ','.join(['?'] * len(category_ids))
            query = f"""
                SELECT DISTINCT w.* 
                FROM Word w
                JOIN CategoryWord wc ON w.id = wc.word_id
                WHERE wc.category_id IN ({placeholders})
            """
            return self.fetch_all(query, category_ids)
        except Exception as e:
            return []
    
    # 카테고리 삭제
    def delete_category(self, category_id: int) -> bool:
        try:
            self.execute(
                "DELETE FROM CategoryWord WHERE category_id = ?",
                (category_id,)
            )
            self.execute(
                "DELETE FROM Category WHERE category_id = ?",
                (category_id,)
            )
            self.commit()
            return True
        except Exception as e:
            return False
    
    # 단어가 속한 카테고리 목록 조회
    def get_word_categories(self, word_id: int) -> List[Dict]:
        try:
            query = """
                SELECT c.category_id, c.name
                FROM Category c
                JOIN CategoryWord wc ON c.category_id = wc.category_id
                WHERE wc.word_id = ?
            """
            return self.fetch_all(query, (word_id,))
        except Exception as e:
            return []

    # 카테고리 추가 (user_id와 함께)
    def add_category(self, name: str, created_by: int) -> bool:
        return self.execute(
            """
            INSERT INTO Category (name, user_id)
            VALUES (?, ?)
            """,
            (name, created_by)
        )

    # category_id로 카테고리 정보 조회
    def get_category(self, category_id: int) -> Dict:
        return self.fetch_one(
            "SELECT * FROM Category WHERE category_id = ?",
            (category_id,)
        )

    # 사용자별 카테고리 전체 조회
    def get_categories_by_user(self, user_id: int) -> List[Dict]:
        return self.fetch_all(
            "SELECT * FROM Category WHERE user_id = ?",
            (user_id,)
        )

    # 전체 카테고리 목록 조회 (단어 수 포함)
    def get_all_categories(self) -> List[Dict]:
        return self.fetch_all(
            """
            SELECT c.*, u.username as creator_name, COUNT(w.word_id) as word_count
            FROM Category c
            JOIN User u ON c.user_id = u.user_id
            LEFT JOIN CategoryWord w ON c.category_id = w.category_id
            GROUP BY c.category_id
            ORDER BY c.name
            """
        )

    # 카테고리명 수정
    def update_category(self, category_id: int, category_name: str) -> bool:
        self.execute(
            "UPDATE Category SET name = ? WHERE category_id = ?",
            (category_name, category_id)
        )
        self.commit()
        return True

    # 카테고리에 속한 단어 목록 조회
    def get_words_in_category(self, category_id: int) -> List[Dict]:
        return self.fetch_all(
            "SELECT w.word_id, w.english, w.korean, w.part_of_speech FROM Word w JOIN CategoryWord cw ON w.word_id = cw.word_id WHERE cw.category_id = ?",
            (category_id,)
        )

category_db = CategoryDB('category.db') 