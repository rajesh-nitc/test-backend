import logging
from typing import Any

from vertexai.generative_models import GenerationResponse, Part

from config.exceptions import ResponseExtractionError
from functions.agent import FUNCTION_REGISTRY

logger = logging.getLogger(__name__)


def extract_function_calls(response: GenerationResponse) -> list[dict]:
    """
    Extracts function calls from the model's response.
    """
    try:
        function_calls = []
        if response.candidates[0].function_calls:
            for function_call in response.candidates[0].function_calls:
                function_call_dict: dict[str, Any] = {function_call.name: {}}
                for key, value in function_call.args.items():
                    function_call_dict[function_call.name][key] = value
                function_calls.append(function_call_dict)
            return function_calls
        else:
            return []
    except Exception as e:
        logger.error(f"Error extracting function call from response: {e}")
        raise ResponseExtractionError("Failed to extract function call from response.")


def extract_text(response: GenerationResponse) -> str:
    """
    Extracts text from the model's response.
    """
    try:
        # Ensure there's at least one candidate and one part in the content
        if (
            response.candidates
            and response.candidates[0].content
            and response.candidates[0].content.parts
        ):
            part = response.candidates[0].content.parts[0]
            # Check if text exists in the part
            if hasattr(part, "text") and part.text:
                text = part.text
                return text
            else:
                return ""
        else:
            logger.info("No valid content or parts in the response.")
            return ""
    except Exception as e:
        logger.error(f"Error extracting text from response: {e}")
        raise ResponseExtractionError("Failed to extract text from response.")


async def process_function_calls(function_calls):
    """
    Processes a list of function calls and returns their API responses.
    """
    api_responses = []

    for function_call in function_calls:
        function_name, function_args = next(iter(function_call.items()))
        try:
            # Call the API
            api_response = await FUNCTION_REGISTRY[function_name](function_args)
            api_responses.append(
                Part.from_function_response(
                    name=function_name,
                    response={"content": api_response},
                )
            )
        except Exception as e:
            logger.error(f"Error in {function_name}: {e}")
            api_responses.append(
                Part.from_function_response(
                    name=function_name,
                    response={"error": str(e)},
                )
            )

    # Check if number of function calls match the number of api responses
    if len(api_responses) != len(function_calls):
        logger.error(
            f"Mismatch: {len(api_responses)} api responses vs {len(function_calls)} function calls"
        )
        raise ValueError(
            "Number of function calls and number of api responses must match."
        )

    return api_responses
