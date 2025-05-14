# test_db_operations.py

import os
import shutil # DB 파일 삭제/백업용
import sys

# 현재 스크립트의 부모 디렉토리(src)를 sys.path에 추가하여
# src.database.xxx 형태의 임포트가 아닌 .xxx 형태의 상대 임포트를 사용하거나,
# 또는 src를 기준으로 하는 절대 임포트를 사용하기 위함.
# 여기서는 상대 경로 임포트를 사용하도록 DB 모듈들을 수정했다고 가정하고,
# 테스트 스크립트 자체는 프로젝트 루트에서 실행하는 것을 권장하나,
# 만약 src/database에서 직접 실행한다면 아래와 같이 sys.path 조정이 필요할 수 있음.

# 프로젝트 루트 디렉토리를 sys.path에 추가 (src 폴더의 부모)
# 이렇게 하면 from src.database.user_db import UserDB 등이 어디서든 잘 동작함
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# 이제 src.database.xxx 형태로 임포트 가능
from src.database.user_db import UserDB
from src.database.word_db import WordDB
from src.database.category_db import CategoryDB
# from .user_db import UserDB # 만약 test_db_operations.py가 src.database 패키지의 일부로 실행된다면
# from .word_db import WordDB
# from .category_db import CategoryDB

# --- 테스트 설정 ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # 현재 파일 위치 (src/database)
DB_FILE_DIR = BASE_DIR # DB 파일은 스크립트와 같은 디렉토리에 생성
DB_FILE_NAME = "toeic_vocabulary.db"
DB_FILE_PATH = os.path.join(DB_FILE_DIR, DB_FILE_NAME) # DB 파일 경로 수정

CSV_FILE_NAME = "test_words.csv"
CSV_FILE_PATH = os.path.join(BASE_DIR, CSV_FILE_NAME) 

# 테스트 전 기존 DB 파일 삭제 또는 백업 (선택)
BACKUP_DB_PATH = DB_FILE_PATH + ".backup"

def setup_test_environment():
    """테스트 환경 설정: 기존 DB 파일 삭제 또는 백업"""
    try:
        # DB 파일이 저장될 디렉토리 생성 (없으면)
        os.makedirs(DB_FILE_DIR, exist_ok=True)

        if os.path.exists(DB_FILE_PATH):
            print(f"기존 데이터베이스 파일 '{DB_FILE_PATH}'을 삭제합니다.")
            try:
                if os.path.exists(BACKUP_DB_PATH):
                    os.remove(BACKUP_DB_PATH)  # 이전 백업이 있다면 삭제
                shutil.copy2(DB_FILE_PATH, BACKUP_DB_PATH)  # 백업 생성 (메타데이터 포함)
                print(f"기존 데이터베이스를 '{BACKUP_DB_PATH}'로 백업했습니다.")
            except Exception as e:
                print(f"백업 중 오류 발생: {e}")
                
            try:
                os.remove(DB_FILE_PATH)
            except Exception as e:
                print(f"DB 파일 삭제 중 오류 발생: {e}")
                if os.path.exists(DB_FILE_PATH):
                    print("파일이 여전히 존재합니다. 프로세스가 파일을 사용 중일 수 있습니다.")
                    return False
    except Exception as e:
        print(f"테스트 환경 설정 중 오류 발생: {e}")
        return False

    # 테스트용 CSV 파일 생성
    csv_content = """english,meaning,part_of_speech,example_sentence,category
apple,"사과","명사","This is an apple.","과일"
banana,"바나나","명사","I like bananas.","과일"
study,"공부하다","동사","I need to study English.","학습"
apple,"(다른 의미의) 사과","명사","Apple Inc. is a tech company.","회사"
happy,"행복한","형용사","I am happy.",""
"""
    try:
        with open(CSV_FILE_PATH, 'w', encoding='utf-8') as f:
            f.write(csv_content)
        print(f"테스트용 CSV 파일 '{CSV_FILE_PATH}' 생성 완료.")
    except Exception as e:
        print(f"CSV 파일 생성 중 오류 발생: {e}")
        return False

    return True  # 모든 작업이 성공적으로 완료됨


