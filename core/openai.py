import json
import logging
from typing import Any

from config.exceptions import (
    ModelResponseError,
    ProcessingFuncationCallsError,
    ResponseExtractionError,
)
from core.interface import ModelHandler
from functions.agent import FUNCTION_REGISTRY
from utils.schema import function_to_openai_schema

logger = logging.getLogger(__name__)


class OpenAIModelHandler(ModelHandler):
    def extract_function_calls(self, response) -> list[dict[str, Any]]:
        """
        Extract function calls from Model response
        """
        try:
            function_calls = []
            if (
                response.choices[0].message
                and hasattr(response.choices[0].message, "tool_calls")
                and response.choices[0].message.tool_calls is not None
            ):
                for function_call in response.choices[0].message.tool_calls:
                    function_name = function_call.function.name
                    function_args = json.loads(function_call.function.arguments)
                    function_calls.append({function_name: function_args})

                    self.agent.messages.append(  # type: ignore
                        {
                            "role": response.choices[0].message.role,
                            "function_call": {
                                "name": response.choices[0]
                                .message.tool_calls[0]
                                .function.name,
                                "arguments": response.choices[0]
                                .message.tool_calls[0]
                                .function.arguments,
                            },
                            "content": None,
                        }
                    )
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
            if response.choices[0].message.content is not None:
                return response.choices[0].message.content.strip()
            return ""
        except Exception as e:
            logger.error(f"Error extracting text from response: {e}")
            raise ResponseExtractionError("Failed to extract text from response.")

    async def process_function_calls(self, function_calls: list[dict[str, Any]]):
        """
        Make api calls for the function calls and prepare the api response for the model
        Api responses are appended to agent.messages. api_responses is not used.
        """
        api_responses: list[Any] = []

        for function_call in function_calls:
            function_name, function_args = next(iter(function_call.items()))
            try:
                api_response = await FUNCTION_REGISTRY[function_name](function_args)
                self.agent.messages.append(  # type: ignore
                    {
                        "role": "function",
                        "name": function_name,
                        "content": json.dumps(api_response),
                    }
                )
            except Exception as e:
                logger.error(f"Error processing function calls: {e}")
                raise ProcessingFuncationCallsError("Failed to process function calls.")

        return api_responses

    async def get_response(self, chat=None, api_responses=None):
        """
        Model response
        """
        try:
            response = self.agent.get_client().chat.completions.create(  # type: ignore
                model=self.agent.model.split("/")[1],  # type: ignore
                messages=self.agent.messages,  # type: ignore
                tools=[function_to_openai_schema(func) for func in self.agent.functions],  # type: ignore
                temperature=0,
                tool_choice="auto",
            )
            return response
        except Exception as e:
            logger.error(f"Error getting model response: {e}")
            raise ModelResponseError("Failed to get model response")

    def get_role(self):
        return "assistant"
