from typing import Dict, List, Optional, Tuple
from .base_db import BaseDatabase
import csv
# import os # os 모듈이 직접 사용되지 않으면 삭제 가능
# import sqlite3 # sqlite3 모듈이 직접 사용되지 않으면 삭제 가능
# from .category_db import CategoryDB # CategoryDB 임포트 (순환참조 주의하며 실제 경로로)
# 위 임포트가 순환 참조를 일으키면, category_db: 'CategoryDB' 타입 힌트 사용

# word_db.py 상단에 추가 (실제 CategoryDB 위치에 따라 경로 조정 필요)
# from ..category_db import CategoryDB # 만약 category_db가 database 폴더 밖에 있다면
# 여기서는 같은 폴더라 가정하고 from .category_db import CategoryDB

# 클래스 정의 전에 임포트하는 것이 일반적
# 이 예제에서는 CategoryDB가 같은 디렉토리에 있다고 가정합니다.
# 실제 프로젝트 구조에 따라 from src.database.category_db import CategoryDB 등이 될 수 있습니다.
# 순환 참조를 피하기 위해, 함수 시그니처에서 'CategoryDB' 문자열 힌트를 사용하는 것이 더 안전할 수 있습니다.
# 여기서는 직접 임포트를 시도합니다.

# from .category_db import CategoryDB # CategoryDB 임포트 (순환참조 주의하며 실제 경로로)

