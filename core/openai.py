import json
import logging
from typing import Any

from openai import AsyncAzureOpenAI

from config.agent import FUNCTION_REGISTRY
from config.settings import settings
from core.interface import ModelHandler
from models.common.chat import ChatMessage
from utils.schema import function_to_openai_schema

logger = logging.getLogger(__name__)


class OpenAIModelHandler(ModelHandler):
    def _get_client(self):
        """
        Get client
        """
        return AsyncAzureOpenAI(
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            api_key=settings.AZURE_OPENAI_API_KEY,
            api_version=self.agent.api_version,
        )

    async def _get_model_response(self) -> Any:
        """
        Model response
        """
        try:
            response = await self._get_client().chat.completions.create(
                model=self.agent.model.split("/")[1],
                messages=self.agent.messages,  # type: ignore
                tools=[function_to_openai_schema(func) for func in self.agent.functions],  # type: ignore
                temperature=self.agent.temperature,
                n=self.agent.n,
                tool_choice=self.agent.tool_choice,  # type: ignore
                top_p=self.agent.top_p,
                seed=self.agent.seed,
            )
            return response
        except Exception:
            raise

    async def get_response_to_prompt(self, prompt, history):
        """
        Model response to prompt
        """
        try:
            self.agent.messages = []
            for message in history:
                self.agent.messages.append(
                    ChatMessage(role=message["role"], content=message["content"])
                )
            self.agent.messages.append(
                ChatMessage(role="system", content=self.agent.system_instruction)
            )
            self.agent.messages.append(ChatMessage(role="user", content=prompt))
            return await self._get_model_response()
        except Exception as e:
            logger.error(f"Error getting model response to prompt: {str(e)}")
            raise

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
            logger.error(f"Error extracting function calls from response: {str(e)}")
            raise

    async def process_function_calls(
        self, function_calls: list[dict[str, Any]]
    ) -> list[Any]:
        """
        Make api calls for the function calls
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
                logger.error(f"Error processing function calls: {str(e)}")
                raise

        return api_responses

    async def get_response_to_api_responses(self, api_responses):
        """
        Model response to api responses
        """
        try:
            return await self._get_model_response()
        except Exception as e:
            logger.error(f"Error getting model response to api responses: {e}")
            raise

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
            raise

    def get_role(self) -> str:
        """
        Returns assistant role
        """
        return "assistant"
