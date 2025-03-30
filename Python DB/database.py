import sqlite3

def init_database():
    """
    데이터베이스를 초기화하고 필요한 테이블을 생성합니다.
    """
    conn = sqlite3.connect("toeic_vocab.db")
    cursor = conn.cursor()
    
    # User 테이블 생성
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS User (
        user_id TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        username TEXT NOT NULL,
        is_admin BOOLEAN NOT NULL DEFAULT 0
    )
    """)
    
    # Word 테이블 생성
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Word (
        word_id INTEGER PRIMARY KEY AUTOINCREMENT,
        english TEXT NOT NULL,
        korean TEXT NOT NULL,
        category TEXT,
        example_sentence TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Quiz 테이블 생성
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Quiz (
        quiz_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        word_id INTEGER NOT NULL,
        is_correct BOOLEAN NOT NULL,
        quiz_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES User(user_id),
        FOREIGN KEY (word_id) REFERENCES Word(word_id)
    )
    """)
    
    # 기본 관리자 계정 생성
    cursor.execute("""
    INSERT OR IGNORE INTO User (user_id, password, username, is_admin)
    VALUES ('admin', 'admin123', '관리자', 1)
    """)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_database()
    print("데이터베이스 초기화가 완료되었습니다.") 