import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.user_db import user_db
from database.word_db import word_db
from database.category_db import category_db
from database.quiz_db import quiz_db

def initialize_database():
    print("데이터베이스 초기화 시작...")
    
    # 외래키 제약 조건 비활성화
    user_db.disable_foreign_keys()
    
    try:
        # 테이블 초기화 (순서 중요)
        user_db.initialize_tables()
        category_db.initialize_tables()
        word_db.initialize_tables()
        quiz_db.initialize_tables()
        
        print("테이블 생성 완료!")
        
    finally:
        # 외래키 제약 조건 활성화
        user_db.enable_foreign_keys()
    
    print("데이터베이스 초기화 완료!")

if __name__ == "__main__":
    initialize_database() 