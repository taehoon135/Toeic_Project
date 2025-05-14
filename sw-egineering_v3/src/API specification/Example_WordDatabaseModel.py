"""
WordDB API 명세서 (실제 구현 기준)

- 단어 추가, 수정, 삭제, 검색, 카테고리 관리 등 단어장 관련 DB 함수 명세
"""

# CSV 파일에서 단어 데이터 임포트
def import_from_csv(csv_path: str) -> bool:
    """
    Args:
        csv_path (str): CSV 파일 경로
    Returns:
        bool: 성공 여부
    Example:
        success = word_db.import_from_csv('word_list.csv')
    """
    pass

# 전체 단어 목록 조회
def get_all_words() -> list:
    """
    Returns:
        list[dict]: 전체 단어 목록
    Example:
        words = word_db.get_all_words()
    """
    pass

# 카테고리별 단어 목록 조회
def get_words_by_category(category_id: int) -> list:
    """
    Args:
        category_id (int): 카테고리 PK
    Returns:
        list[dict]: 카테고리별 단어 목록
    Example:
        words = word_db.get_words_by_category(1)
    """
    pass

# 단어 상세 정보 조회
def get_word_details(word_id: int) -> dict:
    """
    Args:
        word_id (int): 단어 PK
    Returns:
        dict: 단어 상세 정보
    Example:
        word = word_db.get_word_details(1)
    """
    pass

# 오답 횟수 증가
def update_wrong_count(word_id: int) -> bool:
    """
    Args:
        word_id (int): 단어 PK
    Returns:
        bool: 성공 여부
    Example:
        success = word_db.update_wrong_count(1)
    """
    pass

# 단어 추가
def add_word(word: str, meaning: str, part_of_speech: str, example: str, category_id: int = None) -> int:
    """
    Args:
        word (str): 영어 단어
        meaning (str): 한글 의미
        part_of_speech (str): 품사
        example (str): 예문
        category_id (int, optional): 카테고리 PK
    Returns:
        int: 생성된 단어 PK
    Example:
        word_id = word_db.add_word('apple', '사과', 'noun', 'I ate an apple.', 1)
    """
    pass

# 단어 수정
def update_word(word_id: int, word: str, meaning: str, part_of_speech: str, example: str, category_id: int = None) -> bool:
    """
    Args:
        word_id (int): 단어 PK
        word (str): 영어 단어
        meaning (str): 한글 의미
        part_of_speech (str): 품사
        example (str): 예문
        category_id (int, optional): 카테고리 PK
    Returns:
        bool: 성공 여부
    Example:
        success = word_db.update_word(1, 'apple', '사과', 'noun', 'I ate an apple.', 1)
    """
    pass

# 단어 삭제
def delete_word(word_id: int) -> bool:
    """
    Args:
        word_id (int): 단어 PK
    Returns:
        bool: 성공 여부
    Example:
        success = word_db.delete_word(1)
    """
    pass

# 카테고리 추가
def add_category(name: str) -> int:
    """
    Args:
        name (str): 카테고리명
    Returns:
        int: 생성된 카테고리 PK
    Example:
        category_id = word_db.add_category('일상생활')
    """
    pass

# 전체 카테고리 목록 조회
def get_categories() -> list:
    """
    Returns:
        list[dict]: 전체 카테고리 목록
    Example:
        categories = word_db.get_categories()
    """
    pass

# 단어를 카테고리에 추가
def add_word_to_category(word_id: int, category_id: int) -> bool:
    """
    Args:
        word_id (int): 단어 PK
        category_id (int): 카테고리 PK
    Returns:
        bool: 성공 여부
    Example:
        success = word_db.add_word_to_category(1, 1)
    """
    pass

# 단어를 카테고리에서 제거
def remove_word_from_category(word_id: int, category_id: int) -> bool:
    """
    Args:
        word_id (int): 단어 PK
        category_id (int): 카테고리 PK
    Returns:
        bool: 성공 여부
    Example:
        success = word_db.remove_word_from_category(1, 1)
    """
    pass

# 단어 검색
def search_words(keyword: str) -> list:
    """
    Args:
        keyword (str): 검색어
    Returns:
        list[dict]: 검색된 단어 목록
    Example:
        words = word_db.search_words('apple')
    """
    pass

# 카테고리 삭제
def delete_category(category_id: int) -> bool:
    """
    Args:
        category_id (int): 카테고리 PK
    Returns:
        bool: 성공 여부
    Example:
        success = word_db.delete_category(1)
    """
    pass

# 오답 횟수 기준 단어 목록 조회
def get_words_by_wrong_count(min_wrong_count: int = 1) -> list:
    """
    Args:
        min_wrong_count (int): 최소 오답 횟수
    Returns:
        list[dict]: 오답 횟수 기준 단어 목록
    Example:
        words = word_db.get_words_by_wrong_count(3)
    """
    pass 
