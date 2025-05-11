import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Create db
import pandas as pd
from quiz_generation.four_choice_quiz import FourChoiceQuizModel

df = pd.read_csv("DB_module/toeic_word.csv")

word_id, english, meaning, pos, example = df.iloc[0]

db = [df.iloc[i] for i in range(10)]

# Create model
model = FourChoiceQuizModel(db)

# Print quiz
for i in model:
    print(i)

# Equivalently
#result = model.get()
#for i in result:
#    print(i)
