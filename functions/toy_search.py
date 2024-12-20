from vertexai.generative_models import FunctionDeclaration

from config.settings import settings

DESCRIPTIONS = {
    "top_k": f"""
Identify number of toys or games from user queries.

Examples:
- "suggest toys": default to {settings.EMB_TOP_K} if not provided by user
- "recommend five indoor toys: 5
""",
    "operator": """
Identify the operator.

Examples:
- "indoor toys under $25": LESS
- "bicycles over $25: GREATER
""",
    "price": """
Identify the price from user queries.

Examples:
- "indoor toys under $25": 25
- "bicycles over ten dollars: 10
""",
    "query": """
Search query for the toy or game recommendations.
Examples:
- "suggest toys for a 7-year-old girl"
- "recommend five indoor toys"
""",
}

# Define the function declaration
get_toys_func = FunctionDeclaration(
    name="get_toys_func",
    description="Call this if the user is asking for information on toys or games",
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
                "type": "integer",
                "description": DESCRIPTIONS["price"],
                "nullable": True,
            },
        },
        "required": ["query"],
    },
)
