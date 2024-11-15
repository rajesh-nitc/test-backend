from vertexai.generative_models import Tool

from function_declarations.spend import get_spend_func

spend_tool = Tool(
    function_declarations=[get_spend_func],
)
