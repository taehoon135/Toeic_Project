class Quiz:
    """
    퀴즈 기능을 관리하는 클래스
    
    주요 기능:
    1. 퀴즈 시작
    2. 퀴즈 결과 확인
    3. 오답 노트
    4. 퀴즈 통계
    """
    
    def __init__(self, conn, user_info):
        """
        Quiz 클래스 초기화
        
        Args:
            conn: 데이터베이스 연결 객체
            user_info (dict): 사용자 정보
        """
        self.conn = conn
        self.cursor = conn.cursor()
        self.user_info = user_info

    def show_quiz_menu(self):
        """
        퀴즈 메뉴를 표시하고 사용자 선택을 처리합니다.
        """
        while True:
            print("\n=== 퀴즈 ===")
            print("1. 퀴즈 시작")
            print("2. 퀴즈 결과 확인")
            print("3. 오답 노트")
            print("4. 퀴즈 통계")
            print("5. 돌아가기")
            
            choice = input("\n원하는 작업을 선택하세요 (1-5): ")
            
            if choice == "1":
                self.start_quiz()
            elif choice == "2":
                self.show_quiz_results()
            elif choice == "3":
                self.show_wrong_answers()
            elif choice == "4":
                self.show_quiz_stats()
            elif choice == "5":
                break
            else:
                print("잘못된 선택입니다. 다시 선택해주세요.")

    def start_quiz(self):
        """
        퀴즈를 시작합니다.
        """
        print("\n=== 퀴즈 시작 ===")
        # TODO: 퀴즈 시작 구현

    def show_quiz_results(self):
        """
        퀴즈 결과를 확인합니다.
        """
        print("\n=== 퀴즈 결과 ===")
        # TODO: 퀴즈 결과 표시 구현

    def show_wrong_answers(self):
        """
        오답 노트를 확인합니다.
        """
        print("\n=== 오답 노트 ===")
        # TODO: 오답 노트 표시 구현

    def show_quiz_stats(self):
        """
        퀴즈 통계를 확인합니다.
        """
        print("\n=== 퀴즈 통계 ===")
        # TODO: 퀴즈 통계 표시 구현 