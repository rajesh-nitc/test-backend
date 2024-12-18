import os

from vertexai.generative_models import FunctionDeclaration

top_k_description = f"""
Identify number of toys, games or products from user queries.

Examples:
- "can you suggest some toys for a 7 year old?": default to {os.getenv("DEFAULT_TOP_K")}
- "top five indoor toys for kids?: 5
"""

operator_description = """
Identify the operator

Examples:
- "indoor toys under $25": LESS
- "bicyles over $25: GREATER
"""

price_description = """
Identify the price from user queries.

Examples:
- "indoor toys under $25": 25
- "bicyles over ten dollars: 10
"""

# Define the function declaration
get_toys_func = FunctionDeclaration(
    name="get_toys_func",
    description="Call this if the user is asking for information on toys or games",
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query",
            },
            "top_k": {
                "type": "integer",
                "description": top_k_description,
            },
            "operator": {
                "type": "string",
                "enum": ["LESS", "LESS_EQUAL", "EQUAL", "GREATER_EQUAL", "GREATER"],
                "description": operator_description,
                "nullable": True,
            },
            "price": {
                "type": "integer",
                "description": price_description,
                "nullable": True,
            },
        },
        "required": ["query", "top_k"],
    },
)
