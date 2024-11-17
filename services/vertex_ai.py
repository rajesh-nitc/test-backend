import logging

from vertexai.generative_models import GenerativeModel, Part

from services.mock_external_api import fetch_mock_data
from utils.genai import extract_function_call, extract_text

logger = logging.getLogger(__name__)


def generate_model_response(prompt: str, model: GenerativeModel) -> str:
    """
    Generates a response from the model based on the given prompt.

    Args:
        prompt (str): The input prompt.
        model (GenerativeModel): The generative model to use.

    Returns:
        str: The final model response.
    """
    chat = model.start_chat()
    response = chat.send_message(prompt)

    # Extract the single function call from the model's response
    function_call = extract_function_call(response)

    if function_call:
        function_name, function_args = next(iter(function_call.items()))
        logger.info(f"function_name: {function_name}, function_args: {function_args}")

        # Fetch mock data based on the function arguments
        api_response = fetch_mock_data(function_args)

        # Send the function response back to the model
        response = chat.send_message(
            Part.from_function_response(
                name=function_name,
                response={"content": api_response},
            )
        )
        # After sending the API response, return the text response from the model
        return extract_text(response)

    # If there is no function call, return the text from the initial response
    return extract_text(response)
