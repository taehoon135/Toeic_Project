import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Create db
import pandas as pd
from quiz_generation.rain_quiz import RainQuizModel
from database.word_db import WordDB

# 현재 파일의 디렉토리 경로
current_dir = os.path.dirname(os.path.abspath(__file__))

# 상대 경로를 절대 경로로 변환
db_path = os.path.join(current_dir, '../../toeic_vocabulary.db')

word_db = WordDB(db_path=db_path)

word_db.add_word('apple', '사과', 'noun', 'I like apples.')
word_db.add_word('banana', '바나나', 'noun', 'I like bananas.')
word_db.add_word('orange', '오렌지', 'noun', 'I like oranges.')
word_db.add_word('pear', '배', 'noun', 'I like pears.')
word_db.add_word('pineapple', '파인애플', 'noun', 'I like pineapples.')

word_list = word_db.get_all_words()

if not word_list:
    print("No words found")
    exit()

# Create model
model = RainQuizModel(word_list)

# Print quiz
for i in model:
    print(i)

# Equivalently
#result = model.get()
#for i in result:
#    print(i)
