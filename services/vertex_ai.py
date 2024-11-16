import logging

from vertexai.generative_models import GenerativeModel, Part

from services.mock_external_api import fetch_mock_data
from utils.genai import extract_function_calls, extract_text

logger = logging.getLogger(__name__)


def generate_model_response(prompt: str, model: GenerativeModel) -> str:
    """_summary_

    Args:
        prompt (str): _description_
        model (GenerativeModel): _description_

    Returns:
        str: _description_
    """
    chat = model.start_chat()
    response = chat.send_message(prompt)

    # Extract function calls from the model's response
    function_calls = extract_function_calls(response)

    if function_calls:
        for k, v in function_calls[0].items():
            logger.info(f"Type of v: {type(v)}")
            api_response = fetch_mock_data(v)
            response = chat.send_message(
                Part.from_function_response(
                    name=k,
                    response={
                        "content": api_response,
                    },
                ),
            )
        # After passing api_response to Model, return the model response
        return extract_text(response)

    else:
        # If there are no function calls, return the extracted text from the response
        return extract_text(response)