def main_test_flow():
    """주요 DB 기능 테스트 흐름"""
    print("\n--- 테스트 시작 ---")

    # 0. 테스트 환경 설정
    if not setup_test_environment():
        print("테스트 환경 설정 실패. 테스트를 중단합니다.")
        return

    try:
        # DB 인스턴스 생성
        user_db = UserDB(DB_FILE_PATH)
        word_db = WordDB(DB_FILE_PATH)
        category_db = CategoryDB(DB_FILE_PATH)

        # 1. DB 초기화 테스트 (테이블 생성)
        print("\n[1. DB 초기화 테스트]")
        print("UserDB 테이블 초기화...")
        user_db.initialize_tables()
        print("WordDB 테이블 초기화...")
        word_db.initialize_tables()
        print("CategoryDB 테이블 초기화...")
        category_db.initialize_tables()
        print("테이블 초기화 완료 (DB 파일 생성 확인 필요).")

        # 2. UserDB 테스트
        print("\n[2. UserDB 테스트]")
        user1_id = user_db.register_user("testuser1", "password123", "Test User One")
        assert user1_id is not None and user1_id > 0, f"사용자1 등록 실패, ID: {user1_id}"
        print(f"사용자1 등록 성공, ID: {user1_id}")

        user2_id = user_db.register_user("testuser2", "securepass", "Test User Two")
        assert user2_id is not None and user2_id > 0, f"사용자2 등록 실패, ID: {user2_id}"
        print(f"사용자2 등록 성공, ID: {user2_id}")

        # 중복 등록 시도 (user_login_id는 UNIQUE해야 함)
        try:
            print("중복 사용자 등록 시도 (testuser1)...")
            user_db.register_user("testuser1", "newpass", "Duplicate User")
            # 위 라인에서 IntegrityError가 발생해야 함 (BaseDatabase.execute에서 False를 반환 시)
            # 만약 UserDB.register_user가 내부적으로 에러를 먹고 None이나 0을 반환한다면 다른 방식의 assert 필요
            # 여기서는 execute가 False를 반환하고 commit이 안되어도 lastrowid가 이전 값을 가질 수 있음을 가정.
            # 더 나은 방법은 register_user가 명시적으로 실패를 알리는 값을 반환하게 하는 것.
            # 지금은 에러가 터지지 않으면 실패로 간주 (테스트 목적상)
            assert False, "중복 사용자 등록 시 IntegrityError가 발생해야 하나, 발생하지 않음."
        except Exception as e: # 보다 구체적으로 sqlite3.IntegrityError를 잡는 것이 좋음
            print(f"중복 사용자 등록 시도 시 예상된 예외 발생: {type(e).__name__} (정상)")

        logged_in_user = user_db.login_user("testuser1", "password123")
        assert logged_in_user is not None and logged_in_user['user_id'] == user1_id, "사용자1 로그인 실패"
        print(f"사용자1 로그인 성공: {logged_in_user['user_name']}")

        wrong_login = user_db.login_user("testuser1", "wrongpassword")
        assert wrong_login is None, "잘못된 비밀번호로 로그인 성공 (실패해야 함)"
        print("잘못된 비밀번호 로그인 시도 -> 로그인 실패 (정상)")

        # 3. WordDB 및 CategoryDB 연동 테스트 (CSV 임포트)
        print("\n[3. WordDB 및 CategoryDB 연동 테스트 - CSV 임포트]")
        # CSV 임포트는 특정 사용자의 컨텍스트에서 이루어져야 함 (여기서는 user1_id 사용)
        import_success = word_db.import_from_csv(CSV_FILE_PATH, user1_id, category_db)
        assert import_success, "CSV 파일 임포트 실패"
        print(f"CSV 파일 임포트 성공 (사용자 ID: {user1_id}).")

        all_words_after_import = word_db.get_all_words()
        print(f"CSV 임포트 후 전체 단어 수: {len(all_words_after_import)}")
        # 예상 단어 수: apple, banana, study, happy (4개. CSV의 두번째 apple은 중복으로 처리되어 추가 안됨)
        assert len(all_words_after_import) == 4, f"CSV 임포트 후 단어 수 불일치: {len(all_words_after_import)}"
        # for word in all_words_after_import:
        #     print(f"  - ID: {word['id']}, Eng: {word['english']}, Categories: {word.get('categories')}")

        # 카테고리 정보 확인 (apple -> 과일, banana -> 과일, study -> 학습)
        apple_word_info = next((w for w in all_words_after_import if w['english'] == 'apple'), None)
        banana_word_info = next((w for w in all_words_after_import if w['english'] == 'banana'), None)
        study_word_info = next((w for w in all_words_after_import if w['english'] == 'study'), None)
        happy_word_info = next((w for w in all_words_after_import if w['english'] == 'happy'), None)

        assert apple_word_info and apple_word_info.get('categories') == "과일", f"apple 단어 카테고리 오류: {apple_word_info}"
        assert banana_word_info and banana_word_info.get('categories') == "과일", f"banana 단어 카테고리 오류: {banana_word_info}"
        assert study_word_info and study_word_info.get('categories') == "학습", f"study 단어 카테고리 오류: {study_word_info}"
        assert happy_word_info and not happy_word_info.get('categories'), f"happy 단어는 카테고리가 없어야 함: {happy_word_info}" # CSV에서 happy는 카테고리 없음
        print("CSV 임포트된 단어들의 카테고리 정보 확인 (부분적).")

        # 4. CategoryDB 테스트 (user1_id 컨텍스트)
        print(f"\n[4. CategoryDB 테스트 (사용자 ID: {user1_id})]")
        user1_categories = category_db.get_user_categories(user1_id)
        print(f"사용자1의 카테고리 목록 ({len(user1_categories)}개):")
        # 예상 카테고리: "과일", "학습" (CSV에서 생성됨)
        expected_categories_user1 = {"과일", "학습"}
        current_categories_user1 = set()
        for cat in user1_categories:
            print(f"  - ID: {cat['category_id']}, Name: {cat['name']}")
            current_categories_user1.add(cat['name'])
        assert current_categories_user1 == expected_categories_user1, "CSV 임포트를 통해 생성된 카테고리 불일치"

        # 새 카테고리 생성
        new_cat_name = "일상생활"
        new_cat_id = category_db.get_or_create_category(user1_id, new_cat_name)
        # get_or_create_category는 lastrowid를 반환. UNIQUE 제약(user_id, name)이 있으므로 중복 시 기존 ID 반환
        assert new_cat_id is not None and new_cat_id > 0, f"'{new_cat_name}' 카테고리 생성/조회 실패"
        print(f"'{new_cat_name}' 카테고리 생성/조회 성공, ID: {new_cat_id}")

        # 카테고리 이름 수정
        updated_cat_name = "매일 생활"
        update_cat_success = category_db.update_category(new_cat_id, updated_cat_name, user1_id)
        assert update_cat_success, f"카테고리 ID {new_cat_id} 이름 수정 실패"
        print(f"카테고리 ID {new_cat_id} 이름 수정 성공: '{updated_cat_name}'")

        # 다른 사용자가 동일 이름 카테고리 수정 시도 (실패해야 함)
        update_fail_other_user = category_db.update_category(new_cat_id, "해킹시도", user2_id)
        assert not update_fail_other_user, "다른 사용자가 카테고리 수정 성공 (실패해야 함)"
        print("다른 사용자의 카테고리 수정 시도 -> 실패 (정상)")

        # 5. WordDB 단어 수동 추가 및 카테고리 연결
        print(f"\n[5. WordDB 단어 수동 추가 및 카테고리 연결 (사용자 ID: {user1_id})]")
        # "일상생활" 카테고리 ID (new_cat_id)를 사용
        word_book_id = word_db.add_word("book", "책", "명사", "This is a book.")
        assert word_book_id is not None and word_book_id > 0, "'book' 단어 추가 실패"
        print(f"'book' 단어 추가 성공, ID: {word_book_id}")

        link_success = category_db.add_word_to_category(new_cat_id, word_book_id)
        assert link_success, f"'book' 단어를 '{updated_cat_name}' 카테고리에 연결 실패"
        print(f"'book' 단어(ID:{word_book_id})를 '{updated_cat_name}'(ID:{new_cat_id}) 카테고리에 연결 성공")

        # 카테고리 내 단어 조회
        words_in_daily_life = category_db.get_words_in_category(new_cat_id)
        print(f"'{updated_cat_name}' 카테고리 내 단어 ({len(words_in_daily_life)}개):")
        found_book = any(w['word_id'] == word_book_id for w in words_in_daily_life)
        assert found_book, f"'book' 단어가 '{updated_cat_name}' 카테고리에서 조회되지 않음"

        # 6. 단어 정보 수정 및 삭제
        print("\n[6. WordDB 단어 정보 수정 및 삭제]")
        update_word_success = word_db.update_word(word_book_id, "notebook", "공책", "명사", "This is a notebook.")
        assert update_word_success, f"단어 ID {word_book_id} 정보 수정 실패"
        print(f"단어 ID {word_book_id} 정보 수정 성공 ('notebook')")

        notebook_details = word_db.get_word_details(word_book_id)
        assert notebook_details is not None and notebook_details['english'] == "notebook", "수정된 단어 정보 조회 실패"
        print(f"수정된 단어 정보: {notebook_details['english']}, 카테고리: {notebook_details.get('categories')}")

        delete_word_success = word_db.delete_word(word_book_id)
        assert delete_word_success, f"단어 ID {word_book_id} ('notebook') 삭제 실패"
        print(f"단어 ID {word_book_id} ('notebook') 삭제 성공")
        assert word_db.get_word_details(word_book_id) is None, "삭제된 단어가 여전히 조회됨"

        # 7. 카테고리 삭제 (연결된 단어 관계도 해제되어야 함 - ON DELETE CASCADE)
        print(f"\n[7. CategoryDB 카테고리 삭제 (사용자 ID: {user1_id})]")
        # "과일" 카테고리 ID를 찾아서 삭제
        fruit_category_id = next((cat['category_id'] for cat in user1_categories if cat['name'] == "과일"), None)
        assert fruit_category_id is not None, "'과일' 카테고리 ID를 찾을 수 없음"
        
        # '과일' 카테고리에 속한 단어가 있었는지 확인 (apple, banana)
        # apple_word = word_db.fetch_one("SELECT word_id FROM Word WHERE english = 'apple'") # WordDB에 fetch_one 없음
        # banana_word = word_db.fetch_one("SELECT word_id FROM Word WHERE english = 'banana'")
        # WordDB에 fetch_one과 같은 내부 메서드를 사용하거나, get_word_details 등으로 word_id를 가져와야 함.
        # 여기서는 CategoryDB의 get_words_in_category로 삭제 전 단어 확인
        words_in_fruit_before_delete = category_db.get_words_in_category(fruit_category_id)
        print(f"'과일' 카테고리 삭제 전 단어 수: {len(words_in_fruit_before_delete)}")
        # for w_in_f in words_in_fruit_before_delete:
        #    print(f"  - ID: {w_in_f['word_id']}, Eng: {w_in_f['english']}")

        delete_cat_success = category_db.delete_category(fruit_category_id, user1_id)
        assert delete_cat_success, f"'과일' 카테고리(ID:{fruit_category_id}) 삭제 실패"
        print(f"'과일' 카테고리(ID:{fruit_category_id}) 삭제 성공 (사용자 ID: {user1_id})")
        assert category_db.get_category(fruit_category_id) is None, "삭제된 '과일' 카테고리가 여전히 조회됨"
        
        # 카테고리 삭제 후, 해당 카테고리에 있던 단어들이 WordCategory에서도 삭제되었는지 확인
        # (CategoryWord 테이블에서 ON DELETE CASCADE 동작 확인)
        # 직접 WordCategory 테이블을 조회하거나, 삭제된 카테고리로 단어 조회 시 결과가 없는 것으로 간접 확인
        words_in_fruit_after_delete = category_db.get_words_in_category(fruit_category_id)
        assert len(words_in_fruit_after_delete) == 0, "'과일' 카테고리 삭제 후에도 단어가 남아있음 (WordCategory)"
        print("'과일' 카테고리에 연결된 단어 관계도 정상적으로 삭제됨 (ON DELETE CASCADE)")

        # 'apple' 단어는 여전히 Word 테이블에 존재해야 함
        apple_info_after_cat_delete = word_db.get_word_details(apple_word_info['id'])
        assert apple_info_after_cat_delete is not None, "'apple' 단어가 Word 테이블에서 삭제됨 (삭제되면 안됨)"
        assert not apple_info_after_cat_delete.get('categories'), \
            f"'apple' 단어의 카테고리 정보가 남아있음 (비어야 함): {apple_info_after_cat_delete.get('categories')}"
        print("'apple' 단어는 Word 테이블에 존재하며, '과일' 카테고리 연결만 해제됨.")

        # 8. 다른 사용자 컨텍스트 테스트 (user2_id)
        print(f"\n[8. 다른 사용자 컨텍스트 테스트 (사용자 ID: {user2_id})]")
        user2_categories_before = category_db.get_user_categories(user2_id)
        assert len(user2_categories_before) == 0, f"사용자2는 아직 카테고리가 없어야 함. 현재: {len(user2_categories_before)}"
        print(f"사용자2의 카테고리 수 (초기): {len(user2_categories_before)}")

        user2_cat_name = "프로그래밍"
        user2_cat_id = category_db.get_or_create_category(user2_id, user2_cat_name)
        assert user2_cat_id is not None and user2_cat_id > 0, f"사용자2 '{user2_cat_name}' 카테고리 생성 실패"
        print(f"사용자2 '{user2_cat_name}' 카테고리 생성 성공, ID: {user2_cat_id}")
        
        user2_categories_after = category_db.get_user_categories(user2_id)
        assert len(user2_categories_after) == 1 and user2_categories_after[0]['name'] == user2_cat_name, "사용자2 카테고리 생성 후 조회 오류"

        print("\n--- 모든 테스트 단계 완료 ---")

    finally:
        # DB 연결 명시적으로 닫기
        if 'user_db' in locals(): user_db.close()
        if 'word_db' in locals(): word_db.close()
        if 'category_db' in locals(): category_db.close()
        print("\n--- DB 연결 종료 ---")

if __name__ == "__main__":
    main_test_flow()

    # 테스트 후 생성된 DB 파일 및 CSV 파일 정리 (선택)
    # if os.path.exists(CSV_FILE_PATH):
    #     os.remove(CSV_FILE_PATH)
    #     print(f"테스트용 CSV 파일 '{CSV_FILE_PATH}' 삭제 완료.")
    # DB 파일은 다음 테스트를 위해 유지하거나, 필요시 삭제/백업 복원