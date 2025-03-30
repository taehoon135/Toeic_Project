import sqlite3

class Wordbook:
    """
    단어장 기능을 관리하는 클래스
    
    주요 기능:
    1. 단어 목록 보기
    2. 단어 추가
    3. 단어 수정
    4. 단어 삭제
    5. 카테고리 관리
    """
    
    def __init__(self, conn, user_info):
        """
        Wordbook 클래스 초기화
        
        Args:
            conn: 데이터베이스 연결 객체
            user_info: 사용자 정보 딕셔너리
        """
        self.conn = conn
        self.cursor = conn.cursor()
        self.user_info = user_info

    def show_word_list(self):
        """
        단어 목록을 보여줍니다.
        한 페이지당 20개의 단어를 표시하고,
        사용자가 페이지를 이동할 수 있습니다.
        """
        try:
            # 전체 단어 수 조회
            self.cursor.execute("SELECT COUNT(*) FROM Word")
            total_words = self.cursor.fetchone()[0]
            
            if not total_words:
                print("\n등록된 단어가 없습니다.")
                return
            
            # 페이지 당 단어 수
            words_per_page = 20
            total_pages = (total_words + words_per_page - 1) // words_per_page
            current_page = 1
            
            while True:
                # 현재 페이지의 단어 목록 조회
                offset = (current_page - 1) * words_per_page
                self.cursor.execute("""
                    SELECT word_id, english_word, meaning, part_of_speech, example_sentence
                    FROM Word
                    ORDER BY word_id
                    LIMIT ? OFFSET ?
                """, (words_per_page, offset))
                words = self.cursor.fetchall()
                
                print(f"\n=== 단어 목록 ({current_page}/{total_pages} 페이지) ===")
                print(f"총 {total_words}개의 단어 중 {offset+1}~{min(offset+words_per_page, total_words)}번")
                print("\n[번호] 영어 단어 | 품사 | 의미 | 예문")
                print("-" * 80)
                
                for word in words:
                    word_id, english, meaning, pos, example = word
                    print(f"[{word_id:4d}] {english:15} | {pos:10} | {meaning:20} | {example}")
                
                print("-" * 80)
                print("\n1. 이전 페이지")
                print("2. 다음 페이지")
                print("3. 돌아가기")
                
                choice = input("\n원하는 작업을 선택하세요 (1-3): ")
                
                if choice == "1" and current_page > 1:
                    current_page -= 1
                elif choice == "2" and current_page < total_pages:
                    current_page += 1
                elif choice == "3":
                    break
                else:
                    if choice == "1" and current_page == 1:
                        print("\n첫 페이지입니다!")
                    elif choice == "2" and current_page == total_pages:
                        print("\n마지막 페이지입니다!")
                    else:
                        print("\n잘못된 선택입니다. 다시 선택해주세요.")
            
        except sqlite3.Error as e:
            print(f"데이터베이스 오류: {str(e)}")

    def add_word(self):
        """
        새로운 단어를 추가합니다.
        """
        print("\n=== 단어 추가 ===")
        english = input("영어 단어를 입력하세요: ")
        meaning = input("의미를 입력하세요: ")
        pos = input("품사를 입력하세요 (예: n. 명사): ")
        example = input("예문을 입력하세요: ")
        
        """
        SQL insert 문을 실행하여 새로운 단어를 데이터베이스에 추가가
        """

        try:
            self.cursor.execute("""
                INSERT INTO Word (english_word, meaning, part_of_speech, example_sentence)
                VALUES (?, ?, ?, ?)
            """, (english, meaning, pos, example))
            self.conn.commit()
            print("단어가 추가되었습니다.")
        except sqlite3.Error as e:
            print(f"데이터베이스 오류: {str(e)}")

    def edit_word(self):
        """
        단어 정보를 수정합니다.
        영어 단어를 입력받아 해당 단어를 수정합니다.
        """
        print("\n=== 단어 수정 ===")
        english = input("수정할 영어 단어를 입력하세요: ")
        
        try:
            # 단어 존재 여부 확인
            self.cursor.execute("SELECT * FROM Word WHERE english_word = ?", (english,))
            word = self.cursor.fetchone()
            if not word:
                print("해당 단어가 없습니다.")
                return
            
            # 현재 단어 정보 표시
            print(f"\n현재 단어 정보:")
            print(f"영어: {word[1]}")
            print(f"의미: {word[2]}")
            print(f"품사: {word[3]}")
            print(f"예문: {word[4]}")
            
            print("\n수정할 내용을 입력하세요 (변경 없으면 Enter):")
            new_english = input("영어 단어: ")
            new_meaning = input("의미: ")
            new_pos = input("품사: ")
            new_example = input("예문: ")
            
            # 변경된 값만 업데이트
            updates = []
            values = []
            if new_english:
                updates.append("english_word = ?")
                values.append(new_english)
            if new_meaning:
                updates.append("meaning = ?")
                values.append(new_meaning)
            if new_pos:
                updates.append("part_of_speech = ?")
                values.append(new_pos)
            if new_example:
                updates.append("example_sentence = ?")
                values.append(new_example)
            
            if updates:
                values.append(english)  # WHERE 조건을 위한 원래 단어
                query = f"UPDATE Word SET {', '.join(updates)} WHERE english_word = ?"
                self.cursor.execute(query, values)
                self.conn.commit()
                print("\n단어가 수정되었습니다.")
                
                # 수정된 단어 정보 표시
                self.cursor.execute("SELECT * FROM Word WHERE english_word = ?", (new_english if new_english else english,))
                updated_word = self.cursor.fetchone()
                print("\n수정된 단어 정보:")
                print(f"영어: {updated_word[1]}")
                print(f"의미: {updated_word[2]}")
                print(f"품사: {updated_word[3]}")
                print(f"예문: {updated_word[4]}")
            else:
                print("\n변경사항이 없습니다.")
                
        except sqlite3.Error as e:
            print(f"데이터베이스 오류: {str(e)}")

    def delete_word(self):
        """
        단어를 삭제합니다.
        영어 단어를 입력받아 해당 단어를 삭제합니다.
        """
        print("\n=== 단어 삭제 ===")
        english = input("삭제할 영어 단어를 입력하세요: ")
        
        try:
            # 단어 존재 여부 확인
            self.cursor.execute("SELECT * FROM Word WHERE english_word = ?", (english,))
            word = self.cursor.fetchone()
            if not word:
                print("해당 단어가 없습니다.")
                return
            
            # 삭제 전 단어 정보 표시
            print(f"\n삭제할 단어 정보:")
            print(f"영어: {word[1]}")
            print(f"의미: {word[2]}")
            print(f"품사: {word[3]}")
            print(f"예문: {word[4]}")
            
            confirm = input("\n정말 삭제하시겠습니까? (y/n): ")
            if confirm.lower() == 'y':
                self.cursor.execute("DELETE FROM Word WHERE english_word = ?", (english,))
                self.conn.commit()
                print("단어가 삭제되었습니다.")
            else:
                print("삭제가 취소되었습니다.")
                
        except sqlite3.Error as e:
            print(f"데이터베이스 오류: {str(e)}")

    def manage_categories(self):
        """
        카테고리를 관리합니다.
        """
        print("\n=== 카테고리 관리 ===")
        # TODO: 카테고리 관리 기능 구현
        print("카테고리 관리 기능은 아직 구현되지 않았습니다.")

    def show_wordbook_menu(self):
        """
        단어장 메뉴를 표시하고 사용자 선택을 처리합니다.
        """
        while True:
            print("\n=== 단어장 ===")
            print("1. 단어 목록 보기")
            print("2. 단어 추가")
            print("3. 단어 수정")
            print("4. 단어 삭제")
            print("5. 카테고리 관리")
            print("6. 돌아가기")
            
            choice = input("\n원하는 작업을 선택하세요 (1-6): ")
            
            if choice == "1":
                self.show_word_list()
            elif choice == "2":
                self.add_word()
            elif choice == "3":
                self.edit_word()
            elif choice == "4":
                self.delete_word()
            elif choice == "5":
                self.manage_categories()
            elif choice == "6":
                print("단어장을 종료합니다.")
                break
            else:
                print("잘못된 선택입니다. 다시 선택해주세요.") 
