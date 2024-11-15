import logging
from typing import Any

from vertexai.generative_models import GenerativeModel

from tools.spend import spend_tool
from utils.util import extract_function_calls, extract_text

logger = logging.getLogger(__name__)


def generate_model_response(prompt: str, model: GenerativeModel) -> str:
    # Generate content with the model
    response = model.generate_content(
        prompt,
        tools=[spend_tool],
    )

    # Extract function calls from the model's response
    function_calls = extract_function_calls(response)

    if function_calls:
        # Iterate through the list of function calls
        for item in function_calls:
            for k, v in item.items():
                if k == "get_spend_func":
                    return v

    # If no function calls, return the extracted text from the response
    return extract_text(response)
