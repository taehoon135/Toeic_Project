import sqlite3
import os
from typing import Optional, Dict, Any, List, Tuple
from abc import ABC, abstractmethod

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'toeic_vocabulary.db')

class BaseDatabase(ABC):
    def __init__(self, db_path: str = 'toeic_vocabulary.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.initialize_tables()

    def disable_foreign_keys(self):
        self.execute("PRAGMA foreign_keys = OFF")
        self.commit()

    def enable_foreign_keys(self):
        self.execute("PRAGMA foreign_keys = ON")
        self.commit()

    def execute(self, query: str, params: Tuple = ()) -> bool:
        try:
            self.cursor.execute(query, params)
            return True
        except Exception as e:
            return False

    def fetch_one(self, query: str, params: Tuple = ()) -> Optional[Dict]:
        try:
            self.cursor.execute(query, params)
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            return None

    def fetch_all(self, query: str, params: Tuple = ()) -> List[Dict]:
        try:
            self.cursor.execute(query, params)
            rows = self.cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            return []

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.conn.close()

    @abstractmethod
    def initialize_tables(self):
        """각 DB 클래스에서 구현해야 하는 테이블 초기화 메서드"""
        raise NotImplementedError("하위 클래스에서 이 메서드를 구현해야 합니다.")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close() 