class WordDB(BaseDatabase):
    def __init__(self, db_path: str = 'toeic_vocabulary.db'):
        super().__init__(db_path)

    # CSV 파일에서 단어 데이터 임포트 (카테고리 연결 로직 추가)
    def import_from_csv(self, csv_path: str, user_id: int, category_db_instance: 'CategoryDB') -> bool:
        """CSV 파일에서 단어를 가져와 Word 테이블에 추가하고, 명시된 경우 카테고리에 연결합니다.

        Args:
            csv_path: CSV 파일 경로.
            user_id: 단어와 카테고리를 연결할 사용자의 ID.
            category_db_instance: CategoryDB의 인스턴스.

        Returns:
            성공 여부.
        """
        # category_db_instance의 실제 타입을 사용하기 위해 임포트 필요.
        # 만약 임포트가 어렵다면, 이 함수 내에서 category_db_instance.메서드() 호출 시
        # 덕 타이핑에 의존하게 됨.
        # from .category_db import CategoryDB # 함수 내 지역 임포트 (권장하지 않음)
        
        processed_rows = 0
        added_words = 0
        linked_to_category = 0

        try:
            with open(csv_path, 'r', encoding='utf-8-sig') as file: # utf-8-sig for BOM
                reader = csv.DictReader(file)
                if not reader.fieldnames:
                    print(f"Error: CSV file {csv_path} is empty or has no header.")
                    return False
                
                # 필수 컬럼 확인 (예시)
                required_cols = ['english', 'meaning']
                for col in required_cols:
                    if col not in reader.fieldnames:
                        print(f"Error: CSV file missing required column '{col}'.")
                        return False

                for row in reader:
                    processed_rows += 1
                    english = row.get('english', '').strip()
                    meaning = row.get('meaning', '').strip()
                    
                    if not english or not meaning:
                        print(f"Skipping row due to empty english or meaning: {row}")
                        continue

                    part_of_speech = row.get('part_of_speech', '').strip()
                    example_sentence = row.get('example_sentence', '').strip()
                    category_name_from_csv = row.get('category', '').strip()

                    word_id = self.add_word(english, meaning, part_of_speech, example_sentence)

                    if word_id:
                        added_words +=1 # add_word가 기존 ID 반환 시에도 카운트 (단어가 DB에 존재 또는 추가됨)
                        if category_name_from_csv:
                            category_id = category_db_instance.get_or_create_category(user_id, category_name_from_csv)
                            if category_id:
                                if category_db_instance.add_word_to_category(category_id, word_id):
                                    linked_to_category +=1
                                else:
                                    print(f"Failed to link word ID {word_id} to category ID {category_id}.")
                            else:
                                print(f"Could not get or create category '{category_name_from_csv}' for user {user_id}. Word '{english}' not linked.")
                    else:
                        print(f"Failed to add or get word '{english}'.")
            
            print(f"CSV Import Summary: Processed {processed_rows} rows. Words in DB/added: {added_words}. Linked to category: {linked_to_category}.")
            return True
        except FileNotFoundError:
            print(f"Error: CSV file not found at {csv_path}")
            return False
        except Exception as e:
            print(f"Error during CSV import from {csv_path}: {e}")
            # self.rollback() # 개별 DB 메서드가 롤백 처리 가정
            return False

    # _get_or_create_category, add_category, get_categories, delete_category 메서드 삭제됨

    # 전체 단어 목록 조회 (카테고리 정보는 WordCategory, Category 테이블을 JOIN하여 가져옴)
    def get_all_words(self) -> List[Dict]:
        try:
            return self.fetch_all("""
                SELECT 
                    w.word_id as id,
                    w.english,
                    w.meaning,
                    w.part_of_speech,
                    w.example_sentence as example,
                    w.wrong_count,
                    w.created_at,
                    (SELECT GROUP_CONCAT(cat.name) FROM Category cat JOIN WordCategory wc_join ON cat.category_id = wc_join.category_id WHERE wc_join.word_id = w.word_id) as categories
                FROM Word w
                GROUP BY w.word_id
                ORDER BY w.word_id
            """)
        except Exception as e:
            print(f"Error in get_all_words: {e}")
            return []

    # 특정 카테고리의 단어 목록 조회는 category_db.get_words_in_category(category_id, user_id) 사용 권장
    # get_words 메서드는 삭제하거나, 모든 단어를 반환하는 get_all_words의 별칭으로 남길 수 있음.
    # 여기서는 get_words(category_id=None)이 get_all_words()를 호출하도록 유지
    def get_words(self, category_id: Optional[int] = None) -> List[Dict]:
        if category_id is not None:
            # 이 부분은 category_db.py의 기능을 사용하도록 유도.
            # word_db.py가 category_id만으로 user를 특정할 수 없으므로,
            # user_id가 필요한 category_db.py의 함수를 호출하는 것이 맞음.
            # 여기서는 일단 빈 리스트를 반환하거나, 예외를 발생시킬 수 있음.
            # 또는, 이 기능을 사용하지 않도록 API에서 제거하는 것이 좋음.
            # 기존 코드 호환성을 위해 일단 남겨두나, 실제 사용 시 주의 필요.
            # 이전에 JOIN으로 가져왔지만, Category가 user_id를 가지므로 user 컨텍스트 없이 여기서 직접 가져오는 것은 부적절.
            print("Warning: get_words with category_id is deprecated in WordDB. Use CategoryDB.get_words_in_category.")
            # 임시로 모든 단어 반환 또는 빈 리스트 반환
            # return self.get_all_words() # 또는
            return [] 
        else:
            return self.get_all_words()


    # 단어 상세 정보 조회 (카테고리 정보 JOIN)
    def get_word_details(self, word_id: int) -> Optional[Dict]:
        try:
            return self.fetch_one("""
                SELECT 
                    w.word_id as id,
                    w.english,
                    w.meaning,
                    w.part_of_speech,
                    w.example_sentence as example,
                    w.wrong_count,
                    w.created_at,
                    (SELECT GROUP_CONCAT(cat.name) FROM Category cat JOIN WordCategory wc_join ON cat.category_id = wc_join.category_id WHERE wc_join.word_id = w.word_id) as categories
                FROM Word w
                WHERE w.word_id = ?
                GROUP BY w.word_id
            """, (word_id,))
        except Exception as e:
            print(f"Error in get_word_details: {e}")
            return None

    # 오답 횟수 1 증가 (변경 없음)
    def update_wrong_count(self, word_id: int) -> bool:
        try:
            self.execute("""
                UPDATE Word
                SET wrong_count = wrong_count + 1
                WHERE word_id = ?
            """, (word_id,))
            self.commit()
            return True
        except Exception as e:
            self.rollback()
            return False

    # 단어 추가 (카테고리 연결 로직 제거)
    def add_word(self, word: str, meaning: str, part_of_speech: str, example: str) -> Optional[int]: # 반환 타입 Optional[int]로 변경, category_id 인자 이미 삭제됨
        try:
            # 먼저 동일한 영어 단어가 있는지 확인 (기존 로직은 영어 단어 기준)
            existing_word = self.fetch_one(
                "SELECT word_id FROM Word WHERE english = ?",
                (word,)
            )
            if existing_word:
                # print(f"Word '{word}' already exists with ID {existing_word['word_id']}. Returning existing ID.") # 이전 메시지에서 로그 추가 제안했었음
                return existing_word['word_id'] # 중복 시 기존 ID 반환

            # 새 단어 추가
            self.execute(
                """
                INSERT INTO Word (english, meaning, part_of_speech, example_sentence)
                VALUES (?, ?, ?, ?)
                """,
                (word, meaning, part_of_speech, example)
            )
            self.commit() # 단어 추가 후 커밋
            new_word_id = self.cursor.lastrowid
            
            if new_word_id is None or new_word_id == 0: # SQLite에서 lastrowid가 0을 반환하는 경우도 고려
                # 이 경우는 INSERT가 실패했거나 ID를 가져올 수 없는 경우
                print(f"Failed to get lastrowid after inserting word '{word}'. Rolling back.")
                self.rollback() # 혹시 모를 변경사항 롤백
                return None
            
            return new_word_id
        except Exception as e:
            self.rollback()
            print(f"Error in add_word for '{word}': {e}")
            return None # 에러 발생 시 None 반환

    # add_word_to_category, remove_word_from_category 메서드 삭제됨

    # Word, WordHistory 테이블 생성 및 초기화 (Category, WordCategory DDL 삭제)
    def initialize_tables(self):
        # self.execute("DROP TABLE IF EXISTS WordHistory") # 주석 처리된 상태 유지
        # self.execute("DROP TABLE IF EXISTS WordCategory")# 주석 처리된 상태 유지
        # self.execute("DROP TABLE IF EXISTS Word") # 주석 처리된 상태 유지
        # self.execute("DROP TABLE IF EXISTS Category")# 주석 처리된 상태 유지
        
        # Category 테이블 DDL 삭제
        # WordCategory 테이블 DDL 삭제
        
        self.execute("""
        CREATE TABLE IF NOT EXISTS Word (
            word_id INTEGER PRIMARY KEY AUTOINCREMENT,
            english TEXT NOT NULL, 
            meaning TEXT NOT NULL,
            part_of_speech TEXT,
            example_sentence TEXT,
            wrong_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            -- UNIQUE(english) 제약 조건 추가 고려
        )
        """)
        
        self.execute("""
        CREATE TABLE IF NOT EXISTS WordHistory (
            history_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            word_id INTEGER NOT NULL,
            is_correct INTEGER NOT NULL,
            study_type TEXT NOT NULL,
            studied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
            FOREIGN KEY (word_id) REFERENCES Word(word_id) ON DELETE CASCADE
        )
        """)
        self.commit()

    # 단어장 전체 리스트(영어, 해석, 품사) (변경 없음)
    def get_word_list(self):
        return self.fetch_all("SELECT word_id, english, meaning, part_of_speech FROM Word")

    # 단어 상세정보(예문, 발음) (변경 없음)
    def get_word_detail(self, word_id): # 이 메서드는 get_word_details와 유사. 하나로 통일하거나 역할 분담.
        return self.fetch_one("SELECT example_sentence, pronunciation FROM Word WHERE word_id = ?", (word_id,))

    # 단어 검색 (영어/한글) (카테고리 JOIN 유지)
    def search_words(self, keyword: str) -> List[Dict]:
        keyword_param = f"{keyword}%"
        try:
            return self.fetch_all(
                """
                SELECT 
                    w.*, 
                    (SELECT GROUP_CONCAT(cat.name) FROM Category cat JOIN WordCategory wc_join ON cat.category_id = wc_join.category_id WHERE wc_join.word_id = w.word_id) as categories
                FROM Word w
                WHERE w.english LIKE ? OR w.meaning LIKE ?
                GROUP BY w.word_id
                ORDER BY w.english
                """,
                (keyword_param, keyword_param)
            )
        except Exception as e:
            print(f"Error in search_words: {e}")
            return []
            
    # 단어 조회 (word_id) (카테고리 JOIN 유지)
    def get_word(self, word_id: int) -> Optional[Dict]: # 반환 타입 Optional[Dict]로 명시
        try:
            return self.fetch_one(
                """
                SELECT 
                    w.*, 
                    (SELECT GROUP_CONCAT(cat.name) FROM Category cat JOIN WordCategory wc_join ON cat.category_id = wc_join.category_id WHERE wc_join.word_id = w.word_id) as categories
                FROM Word w
                WHERE w.word_id = ?
                GROUP BY w.word_id
                """,
                (word_id,)
            )
        except Exception as e:
            print(f"Error in get_word: {e}")
            return None

    # get_words_by_category 메서드 삭제 (category_db.py의 기능 사용)

    # 단어 정보 수정 (카테고리 연결 로직 제거)
    def update_word(self, word_id: int, word: str, meaning: str, part_of_speech: str, example: str) -> bool: # category_id 인자 삭제
        try:
            # Word 테이블 업데이트
            self.execute(
                """
                UPDATE Word
                SET english = ?, meaning = ?, part_of_speech = ?, example_sentence = ?
                WHERE word_id = ?
                """,
                (word, meaning, part_of_speech, example, word_id)
            )
            self.commit()
            return self.cursor.rowcount > 0 # 실제로 업데이트 되었는지 확인
        except Exception as e:
            self.rollback()
            print(f"Error in update_word: {e}")
            return False

    # 단어 삭제 (변경 없음, ON DELETE CASCADE로 WordCategory 등에서 자동 처리 기대)
    def delete_word(self, word_id: int) -> bool:
        try:
            self.execute(
                "DELETE FROM Word WHERE word_id = ?",
                (word_id,)
            )
            self.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            self.rollback()
            print(f"Error in delete_word: {e}")
            return False

    # 오답 횟수 기준 단어 목록 조회 (카테고리 JOIN 유지)
    def get_words_by_wrong_count(self, min_wrong_count: int = 1) -> List[Dict]:
        try:
            return self.fetch_all(
                """
                SELECT 
                    w.*, 
                    (SELECT GROUP_CONCAT(cat.name) FROM Category cat JOIN WordCategory wc_join ON cat.category_id = wc_join.category_id WHERE wc_join.word_id = w.word_id) as categories
                FROM Word w
                WHERE w.wrong_count >= ?
                GROUP BY w.word_id
                ORDER BY w.wrong_count DESC
                """,
                (min_wrong_count,)
            )
        except Exception as e:
            print(f"Error in get_words_by_wrong_count: {e}")
            return []

# word_db = WordDB() # 모듈 레벨에서 인스턴스 생성하지 않도록 변경 (main.py 등에서 관리) 
