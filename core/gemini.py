import logging
from typing import Any

from vertexai.generative_models import GenerationResponse, Part

from config.agent import FUNCTION_REGISTRY
from core.interface import ModelHandler

logger = logging.getLogger(__name__)


class GeminiModelHandler(ModelHandler):
    async def get_response_to_prompt(self, prompt, history) -> GenerationResponse:
        """
        Model response to prompt
        """
        try:
            self.agent.chat = self.agent.get_client().start_chat(history=history, response_validation=False)  # type: ignore
            return await self.agent.chat.send_message_async(prompt, stream=self.agent.stream)  # type: ignore
        except Exception as e:
            logger.error(f"Error getting model response to prompt: {e}")
            raise

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
            raise

    async def process_function_calls(
        self, function_calls: list[dict[str, Any]]
    ) -> list[Part]:
        """
        Make api calls for the function calls and add the responses to api_responses
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
                raise

        return api_responses

    async def get_response_to_api_responses(self, api_responses) -> GenerationResponse:
        """
        Model response to api responses
        """
        try:
            response = await self.agent.chat.send_message_async(api_responses, stream=self.agent.stream)  # type: ignore
            return response
        except Exception as e:
            logger.error(f"Error getting model response: {e}")
            raise

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
            raise

    def get_role(self) -> str:
        return "model"
