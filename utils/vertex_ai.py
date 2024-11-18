import logging

from vertexai.generative_models import GenerationResponse,GenerativeModel,GenerationConfig
from tools.spend import spend_tool
import os
logger = logging.getLogger(__name__)


def extract_function_call(response: GenerationResponse) -> dict:
    """
    Extracts a single function call and its arguments from the response.

    Args:
        response (GenerationResponse): The model's response.

    Returns:
        dict: A dictionary representing the function call and its arguments.
    """
    if response.candidates and response.candidates[0].function_calls:
        function_call = response.candidates[0].function_calls[0]
        function_call_dict = {function_call.name: dict(function_call.args)}
        logger.info(f"function_call_dict: {function_call_dict}")
        return function_call_dict

    logger.info("No function call found in the model response.")
    return {}


def extract_text(response: GenerationResponse) -> str:
    """_summary_

    Args:
        response (GenerationResponse): _description_

    Returns:
        str: _description_
    """
    logger.info(f"Text: {response.candidates[0].content.parts[0].text}")
    return response.candidates[0].content.parts[0].text




def get_model() -> GenerativeModel:
    """_summary_

    Raises:
        ValueError: _description_

    Returns:
        GenerativeModel: _description_
    """
    model_name = os.getenv("MODEL_NAME")
    if not model_name:
        raise ValueError("MODEL_NAME environment variable is not set.")
    return GenerativeModel(
        model_name,
        generation_config=GenerationConfig(temperature=0, candidate_count=1),
        tools=[spend_tool],
    )