from typing import Dict, Optional, Tuple
from .base_db import BaseDatabase
import sqlite3

class UserDB(BaseDatabase):
    def __init__(self, db_path: str = 'toeic_vocabulary.db'):
        super().__init__(db_path)

    # User 테이블 생성 및 초기화
    def initialize_tables(self):
        self.execute("PRAGMA foreign_keys = OFF")
        self.execute("""
        CREATE TABLE IF NOT EXISTS User (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_login_id TEXT UNIQUE NOT NULL,
            user_pw TEXT NOT NULL,
            user_name TEXT NOT NULL,
            is_admin BOOLEAN DEFAULT 0,
            user_api TEXT
        )
        """)
        self.execute("PRAGMA foreign_keys = ON")
        self.commit()

    # 회원가입: 새로운 사용자 등록, user_id 반환
    def register_user(self, user_login_id, user_pw, user_name, is_admin=0, user_api=None):
        self.execute(
            "INSERT INTO User (user_login_id, user_pw, user_name, is_admin, user_api) VALUES (?, ?, ?, ?, ?)",
            (user_login_id, user_pw, user_name, is_admin, user_api)
        )
        self.commit()
        return self.cursor.lastrowid

    # 로그인: user_login_id, user_pw로 사용자 정보 반환
    def login_user(self, user_login_id, user_pw):
        return self.fetch_one(
            "SELECT * FROM User WHERE user_login_id = ? AND user_pw = ?",
            (user_login_id, user_pw)
        )

    # 사용자 정보(이름 등) 수정
    def update_user_info(self, user_id, **kwargs):
        fields = ', '.join([f"{k}=?" for k in kwargs])
        values = list(kwargs.values())
        values.append(user_id)
        self.execute(f"UPDATE User SET {fields} WHERE user_id = ?", values)
        self.commit()

    # API KEY 수정
    def update_api_key(self, user_id, new_api_key):
        self.execute("UPDATE User SET user_api = ? WHERE user_id = ?", (new_api_key, user_id))
        self.commit()

    # user_id로 사용자 정보 조회
    def get_user(self, user_id):
        return self.fetch_one("SELECT * FROM User WHERE user_id = ?", (user_id,))

    # user_id로 사용자 정보(일부 필드) 조회
    def get_user_info(self, user_id: int) -> Optional[Dict]:
        try:
            return self.fetch_one("""
                SELECT user_id, username, name, created_at
                FROM User
                WHERE user_id = ?
            """, (user_id,))
        except Exception as e:
            print(f"사용자 정보 조회 오류: {e}")
            return None

    # 사용자 이름 수정 (성공시 True)
    def update_user_info(self, user_id: int, name: str) -> bool:
        try:
            self.execute("""
                UPDATE User
                SET name = ?
                WHERE user_id = ?
            """, (name, user_id))
            self.commit()
            return True
        except Exception as e:
            print(f"사용자 정보 수정 오류: {e}")
            self.rollback()
            return False

    # 비밀번호 변경 (성공시 True)
    def change_password(self, user_id: int, old_password: str, new_password: str) -> bool:
        try:
            user = self.fetch_one("""
                SELECT user_id
                FROM User
                WHERE user_id = ? AND password = ?
            """, (user_id, old_password))
            if not user:
                print("현재 비밀번호가 일치하지 않습니다.")
                return False
            self.execute("""
                UPDATE User
                SET password = ?
                WHERE user_id = ?
            """, (new_password, user_id))
            self.commit()
            return True
        except Exception as e:
            print(f"비밀번호 변경 오류: {e}")
            self.rollback()
            return False

user_db = UserDB() 