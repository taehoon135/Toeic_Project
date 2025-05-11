from abc import ABC, abstractmethod
from typing import Tuple, List


class BaseQuizModel(ABC):
    """
    Base class for quiz model

    Input:
        db: database
        APIKEY: optional APIKEY
    Output:
        (Question, Answer, Hint) pairs
    
    Whole pairs can be retrieved by .get() method at once
    This class can be used as an iterable, which returns single pairs at a time
    """
    def __init__(self, db, APIKEY = None):
        pass

    @abstractmethod
    def _parse_db(self, db):
        pass

    @abstractmethod
    def _create_pairs(self, parsed_db):
        pass

    @abstractmethod
    def get(self) -> List[Tuple[str,str,str]]:
        """
        Returns every (Question, Answer, Hint) pairs

        Returns:
            List[Tuple[str,str,str]]: List of (Question, Answer, Hint)
        """
        pass
    
    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def __next__(self):
        pass