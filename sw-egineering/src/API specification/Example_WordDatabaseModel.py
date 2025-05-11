"""
WordDB API 명세서 (실제 구현 기준)

- 단어 등록, 조회, 수정, 삭제, 카테고리 관리 등 단어 관련 DB 함수 명세
"""

# CSV 파일에서 단어 데이터 임포트
def import_from_csv(csv_path: str) -> bool:
    """
    Args:
        csv_path (str): CSV 파일 경로
    Returns:
        bool: 성공 여부
    Example:
        word_db.import_from_csv('words.csv')
    """
    pass

# 전체 단어 목록 조회
def get_all_words() -> list:
    """
    Returns:
        list[dict]: 전체 단어 정보 리스트
    Example:
        words = word_db.get_all_words()
    """
    pass

# 카테고리별 단어 목록 조회
def get_words(category_id: int = None) -> list:
    """
    Args:
        category_id (int, optional): 카테고리 PK
    Returns:
        list[dict]: 해당 카테고리의 단어 정보 리스트
    Example:
        words = word_db.get_words(1)
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

# 오답 횟수 1 증가
def update_wrong_count(word_id: int) -> bool:
    """
    Args:
        word_id (int): 단어 PK
    Returns:
        bool: 성공 여부
    Example:
        word_db.update_wrong_count(1)
    """
    pass

# 단어 추가
def add_word(word: str, meaning: str, part_of_speech: str, example: str, category_id: int = None) -> int:
    """
    Args:
        word (str): 영어 단어
        meaning (str): 뜻
        part_of_speech (str): 품사
        example (str): 예문
        category_id (int, optional): 카테고리 PK
    Returns:
        int: 생성된 단어 PK
    Example:
        word_id = word_db.add_word('apple', '사과', '명사', 'I ate an apple.', 1)
    """
    pass

# 단어 수정
def update_word(word_id: int, word: str, meaning: str, part_of_speech: str, example: str, category_id: int = None) -> bool:
    """
    Args:
        word_id (int): 단어 PK
        word (str): 영어 단어
        meaning (str): 뜻
        part_of_speech (str): 품사
        example (str): 예문
        category_id (int, optional): 카테고리 PK
    Returns:
        bool: 성공 여부
    Example:
        word_db.update_word(1, 'apple', '사과', '명사', 'I ate an apple.', 1)
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
        word_db.delete_word(1)
    """
    pass

# 카테고리 추가
def add_category(name: str) -> bool:
    """
    Args:
        name (str): 카테고리명
    Returns:
        bool: 성공 여부
    Example:
        word_db.add_category('동물')
    """
    pass

# 전체 카테고리 목록 조회
def get_categories() -> list:
    """
    Returns:
        list[dict]: 전체 카테고리 정보 리스트
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
        word_db.add_word_to_category(1, 2)
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
        word_db.remove_word_from_category(1, 2)
    """
    pass

# 단어 검색 (영어/한글)
def search_words(keyword):
    """
    Args:
        keyword (str): 검색어
    Returns:
        list: 검색 결과 리스트
    Example:
        result = word_db.search_words('apple')
    """
    pass 