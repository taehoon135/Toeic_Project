import unittest
import pandas as pd
from quiz_generation.base_quiz_gen_class import BaseQuizModel

class TestQuizModel(BaseQuizModel):
    def __init__(self, db, APIKEY):
        self.__parsed_db: pd.DataFrame = self._parse_db(db)
        self.__pairs = self._create_pairs(self.__parsed_db, APIKEY)

    def _parse_db(self, db):
        # 실제로는 db 를 parsing 하지만, demo 이므로 간단히 구현
        data = [{"Word": "hello", "Meaning": "안녕", "Multiplicity":1},
                {"Word": "world", "Meaning": "세계", "Multiplicity":5}]
        return pd.DataFrame(data)

    def _create_pairs(self, parsed_db: pd.DataFrame, APIKEY):
        question_template = "다음 의미를 가지는 단어의 뜻은?: {0}"
        default_hint = "Hint"
        return [(question_template.format(row[0]), row[1], default_hint) for row in parsed_db.itertuples(index=False, name=None)]

    def get(self):
        """
        Returns every (Question, Answer, Hint) pairs

        Returns:
            List[Tuple[str,str,str]]: List of (Question, Answer, Hint)
        """
        return self.__pairs
    
    def __iter__(self):
        self.__index = 0
        return self

    def __next__(self):
        if self.__index >= len(self.__pairs):
            raise StopIteration
        
        result = self.__pairs[self.__index]
        self.__index += 1
        return result

class TestQuizModelFunctionality(unittest.TestCase):
    def setUp(self):
        self.db = "Some DB"
        self.quiz_model = TestQuizModel(self.db, None)

    def test_get_method(self):
        pairs = self.quiz_model.get()
        self.assertEqual(len(pairs), 2)
        self.assertEqual(pairs[0][0], "다음 의미를 가지는 단어의 뜻은?: hello")
        self.assertEqual(pairs[0][1], "안녕")
        self.assertEqual(pairs[0][2], "Hint")

    def test_iteration(self):
        expected_pairs = [
            ("다음 의미를 가지는 단어의 뜻은?: hello", "안녕", "Hint"),
            ("다음 의미를 가지는 단어의 뜻은?: world", "세계", "Hint")
        ]
        
        # Test iteration
        for i, pair in enumerate(self.quiz_model):
            self.assertEqual(pair, expected_pairs[i])
        
        # Test that iteration is exhausted
        with self.assertRaises(StopIteration):
            next(self.quiz_model)

    def test_parsed_db(self):
        parsed_db = self.quiz_model._parse_db(self.db)
        self.assertIsInstance(parsed_db, pd.DataFrame)
        self.assertEqual(len(parsed_db), 2)
        self.assertEqual(parsed_db.iloc[0]["Word"], "hello")
        self.assertEqual(parsed_db.iloc[0]["Meaning"], "안녕")

if __name__ == "__main__":
    unittest.main()