import datetime
import logging
from typing import Any, Tuple

from vertexai.generative_models import GenerationResponse

logger = logging.getLogger(__name__)


def extract_function_calls(response: GenerationResponse) -> list[dict]:
    """_summary_

    Args:
        response (GenerationResponse): _description_

    Returns:
        list[dict]: _description_
    """
    function_calls: list[dict] = []
    if response.candidates[0].function_calls:
        for function_call in response.candidates[0].function_calls:
            function_call_dict: dict[str, dict[str, Any]] = {function_call.name: {}}
            for key, value in function_call.args.items():
                function_call_dict[function_call.name][key] = value
            function_calls.append(function_call_dict)
    logger.info(f"function_calls: {function_calls}")
    return function_calls


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
