"""
QuizDB API 명세서 (실제 구현 기준)

- 퀴즈 생성, 문제 추가, 결과 기록, 통계 조회 등 퀴즈 관련 DB 함수 명세
"""

# 퀴즈 생성
def create_quiz(quiz_type: str, category_id: int = None) -> int:
    """
    Args:
        quiz_type (str): 퀴즈 유형
        category_id (int, optional): 카테고리 PK
    Returns:
        int: 생성된 퀴즈 PK
    Example:
        quiz_id = quiz_db.create_quiz('multiple_choice', 1)
    """
    pass

# 퀴즈에 문제 추가
def add_quiz_question(quiz_id: int, question: str, correct_answer: str, options: str = None, hint: str = None) -> int:
    """
    Args:
        quiz_id (int): 퀴즈 PK
        question (str): 문제
        correct_answer (str): 정답
        options (str, optional): 보기 (JSON 문자열)
        hint (str, optional): 힌트
    Returns:
        int: 생성된 문제 PK
    Example:
        question_id = quiz_db.add_quiz_question(1, 'apple의 뜻은?', '사과', '["사과", "바나나", "오렌지"]')
    """
    pass

# 퀴즈 상세 정보(문제 포함) 조회
def get_quiz(quiz_id: int) -> dict:
    """
    Args:
        quiz_id (int): 퀴즈 PK
    Returns:
        dict: 퀴즈 정보와 문제 목록
    Example:
        quiz = quiz_db.get_quiz(1)
    """
    pass

# 카테고리별 퀴즈 목록 조회
def get_quizzes_by_category(category_id: int) -> list:
    """
    Args:
        category_id (int): 카테고리 PK
    Returns:
        list[dict]: 해당 카테고리의 퀴즈 목록
    Example:
        quizzes = quiz_db.get_quizzes_by_category(1)
    """
    pass

# 퀴즈용 랜덤 단어 목록 조회
def get_random_words_for_quiz(count: int = 10, category_id: int = None) -> list:
    """
    Args:
        count (int): 조회할 단어 수
        category_id (int, optional): 카테고리 PK
    Returns:
        list[dict]: 랜덤 단어 목록
    Example:
        words = quiz_db.get_random_words_for_quiz(5, 1)
    """
    pass

# 난이도별 단어 목록 조회
def get_words_by_difficulty(difficulty_level: int, count: int = 10) -> list:
    """
    Args:
        difficulty_level (int): 난이도 (wrong_count 기준)
        count (int): 조회할 단어 수
    Returns:
        list[dict]: 난이도별 단어 목록
    Example:
        words = quiz_db.get_words_by_difficulty(3, 5)
    """
    pass

# 퀴즈 결과 기록
def record_quiz_result(user_id: int, word_id: int, is_correct: bool) -> bool:
    """
    Args:
        user_id (int): 사용자 PK
        word_id (int): 단어 PK
        is_correct (bool): 정답 여부
    Returns:
        bool: 성공 여부
    Example:
        quiz_db.record_quiz_result(1, 2, True)
    """
    pass

# 사용자별 퀴즈 이력 조회
def get_user_quiz_history(user_id: int, limit: int = 50) -> list:
    """
    Args:
        user_id (int): 사용자 PK
        limit (int): 조회할 이력 수
    Returns:
        list[dict]: 퀴즈 이력 목록
    Example:
        history = quiz_db.get_user_quiz_history(1, 10)
    """
    pass

# 사용자 취약 단어 목록 조회
def get_user_weak_words(user_id: int, limit: int = 10) -> list:
    """
    Args:
        user_id (int): 사용자 PK
        limit (int): 조회할 단어 수
    Returns:
        list[dict]: 취약 단어 목록 (정답률 70% 미만)
    Example:
        weak_words = quiz_db.get_user_weak_words(1, 5)
    """
    pass

# 사용자 퀴즈 통계 조회
def get_quiz_statistics(user_id: int) -> dict:
    """
    Args:
        user_id (int): 사용자 PK
    Returns:
        dict: 퀴즈 통계 정보 (총 학습 단어 수, 시도 횟수, 정답 수, 정확도)
    Example:
        stats = quiz_db.get_quiz_statistics(1)
    """
    pass 
