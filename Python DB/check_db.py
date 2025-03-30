import sqlite3

def check_users():
    conn = sqlite3.connect("toeic_vocab.db")
    cursor = conn.cursor()
    
    print("\n=== 등록된 사용자 목록 ===")
    cursor.execute("SELECT user_id, password, username, is_admin FROM User")
    users = cursor.fetchall()
    
    if not users:
        print("등록된 사용자가 없습니다.")
    else:
        for user in users:
            print("\nID:", user[0])
            print("비밀번호(해시값):", user[1])
            print("이름:", user[2])
            print("관리자여부:", '예' if user[3] else '아니오')
            print("-" * 50)
    
    conn.close()

if __name__ == "__main__":
    check_users() 