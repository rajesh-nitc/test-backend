from vertexai.generative_models import FunctionDeclaration

from config.settings import settings
from utils.text import dedent_and_strip

DESCRIPTIONS = {
    "FUNCTION": dedent_and_strip(
        f"""
Handles user queries related to toys, games, or recommendations for children
Extract query, top_k, operator, and price from user queries
Example usage:
    - Search toys for toddlers: query is full user query, top_k is {settings.EMB_TOP_K}, operator is None and price is None
    - Find five indoor games for kids: query is full user query, top_k is 5, operator is None and price is None
    - Recommend outdoor toys under $25: query is full user query, top_k is {settings.EMB_TOP_K}, operator is LESS and price is 25
    - toys: query is full user query, top_k is {settings.EMB_TOP_K}, operator is None and price is None
"""
    ),
    "top_k": dedent_and_strip(
        f"""
Number of toys or games to return in the response. Default value is {settings.EMB_TOP_K}
"""
    ),
    "operator": dedent_and_strip(
        """
Comparison operator for toy or game price
"""
    ),
    "price": dedent_and_strip(
        """
Price of the toy or game
"""
    ),
    "query": dedent_and_strip(
        """
User query for toys or games
"""
    ),
}

# Define the function declaration
search_toys_func = FunctionDeclaration(
    name="search_toys_func",
    description=DESCRIPTIONS["FUNCTION"],
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": DESCRIPTIONS["query"],
            },
            "top_k": {
                "type": "integer",
                "description": DESCRIPTIONS["top_k"],
                "nullable": True,
            },
            "operator": {
                "type": "string",
                "enum": ["LESS", "LESS_EQUAL", "EQUAL", "GREATER_EQUAL", "GREATER"],
                "description": DESCRIPTIONS["operator"],
                "nullable": True,
            },
            "price": {
                "type": "number",
                "description": DESCRIPTIONS["price"],
                "nullable": True,
            },
        },
        "required": ["query"],
    },
)
