from quiz_generation.base_quiz_gen_class import BaseQuizModel
from typing import Tuple, List
from jamo import h2j, j2hcj


class ShortAnswerEKQuizModel(BaseQuizModel):
    def __init__(self, db):
        super().__init__(db)
        self.pairs = []
        self.current_index = 0
        self.words = []
        self.meanings = []
        self._parse_db(db)
    
    def _parse_db(self, db):
        for word in db:
            word_id, english, meaning, pos, example = word
            self.words.append(english)
            self.meanings.append(meaning)
        self._create_pairs()

    def _create_pairs(self):
        for word, meaning in zip(self.words, self.meanings):
            question = f"이 단어의 뜻이 무엇인가요: {word}"
            self.pairs.append((question, meaning, self.__extract_initial(meaning)))

    def __extract_initial(self, word):
        list = []
        for x in word:
            temp = h2j(x)
            imf = j2hcj(temp)
            list.append(imf[0])
        return "".join(list)

    def get(self) -> List[Tuple[str, str, str]]:
        return self.pairs
    
    def __iter__(self):
        self.current_index = 0
        return self

    def __next__(self):
        if self.current_index >= len(self.pairs):
            raise StopIteration
        pair = self.pairs[self.current_index]
        self.current_index += 1
        return pair
    

class ShortAnswerKEQuizModel(BaseQuizModel):
    def __init__(self, db):
        super().__init__(db)
        self.pairs = []
        self.current_index = 0
        self.words = []
        self.meanings = []
        self._parse_db(db)
    
    def _parse_db(self, db):
        for word in db:
            word_id, english, meaning, pos, example = word
            self.words.append(english)
            self.meanings.append(meaning)
        self._create_pairs()

    def _create_pairs(self):
        ratio = 0.3
        for word, meaning in zip(self.words, self.meanings):
            question = f"다음 의미를 가지는 단어는 무엇인가요: {meaning}"
            length = max(int(len(word) * ratio), 1)
            self.pairs.append((question, word, word[:length] + '_' * (len(word) - length)))

    def get(self) -> List[Tuple[str, str, str]]:
        return self.pairs
    
    def __iter__(self):
        self.current_index = 0
        return self

    def __next__(self):
        if self.current_index >= len(self.pairs):
            raise StopIteration
        pair = self.pairs[self.current_index]
        self.current_index += 1
        return pair