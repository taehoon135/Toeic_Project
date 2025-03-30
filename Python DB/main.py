import sqlite3

def initialize_db():
    """
    TOEIC 단어장 데이터베이스를 초기화하고 필요한 테이블들을 생성하는 함수
    
    테이블 구조:
    1. User: 사용자 정보 저장
    2. Word: 단어 정보 저장
    3. Category: 사용자별 단어 카테고리
    4. Word_Category: 단어와 카테고리의 다대다 관계
    5. Game: 게임 정보
    6. User_Game_Record: 사용자의 게임 플레이 기록
    7. User_Word_Stats: 사용자별 단어 학습 통계
    """
    # SQLite 데이터베이스 연결
    # 데이터베이스 파일이 없으면 자동으로 생성됨
    conn = sqlite3.connect("toeic_vocab.db")
    cursor = conn.cursor()
    
    # User 테이블 생성
    # 사용자 정보를 저장하는 테이블
    # user_id: 사용자 고유 식별자 (기본키)
    # password: 암호화된 비밀번호 (SHA-256 해시)
    # username: 사용자 이름
    # is_admin: 관리자 여부 (기본값: 일반 사용자)
    # game_score: 게임 점수 (기본값: 0)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS User (
        user_id VARCHAR(50) PRIMARY KEY,
        password VARCHAR(255) NOT NULL,
        username VARCHAR(100) NOT NULL,
        is_admin BOOLEAN NOT NULL DEFAULT 0,
        game_score INTEGER NOT NULL DEFAULT 0
    );
    ''')
    
    # Word 테이블 생성
    # 단어 정보를 저장하는 테이블
    # word_id: 단어 고유 식별자 (자동 증가)
    # english_word: 영어 단어
    # meaning: 단어의 의미
    # part_of_speech: 품사
    # example_sentence: 예문
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Word (
        word_id INTEGER PRIMARY KEY AUTOINCREMENT,
        english_word VARCHAR(100) NOT NULL,
        meaning TEXT NOT NULL,
        part_of_speech VARCHAR(50),
        example_sentence TEXT
    );
    ''')
    
    # Category 테이블 생성
    # 사용자별 단어 카테고리를 저장하는 테이블
    # category_id: 카테고리 고유 식별자 (자동 증가)
    # user_id: 카테고리 소유자 (외래키)
    # category_name: 카테고리 이름
    # ON DELETE CASCADE: 사용자가 삭제되면 해당 사용자의 카테고리도 자동 삭제
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Category (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id VARCHAR(50) NOT NULL,
        category_name VARCHAR(100) NOT NULL,
        FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
    );
    ''')
    
    # Word_Category 테이블 생성
    # 단어와 카테고리의 다대다 관계를 저장하는 테이블
    # word_id: 단어 식별자 (외래키)
    # category_id: 카테고리 식별자 (외래키)
    # 복합 기본키: (word_id, category_id)
    # ON DELETE CASCADE: 단어나 카테고리가 삭제되면 관계도 자동 삭제
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Word_Category (
        word_id INTEGER NOT NULL,
        category_id INTEGER NOT NULL,
        PRIMARY KEY (word_id, category_id),
        FOREIGN KEY (word_id) REFERENCES Word(word_id) ON DELETE CASCADE,
        FOREIGN KEY (category_id) REFERENCES Category(category_id) ON DELETE CASCADE
    );
    ''')
    
    # Game 테이블 생성
    # 게임 정보를 저장하는 테이블
    # game_id: 게임 고유 식별자 (자동 증가)
    # game_name: 게임 이름
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Game (
        game_id INTEGER PRIMARY KEY AUTOINCREMENT,
        game_name VARCHAR(50) NOT NULL
    );
    ''')
    
    # User_Game_Record 테이블 생성
    # 사용자의 게임 플레이 기록을 저장하는 테이블
    # record_id: 기록 고유 식별자 (자동 증가)
    # user_id: 사용자 식별자 (외래키)
    # game_id: 게임 식별자 (외래키)
    # score: 획득 점수 (기본값: 0)
    # play_date: 플레이 날짜 (기본값: 현재 시간)
    # ON DELETE CASCADE: 사용자나 게임이 삭제되면 기록도 자동 삭제
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS User_Game_Record (
        record_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id VARCHAR(50) NOT NULL,
        game_id INTEGER NOT NULL,
        score INTEGER NOT NULL DEFAULT 0,
        play_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
        FOREIGN KEY (game_id) REFERENCES Game(game_id) ON DELETE CASCADE
    );
    ''')
    
    # User_Word_Stats 테이블 생성
    # 사용자별 단어 학습 통계를 저장하는 테이블
    # user_id: 사용자 식별자 (외래키)
    # word_id: 단어 식별자 (외래키)
    # wrong_count: 틀린 횟수 (기본값: 0)
    # 복합 기본키: (user_id, word_id)
    # ON DELETE CASCADE: 사용자나 단어가 삭제되면 통계도 자동 삭제
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS User_Word_Stats (
        user_id VARCHAR(50) NOT NULL,
        word_id INTEGER NOT NULL,
        wrong_count INTEGER NOT NULL DEFAULT 0,
        PRIMARY KEY (user_id, word_id),
        FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
        FOREIGN KEY (word_id) REFERENCES Word(word_id) ON DELETE CASCADE
    );
    ''')
    
    # 변경사항 저장 및 연결 종료
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == "__main__":
    initialize_db()
