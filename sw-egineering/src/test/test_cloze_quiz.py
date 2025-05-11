import unittest
import pandas as pd
from quiz_generation.cloze_quiz import ClozeQuizModel
import time

class TestClozeQuizModel(unittest.TestCase):
    def setUp(self):
        # Sample data for testing
        data = {
            "word": ["apple", "banana"],
            "meaning": ["사과", "바나나"]
        }
        self.db = pd.DataFrame(data)
        self.model = ClozeQuizModel(self.db, APIKEY="dummy")

    def test_pairs_creation(self):
        # Mocking the LLM response
        pairs = self.model.get()
        for pair in pairs:
            print(pair)
        self.assertGreater(len(pairs), 0)  # Ensure pairs are created

    def test_iteration(self):
        self.model._create_pairs()  # Ensure pairs are created
        expected_length = len(self.model.get())
        for _ in self.model:
            expected_length -= 1
        self.assertEqual(expected_length, 0)

if __name__ == "__main__":
    unittest.main()