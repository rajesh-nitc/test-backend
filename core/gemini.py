import logging
from typing import Any

from vertexai.generative_models import Part

from config.exceptions import (
    ModelResponseError,
    ProcessingFuncationCallsError,
    ResponseExtractionError,
)
from core.interface import ModelHandler
from functions.agent import FUNCTION_REGISTRY

logger = logging.getLogger(__name__)


class GeminiModelHandler(ModelHandler):
    def extract_function_calls(self, response) -> list[dict[str, Any]]:
        """
        Extract function calls from Model response
        """
        try:
            function_calls = []
            if response.candidates[0].function_calls:
                for function_call in response.candidates[0].function_calls:
                    function_call_dict: dict[str, Any] = {function_call.name: {}}
                    for key, value in function_call.args.items():
                        function_call_dict[function_call.name][key] = value
                    function_calls.append(function_call_dict)
                logger.info(f"Function calls: {function_calls}")
                return function_calls
            return []
        except Exception as e:
            logger.error(f"Error extracting function calls from response: {e}")
            raise ResponseExtractionError(
                "Failed to extract function calls from response."
            )

    def extract_text(self, response) -> str:
        """
        Extract text from Model response
        """
        try:
            if (
                response.candidates
                and response.candidates[0].content
                and response.candidates[0].content.parts
            ):
                part = response.candidates[0].content.parts[0]
                # Check if text exists in the part
                if hasattr(part, "text") and part.text:
                    return part.text
            return ""
        except Exception as e:
            logger.error(f"Error extracting text from response: {e}")
            raise ResponseExtractionError("Failed to extract text from response.")

    async def process_function_calls(self, function_calls: list[dict[str, Any]]):
        """
        Make api calls for the function calls and prepare the api response for the model
        """
        api_responses = []

        for function_call in function_calls:
            function_name, function_args = next(iter(function_call.items()))
            try:
                api_response = await FUNCTION_REGISTRY[function_name](function_args)
                api_responses.append(
                    Part.from_function_response(
                        name=function_name, response={"content": api_response}
                    )
                )
            except Exception as e:
                logger.error(f"Error processing function calls: {e}")
                raise ProcessingFuncationCallsError("Failed to process function calls.")

        return api_responses

    async def get_response(self, chat, api_responses):
        """
        This is not used for the inital response to prompt
        Feed api responses back to model
        """
        try:
            response = await chat.send_message_async(api_responses)  # type: ignore
            return response
        except Exception as e:
            logger.error(f"Error getting model response: {e}")
            raise ModelResponseError("Failed to get model response.")

    def get_role(self):
        return "model"
