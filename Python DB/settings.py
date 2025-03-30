class Settings:
    """
    설정 기능을 관리하는 클래스
    
    주요 기능:
    1. 회원 정보 수정
    2. 비밀번호 변경
    3. 계정 삭제
    """
    
    def __init__(self, conn, user_info):
        """
        Settings 클래스 초기화
        
        Args:
            conn: 데이터베이스 연결 객체
            user_info (dict): 사용자 정보
        """
        self.conn = conn
        self.cursor = conn.cursor()
        self.user_info = user_info

    def show_settings_menu(self):
        """
        설정 메뉴를 표시하고 사용자 선택을 처리합니다.
        """
        while True:
            print("\n=== 설정 ===")
            print("1. 회원 정보 수정")
            print("2. 비밀번호 변경")
            print("3. 계정 삭제")
            print("4. 돌아가기")
            
            choice = input("\n원하는 작업을 선택하세요 (1-4): ")
            
            if choice == "1":
                self.edit_profile()
            elif choice == "2":
                self.change_password()
            elif choice == "3":
                self.delete_account()
            elif choice == "4":
                break
            else:
                print("잘못된 선택입니다. 다시 선택해주세요.")

    def edit_profile(self):
        """
        회원 정보를 수정합니다.
        """
        print("\n=== 회원 정보 수정 ===")
        # TODO: 회원 정보 수정 구현

    def change_password(self):
        """
        비밀번호를 변경합니다.
        """
        print("\n=== 비밀번호 변경 ===")
        # TODO: 비밀번호 변경 구현

    def delete_account(self):
        """
        계정을 삭제합니다.
        """
        print("\n=== 계정 삭제 ===")
        # TODO: 계정 삭제 구현 