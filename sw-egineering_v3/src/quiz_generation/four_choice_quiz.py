from quiz_generation.base_quiz_gen_class import BaseQuizModel
from typing import Tuple, List
import random


class FourChoiceQuizModel(BaseQuizModel):
    def __init__(self, db):
        super().__init__(db)
        self.pairs = []
        self.current_index = 0
        self.words = []
        self.meanings = []
        self._parse_db(db)
    
    def _parse_db(self, db):
        for word in db:
            #word_id, english, meaning, pos, example = word
            self.words.append(word["english"])
            self.meanings.append(word["meaning"])
        self._create_pairs()

    def _create_pairs(self):
        # The first word in Question is the correct answer  
        for word, meaning in zip(self.words, self.meanings):
            # Get 3 random other words as distractors
            other_words = random.sample([w for w in self.words if w != word], 3)
            # Combine correct answer with distractors and shuffle
            choices = [word] + other_words
            # random.shuffle(choices)
            choices_str = ",".join(choices)
            
            question = f"다음의 뜻을 가진 단어는? 뜻: {meaning}"
            self.pairs.append((question, choices_str, "hint"))

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