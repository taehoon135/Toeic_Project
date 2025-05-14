import unittest
import pandas as pd
from quiz_generation.rain_quiz import RainQuizModel

class TestRainQuizModel(unittest.TestCase):
    def setUp(self):
        # Sample data for testing
        data = {
            "word": ["apple", "banana"],
            "meaning": ["사과", "바나나"]
        }
        self.db = pd.DataFrame(data)
        self.model = RainQuizModel(self.db)

    def test_pairs_creation(self):
        pairs = self.model.get()
        self.assertEqual(len(pairs), 2)
        self.assertEqual(pairs[0], ("apple", "사과", "hint"))

    def test_iteration(self):
        expected_pairs = [
            ("apple", "사과", "hint"),
            ("banana", "바나나", "hint")
        ]
        
        for i, pair in enumerate(self.model):
            self.assertEqual(pair, expected_pairs[i])
        
        with self.assertRaises(StopIteration):
            next(self.model)

if __name__ == "__main__":
    unittest.main()