import csv
import sqlite3

def import_words_from_csv(csv_file_path):
    """
    CSV 파일에서 단어를 읽어 데이터베이스에 저장합니다.
    
    CSV 파일 형식:
    word_id,english_word,meaning,part_of_speech,example_sentence
    
    Args:
        csv_file_path (str): CSV 파일 경로
    """
    conn = sqlite3.connect("toeic_vocab.db")
    cursor = conn.cursor()
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            # 데이터 삽입
            for row in csv_reader:
                cursor.execute("""
                INSERT INTO Word (english_word, meaning, part_of_speech, example_sentence)
                VALUES (?, ?, ?, ?)
                """, (
                    row['english_word'],
                    row['meaning'],
                    row['part_of_speech'],
                    row['example_sentence']
                ))
            
            conn.commit()
            print(f"단어 가져오기 완료!")
            
            # 가져온 단어 수 확인
            cursor.execute("SELECT COUNT(*) FROM Word")
            word_count = cursor.fetchone()[0]
            print(f"현재 데이터베이스에 있는 총 단어 수: {word_count}")
            
    except Exception as e:
        print(f"오류 발생: {str(e)}")
        conn.rollback()
    
    finally:
        conn.close()

if __name__ == "__main__":
    csv_file_path = "toeic_word.csv"  # 현재 디렉토리의 파일 경로
    import_words_from_csv(csv_file_path) 