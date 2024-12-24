from vertexai.generative_models import Tool

from functions.api_spend import get_spend_func
from functions.search_toys import search_toys_func

tool = Tool(
    function_declarations=[get_spend_func, search_toys_func],
)
