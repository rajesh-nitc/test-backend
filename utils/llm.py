import json
import logging
from typing import Any

from vertexai.generative_models import Part

from config.exceptions import ResponseExtractionError
from functions.agent import FUNCTION_REGISTRY, Agent
from utils.schema import function_to_openai_schema

logger = logging.getLogger(__name__)


def extract_function_calls(agent: Agent, response) -> list[dict]:
    """
    Extracts function calls from the model's response, handling both Gemini and OpenAI models.
    """
    try:
        function_calls = []
        if agent.model.startswith("google"):
            if response.candidates[0].function_calls:
                for function_call in response.candidates[0].function_calls:
                    function_call_dict: dict[str, Any] = {function_call.name: {}}
                    for key, value in function_call.args.items():
                        function_call_dict[function_call.name][key] = value
                    function_calls.append(function_call_dict)
            else:
                return []
        elif agent.model.startswith("openai"):
            if (
                response.choices[0].message
                and hasattr(response.choices[0].message, "tool_calls")
                and response.choices[0].message.tool_calls is not None
            ):
                for function_call in response.choices[0].message.tool_calls:
                    function_name = function_call.function.name
                    function_args = json.loads(function_call.function.arguments)
                    function_calls.append({function_name: function_args})

                    agent.messages.append(
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
            else:
                return []
            logger.info(f"Function calls: {function_calls}")
        return function_calls
    except Exception as e:
        logger.error(f"Error extracting function calls from response: {e}")
        raise ResponseExtractionError("Failed to extract function calls from response.")


def extract_text(agent, response) -> str:
    """
    Extracts text from the model's response, handling both Gemini and OpenAI models.
    """
    try:
        if agent.model.startswith("google"):
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
        elif agent.model.startswith("openai"):
            if response.choices[0].message.content is not None:
                return response.choices[0].message.content.strip()
        return ""
    except Exception as e:
        logger.error(f"Error extracting text from response: {e}")
        raise ResponseExtractionError("Failed to extract text from response.")


async def process_function_calls(agent: Agent, function_calls: list[dict]):
    """
    Processes a list of function calls and returns their API responses, handling both Gemini and OpenAI models.
    """

    api_responses = []

    for function_call in function_calls:
        function_name, function_args = next(iter(function_call.items()))
        try:
            api_response = await FUNCTION_REGISTRY[function_name](function_args)
            if agent.model.startswith("google"):
                api_responses.append(
                    Part.from_function_response(
                        name=function_name, response={"content": api_response}
                    )
                )
            elif agent.model.startswith("openai"):
                agent.messages.append(
                    {
                        "role": "function",
                        "name": function_name,
                        "content": json.dumps(api_response),
                    }
                )
        except Exception as e:
            logger.error(f"Error in {function_name}: {e}")

    return api_responses


async def get_response(agent: Agent, chat, api_responses: list | None = None):
    """ """
    try:
        if agent.model.startswith("google"):
            response = await chat.send_message_async(api_responses)
        elif agent.model.startswith("openai"):
            response = agent.get_client().chat.completions.create(  # type: ignore
                model=agent.model.split("/")[1],
                messages=agent.messages,
                tools=[function_to_openai_schema(func) for func in agent.functions],  # type: ignore
                temperature=0,
                tool_choice="auto",
            )

        return response
    except Exception as e:
        logger.error(f"Error getting response: {e}")
        raise ResponseExtractionError("Failed to get response.")
