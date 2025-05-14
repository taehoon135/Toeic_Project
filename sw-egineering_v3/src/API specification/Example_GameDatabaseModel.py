"""
GameDB API 명세서 (실제 구현 기준)

- 게임 점수 저장, 조회, 통계, 랭킹 등 게임 관련 DB 함수 명세
"""

# 게임 점수 저장
def save_score(user_id: int, game_type: str, score: int) -> bool:
    """
    Args:
        user_id (int): 사용자 PK
        game_type (str): 게임 유형
        score (int): 점수
    Returns:
        bool: 성공 여부
    Example:
        game_db.save_score(1, 'word_rain', 100)
    """
    pass

# 사용자별 게임 점수 목록 조회
def get_user_scores(user_id: int, game_type: str = None) -> list:
    """
    Args:
        user_id (int): 사용자 PK
        game_type (str, optional): 게임 유형
    Returns:
        list[dict]: 사용자의 게임 점수 목록
    Example:
        scores = game_db.get_user_scores(1, 'word_rain')
    """
    pass

# 게임별 최고 점수(랭킹) 조회
def get_high_scores(game_type: str, limit: int = 10) -> list:
    """
    Args:
        game_type (str): 게임 유형
        limit (int): 조회할 랭킹 수
    Returns:
        list[dict]: 게임별 최고 점수 랭킹
    Example:
        rankings = game_db.get_high_scores('word_rain', 5)
    """
    pass

# 사용자별 게임 통계 조회
def get_user_statistics(user_id: int) -> dict:
    """
    Args:
        user_id (int): 사용자 PK
    Returns:
        dict: 게임 통계 정보 (총 게임 수, 평균 점수, 최고 점수, 게임별 통계)
    Example:
        stats = game_db.get_user_statistics(1)
    """
    pass

# 사용자별 게임 점수 전체 삭제
def delete_user_scores(user_id: int) -> bool:
    """
    Args:
        user_id (int): 사용자 PK
    Returns:
        bool: 성공 여부
    Example:
        game_db.delete_user_scores(1)
    """
    pass 
