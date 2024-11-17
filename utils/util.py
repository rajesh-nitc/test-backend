import datetime
import logging
from typing import Tuple

from vertexai.generative_models import GenerationResponse

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

    logger.warning("No function call found in the response.")
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


def get_today_date() -> Tuple[datetime.date, str]:
    """_summary_

    Returns:
        Tuple[datetime.date, str]: _description_
    """
    today = datetime.date.today()
    # Return the full date (YYYY-MM-DD) and the day of the week
    return today, today.strftime("%A")
