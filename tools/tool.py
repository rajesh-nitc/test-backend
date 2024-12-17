from vertexai.generative_models import Tool

from functions.spend_api import get_spend_func
from functions.toy_search import get_toys_func

tool = Tool(
    function_declarations=[get_spend_func, get_toys_func],
)
