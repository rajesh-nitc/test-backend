from utils.text import dedent_and_strip

toys = dedent_and_strip(
    """
    Handles user queries related to toys, games, or recommendations for children
    Extract query, top_k, operator, and price from user queries
    Example usage:
    - Search toys for toddlers: query is full user query, top_k is None, operator is None and price is None
    - Find five indoor games for kids: query is full user query, top_k is 5, operator is None and price is None
    - Recommend outdoor toys under $25: query is full user query, top_k is None, operator is LESS and price is 25
"""
)
