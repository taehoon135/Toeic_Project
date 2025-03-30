import sqlite3
from wordbook import Wordbook
from quiz import Quiz
from settings import Settings

class Menu:
    """
    TOEIC 단어장 시스템의 메인 메뉴를 관리하는 클래스
    
    주요 기능:
    1. 단어장 관리
    2. 퀴즈
    3. 설정
    """
    
    def __init__(self, user_info):
        """
        Menu 클래스 초기화
        
        Args:
            user_info (dict): 로그인한 사용자 정보
                {
                    "user_id": 사용자 ID,
                    "username": 사용자 이름,
                    "is_admin": 관리자 여부
                }
        """
        self.user_info = user_info
        self.conn = sqlite3.connect("toeic_vocab.db")
        self.cursor = self.conn.cursor()
        
        # 각 기능 모듈 초기화
        self.wordbook = Wordbook(self.conn, self.user_info)
        self.quiz = Quiz(self.conn, self.user_info)
        self.settings = Settings(self.conn, self.user_info)

    def __del__(self):
        """
        객체가 소멸될 때 데이터베이스 연결을 종료합니다.
        """
        self.conn.close()

    def show_menu(self):
        """
        메인 메뉴를 표시하고 사용자 선택을 처리합니다.
        """
        while True:
            print("\n=== TOEIC 단어장 시스템 ===")
            print(f"환영합니다, {self.user_info['username']}님!")
            print("1. 단어장")
            print("2. 퀴즈")
            print("3. 설정")
            print("4. 로그아웃")
            
            choice = input("\n원하는 작업을 선택하세요 (1-4): ")
            
            if choice == "1":
                self.wordbook.show_wordbook_menu()
            elif choice == "2":
                self.quiz.show_quiz_menu()
            elif choice == "3":
                self.settings.show_settings_menu()
            elif choice == "4":
                print("로그아웃되었습니다.")
                break
            else:
                print("잘못된 선택입니다. 다시 선택해주세요.")

def main():
    """
    테스트용 메인 함수
    """
    # 테스트용 사용자 정보
    test_user = {
        "user_id": "test123",
        "username": "테스트",
        "is_admin": False
    }
    
    menu = Menu(test_user)
    menu.show_menu()

if __name__ == "__main__":
    main() 