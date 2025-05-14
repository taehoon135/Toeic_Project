from typing import List, Dict, Optional
from .base_db import BaseDatabase, DB_PATH

class CategoryDB(BaseDatabase):
    def __init__(self, db_path: str = DB_PATH): # 기본 DB 경로 사용
        super().__init__(db_path)

    # 카테고리 및 카테고리-단어 관계 테이블 생성 및 초기화
    def initialize_tables(self):
        try:
            # self.execute("DROP TABLE IF EXISTS Category") # 주석 처리
            self.execute("""
            CREATE TABLE IF NOT EXISTS Category (
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
                UNIQUE (user_id, name) -- 한 사용자는 같은 이름의 카테고리를 중복 생성 불가
            )
            """)
            # self.execute("DROP TABLE IF EXISTS WordCategory") # 주석 처리
            self.execute("""
            CREATE TABLE IF NOT EXISTS WordCategory (
                category_id INTEGER,
                word_id INTEGER,
                PRIMARY KEY (category_id, word_id),
                FOREIGN KEY (category_id) REFERENCES Category(category_id) ON DELETE CASCADE,
                FOREIGN KEY (word_id) REFERENCES Word(word_id) ON DELETE CASCADE
            )
            """)
            self.commit()
        except Exception as e:
            print(f"Error initializing category tables: {e}")
            self.rollback()

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
                "INSERT OR IGNORE INTO WordCategory (category_id, word_id) VALUES (?, ?)",
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
                "DELETE FROM WordCategory WHERE category_id = ? AND word_id = ?",
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
                JOIN WordCategory wc ON w.id = wc.word_id
                WHERE wc.category_id IN ({placeholders})
            """
            return self.fetch_all(query, category_ids)
        except Exception as e:
            return []
    
    # 카테고리 삭제
    def delete_category(self, category_id: int, user_id: int) -> bool: # user_id 추가하여 권한 확인
        try:
            category = self.fetch_one("SELECT user_id FROM Category WHERE category_id = ?", (category_id,))
            if not category or category['user_id'] != user_id:
                print("Error: Category not found or permission denied.")
                return False

            self.execute(
                "DELETE FROM WordCategory WHERE category_id = ?",
                (category_id,)
            )
            self.execute(
                "DELETE FROM Category WHERE category_id = ? AND user_id = ?", # user_id 조건 추가
                (category_id, user_id)
            )
            self.commit()
            return True
        except Exception as e:
            self.rollback()
            print(f"Error deleting category: {e}")
            return False
    
    # 단어가 속한 카테고리 목록 조회
    def get_word_categories(self, word_id: int) -> List[Dict]:
        try:
            query = """
                SELECT c.category_id, c.name
                FROM Category c
                JOIN WordCategory wc ON c.category_id = wc.category_id
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

    def get_or_create_category(self, user_id: int, category_name: str) -> Optional[int]:
        """지정된 사용자에 대해 카테고리가 존재하면 ID를 반환하고, 없으면 생성 후 ID를 반환."""
        if not category_name or not category_name.strip():
            print(f"Error: Category name cannot be empty for user {user_id}.")
            return None
        try:
            # 먼저 기존 카테고리가 있는지 확인
            existing_category = self.fetch_one(
                "SELECT category_id FROM Category WHERE user_id = ? AND name = ?",
                (user_id, category_name)
            )
            if existing_category:
                return existing_category['category_id']
            else:
                # INSERT OR IGNORE를 사용하여 중복 삽입 시도 방지 (UNIQUE 제약 조건 위반 방지)
                # 실제 삽입은 create_category 메서드가 담당하며, 이 메서드는 lastrowid를 반환함.
                # create_category가 UNIQUE 제약 위반을 어떻게 처리하는지 확인 필요.
                # 현재 create_category는 단순 INSERT 후 lastrowid 반환.
                # UNIQUE 제약으로 인해 INSERT가 실패하면 lastrowid가 0 또는 None일 수 있음.
                # 여기서는 INSERT OR IGNORE 후 SELECT로 ID를 가져오는 더 안전한 패턴을 사용합니다.
                
                self.execute(
                    "INSERT OR IGNORE INTO Category (user_id, name) VALUES (?, ?)",
                    (user_id, category_name)
                )
                # INSERT OR IGNORE는 실제로 행이 삽입되었는지 여부를 직접 알려주지 않음.
                # 따라서 이후 SELECT를 통해 ID를 가져옴.
                new_category_data = self.fetch_one(
                    "SELECT category_id FROM Category WHERE user_id = ? AND name = ?",
                    (user_id, category_name)
                )
                if new_category_data:
                    self.commit() # INSERT OR IGNORE 후 또는 SELECT 성공 후 커밋
                    return new_category_data['category_id']
                else:
                    # 이 경우는 INSERT OR IGNORE 후에도 해당 데이터를 찾지 못한 경우 (이론적으로 발생하기 어려움)
                    print(f"Failed to get/create category '{category_name}' for user {user_id} even after INSERT OR IGNORE.")
                    self.rollback()
                    return None
        except Exception as e:
            print(f"Exception in get_or_create_category for user {user_id}, name '{category_name}': {e}")
            self.rollback()
            return None

    # 전체 카테고리 목록 조회 (단어 수 포함)
    def get_all_categories(self) -> List[Dict]:
        return self.fetch_all(
            """
            SELECT c.*, u.username as creator_name, COUNT(w.word_id) as word_count
            FROM Category c
            JOIN User u ON c.user_id = u.user_id
            LEFT JOIN WordCategory w ON c.category_id = w.category_id
            GROUP BY c.category_id
            ORDER BY c.name
            """
        )

    # 카테고리명 수정
    def update_category(self, category_id: int, category_name: str, user_id: int) -> bool: # user_id 추가
        existing_category = self.fetch_one(
            "SELECT category_id FROM Category WHERE name = ? AND user_id = ? AND category_id != ?",
            (category_name, user_id, category_id)
        )
        if existing_category:
            print(f"Error: Category name '{category_name}' already exists for this user.")
            return False
            
        self.execute(
            "UPDATE Category SET name = ? WHERE category_id = ? AND user_id = ?", # user_id 조건 추가
            (category_name, category_id, user_id)
        )
        self.commit()
        return self.cursor.rowcount > 0

    # 카테고리에 속한 단어 목록 조회
    def get_words_in_category(self, category_id: int) -> List[Dict]:
        return self.fetch_all(
            "SELECT w.word_id, w.english, w.korean, w.part_of_speech FROM Word w JOIN WordCategory cw ON w.word_id = cw.word_id WHERE cw.category_id = ?",
            (category_id,)
        )

category_db = CategoryDB() # DB_PATH 사용하도록 변경 