"""
CategoryDB API 명세서 (실제 구현 기준)

- 카테고리 생성, 조회, 수정, 삭제, 단어-카테고리 관계 등 카테고리 관련 DB 함수 명세
"""

# 카테고리 생성
def create_category(user_id: int, category_name: str) -> int:
    """
    Args:
        user_id (int): 사용자 PK
        category_name (str): 카테고리명
    Returns:
        int: 생성된 카테고리 PK
    Example:
        category_id = category_db.create_category(1, '동물')
    """
    pass

# 사용자별 카테고리 목록 조회
def get_user_categories(user_id: int) -> list:
    """
    Args:
        user_id (int): 사용자 PK
    Returns:
        list[dict]: 해당 사용자의 카테고리 정보 리스트
    Example:
        categories = category_db.get_user_categories(1)
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
        category_db.delete_category(1)
    """
    pass

# 카테고리명 수정
def update_category(category_id: int, category_name: str) -> bool:
    """
    Args:
        category_id (int): 카테고리 PK
        category_name (str): 새 카테고리명
    Returns:
        bool: 성공 여부
    Example:
        category_db.update_category(1, '과일')
    """
    pass

# 단어를 카테고리에 추가
def add_word_to_category(category_id: int, word_id: int) -> bool:
    """
    Args:
        category_id (int): 카테고리 PK
        word_id (int): 단어 PK
    Returns:
        bool: 성공 여부
    Example:
        category_db.add_word_to_category(1, 2)
    """
    pass

# 카테고리에서 단어 제거
def remove_word_from_category(category_id: int, word_id: int) -> bool:
    """
    Args:
        category_id (int): 카테고리 PK
        word_id (int): 단어 PK
    Returns:
        bool: 성공 여부
    Example:
        category_db.remove_word_from_category(1, 2)
    """
    pass

# 카테고리에 속한 단어 목록 조회
def get_words_in_category(category_id: int) -> list:
    """
    Args:
        category_id (int): 카테고리 PK
    Returns:
        list[dict]: 해당 카테고리에 속한 단어 정보 리스트
    Example:
        words = category_db.get_words_in_category(1)
    """
    pass

# 단어가 속한 카테고리 목록 조회
def get_word_categories(word_id: int) -> list:
    """
    Args:
        word_id (int): 단어 PK
    Returns:
        list[dict]: 해당 단어가 속한 카테고리 정보 리스트
    Example:
        categories = category_db.get_word_categories(1)
    """
    pass

# 전체 카테고리 목록 조회 (단어 수 포함)
def get_all_categories() -> list:
    """
    Returns:
        list[dict]: 전체 카테고리 정보 리스트 (단어 수 포함)
    Example:
        categories = category_db.get_all_categories()
    """
    pass 
