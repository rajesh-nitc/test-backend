from vertexai.generative_models import FunctionDeclaration

top_k_description = """
Identify number of toys, games or products from user queries.

Examples:
- "can you suggest couple of toys for a 7 year old?": 2
- "what are the top five products for kids?: 5
- "suggest some good toys": default to 5
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
        },
        "required": ["query", "top_k"],
    },
)
