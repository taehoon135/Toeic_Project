import unittest
import pandas as pd
from quiz_generation.four_choice_quiz import FourChoiceQuizModel

class TestFourChoiceQuizModel(unittest.TestCase):
    def setUp(self):
        # Sample data for testing
        data = {
            "word": ["apple", "banana", "orange", "grape"],
            "meaning": ["사과", "바나나", "오렌지", "포도"]
        }
        self.db = pd.DataFrame(data)
        self.model = FourChoiceQuizModel(self.db)

    def test_pairs_creation(self):
        pairs = self.model.get()
        self.assertEqual(len(pairs), 4)  # Should create 4 pairs
        self.assertIn(pairs[0][0], ["다음의 뜻을 가진 단어는? 뜻: 사과", "다음의 뜻을 가진 단어는? 뜻: 바나나", "다음의 뜻을 가진 단어는? 뜻: 오렌지", "다음의 뜻을 가진 단어는? 뜻: 포도"])

    def test_iteration(self):
        expected_length = len(self.model.get())
        for _ in self.model:
            expected_length -= 1
        self.assertEqual(expected_length, 0)

if __name__ == "__main__":
    unittest.main()