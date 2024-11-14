from typing import Any
import datetime
from vertexai.generative_models import (
    GenerationResponse,  
)
import logging
logger = logging.getLogger(__name__)

def extract_function_calls(response: GenerationResponse) -> list[dict]:
    function_calls: list[dict] = []
    if response.candidates[0].function_calls:
        for function_call in response.candidates[0].function_calls:
            function_call_dict: dict[str, dict[str, Any]] = {function_call.name: {}}
            for key, value in function_call.args.items():
                function_call_dict[function_call.name][key] = value
            function_calls.append(function_call_dict)
    logger.info(f"function_calls: {function_calls}")
    return function_calls

def extract_text(response: GenerationResponse):
    logger.info(f"Text: {response.candidates[0].content.parts[0].text}")
    return response.candidates[0].content.parts[0].text

def get_today_date():
    today = datetime.date.today()
    # Return the full date (YYYY-MM-DD) and the day of the week
    return today, today.strftime("%A")
