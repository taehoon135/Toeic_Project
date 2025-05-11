from quiz_generation.base_quiz_gen_class import BaseQuizModel
from typing import Tuple, List
from LLM.LLMResponse import get_response
from googletrans import Translator
import asyncio


PROMPT_BASE = "주어진 단어에 대하여, 영어로 쓰인, 한국인 사용자가 풀 수 있는 빈칸 퀴즈를 만들어줘."\
                "각 단어 당 하나의 문제를 만들어줘."\
                "퀴즈 페어를 제외하고는 아무것도 출력하지 마."\
                "[input word format]: \"word1;word2;word3;...\" "\
                "[output format]: \"Q:question;A:answer(newline)...\" "\
                "[Example]: \"Q:His behavior was clearly ______, driven by a deep-seated need for attention;A:pathological\" "\
                "[words]:"


class ClozeQuizModel(BaseQuizModel):
    def __init__(self, db, APIKEY=None):
        super().__init__(db)
        self.pairs = []
        self.current_index = 0
        self.APIKEY = APIKEY
        self.db = db
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
        # Create the prompt using the current words
        prompt = self.__create_prompt()
        
        # Get the response from the LLM
        response = get_response(prompt, "gemini-2.0-flash", self.APIKEY)
        
        # Parse the response to get question-answer pairs
        qa_pairs = self.__parse_llm_response(response)
        translated_questions = self.__translate_examples([i[0] for i in qa_pairs])

        # Create quiz pairs
        for (question, answer), translated_question in zip(qa_pairs, translated_questions):

            self.pairs.append((question, answer, translated_question))

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
    
    def __create_prompt(self) -> str:
        """
        Creates a complete prompt from the quiz pairs.
        
        Returns:
            str: A formatted string containing all questions.
        """
        prompt = PROMPT_BASE
        for word in self.words:
            prompt += f"{word};\n"
        return prompt.strip()

    def __parse_llm_response(self, response: str) -> List[Tuple[str, str]]:
        """
        Parses the response from the LLM to extract question-answer pairs.
        
        Args:
            response (str): The response string from the LLM.
        
        Returns:
            List[Tuple[str, str]]: A list of tuples containing (question, answer).
        """
        qa_pairs = []
        lines = response.strip().split('\n')
        for line in lines:
            if line.startswith("Q:") and ";A:" in line:
                q, a = line.split(';A:')
                qa_pairs.append((q.replace('Q:', '').strip(), a.strip()))
        return qa_pairs
    
    def __translate_examples(self, examples: List[str]) -> List[str]:
        translator = Translator()
        result = translator.translate(examples, src="en", dest="ko")

        result = asyncio.get_event_loop().run_until_complete(result) 
        return [i.text for i in result]
