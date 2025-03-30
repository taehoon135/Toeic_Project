import sqlite3
import hashlib
from menu import Menu

class UserAuth:
    """
    사용자 인증을 관리하는 클래스
    
    주요 기능:
    1. 회원가입: 새로운 사용자 등록
    2. 로그인: 사용자 인증
    3. ID 중복 확인: 회원가입 시 ID 중복 검사
    
    데이터베이스 테이블:
    - User: 사용자 정보 저장
    """
    
    def __init__(self):
        """
        UserAuth 클래스 초기화
        데이터베이스 연결을 설정합니다.
        """
        self.conn = sqlite3.connect("toeic_vocab.db")
        self.cursor = self.conn.cursor()

    def __del__(self):
        """
        객체가 소멸될 때 데이터베이스 연결을 종료합니다.
        """
        self.conn.close()

    def check_id_exists(self, user_id):
        """
        ID 중복을 확인합니다.
        
        Args:
            user_id (str): 확인할 사용자 ID
            
        Returns:
            bool: ID가 이미 존재하면 True, 아니면 False
        """
        self.cursor.execute("SELECT user_id FROM User WHERE user_id = ?", (user_id,))
        return self.cursor.fetchone() is not None

    def register_user(self, user_id, password, username, is_admin):
        """
        새로운 사용자를 등록합니다.
        
        Args:
            user_id (str): 사용자 ID
            password (str): 비밀번호
            username (str): 사용자 이름
            is_admin (bool): 관리자 여부
            
        Returns:
            tuple: (성공 여부, 메시지)
            - 성공: (True, "회원가입이 완료되었습니다.")
            - 실패: (False, 에러 메시지)
        """
        try:
            # ID 중복 검사
            if self.check_id_exists(user_id):
                return False, "이미 존재하는 ID입니다."
            
            # 사용자 등록
            self.cursor.execute(
                "INSERT INTO User (user_id, password, username, is_admin) VALUES (?, ?, ?, ?)",
                (user_id, password, username, is_admin)
            )
            self.conn.commit()
            return True, "회원가입이 완료되었습니다."
            
        except sqlite3.Error as e:
            return False, f"데이터베이스 오류: {str(e)}"

    def login(self, user_id, password):
        """
        사용자 로그인을 처리합니다.
        
        Args:
            user_id (str): 사용자 ID
            password (str): 비밀번호
            
        Returns:
            tuple: (성공 여부, 메시지, 사용자 정보)
            - 성공: (True, "로그인 성공", 사용자 정보 딕셔너리)
            - 실패: (False, 에러 메시지, None)
            
        사용자 정보 딕셔너리:
        {
            "user_id": 사용자 ID,
            "username": 사용자 이름,
            "is_admin": 관리자 여부
        }
        """
        try:
            # 사용자 정보 조회
            self.cursor.execute(
                "SELECT user_id, username, is_admin FROM User WHERE user_id = ? AND password = ?",
                (user_id, password)
            )
            user = self.cursor.fetchone()
            
            if user:
                return True, "로그인 성공", {
                    "user_id": user[0],
                    "username": user[1],
                    "is_admin": user[2]
                }
            else:
                return False, "ID 또는 비밀번호가 일치하지 않습니다.", None
                
        except sqlite3.Error as e:
            return False, f"데이터베이스 오류: {str(e)}", None

def main():
    """
    메인 프로그램 실행 함수
    
    기능:
    1. 회원가입
       - 계정 유형 선택 (관리자/일반 사용자)
       - ID 입력 및 중복 확인
       - 비밀번호 입력
       - 이름 입력
    2. 로그인
       - ID와 비밀번호로 로그인
       - 로그인 성공 시 메인 메뉴로 이동
    3. 프로그램 종료
    """
    auth = UserAuth()
    
    while True:
        print("\n=== TOEIC 단어장 시스템 ===")
        print("1. 회원가입")
        print("2. 로그인")
        print("3. 종료")
        
        choice = input("\n원하는 작업을 선택하세요 (1-3): ")
        
        if choice == "1":
            print("\n=== 회원가입 ===")
            
            # 계정 유형 선택
            while True:
                account_type = input("계정 유형을 선택하세요 (1: 관리자, 2: 일반 사용자): ")
                if account_type in ['1', '2']:
                    is_admin = (account_type == '1')
                    break
                print("잘못된 선택입니다. 다시 선택해주세요.")
            
            # ID 입력 및 중복 확인
            while True:
                user_id = input("ID를 입력하세요: ")
                if auth.check_id_exists(user_id):
                    print("이미 존재하는 ID입니다. 다른 ID를 입력해주세요.")
                    continue
                print("사용 가능한 ID입니다!")
                break
            
            password = input("비밀번호를 입력하세요: ")
            username = input("이름을 입력하세요: ")
            
            success, message = auth.register_user(user_id, password, username, is_admin)
            print(f"결과: {message}")
            
        elif choice == "2":
            print("\n=== 로그인 ===")
            user_id = input("ID를 입력하세요: ")
            password = input("비밀번호를 입력하세요: ")
            
            success, message, user_info = auth.login(user_id, password)
            print(f"결과: {message}")
            if user_info:
                account_type = "관리자" if user_info['is_admin'] else "일반 사용자"
                print(f"사용자 정보: [계정유형: {account_type}] ID: {user_info['user_id']}, 이름: {user_info['username']}")
                
                # 로그인 성공 시 메인 메뉴로 이동
                menu = Menu(user_info)
                menu.show_menu()
                
        elif choice == "3":
            print("프로그램을 종료합니다.")
            break
            
        else:
            print("잘못된 선택입니다. 다시 선택해주세요.")

if __name__ == "__main__":
    main() 