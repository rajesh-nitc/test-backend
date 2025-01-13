import logging

from core.factory import get_model_handler
from models.common.chat import ChatMessage
from utils.agent import Agent
from utils.gcs import append_chat_message_to_gcs, get_chat_messages
from utils.text import dedent_and_strip

logger = logging.getLogger(__name__)


async def generate_model_response(agent: Agent, prompt: str, user_id: str) -> str:
    """
    Generate final Model response.
    """
    # Get Model handler
    handler = get_model_handler(agent)

    # Log received prompt
    prompt = dedent_and_strip(prompt)
    logger.info(f"Received prompt from user {user_id}: {prompt}")

    # Get user's chat history
    history = get_chat_messages(agent, user_id)

    # Model response to prompt
    try:
        response = await handler.get_response_to_prompt(prompt, history)
        logger.info(f"Model response to prompt: {response}")
    except Exception as e:
        return str(e)

    # Final Model response
    final_response = ""

    # Function calling loop
    function_calling_in_process = True
    while function_calling_in_process:

        function_calls = handler.extract_function_calls(response)
        text_content = handler.extract_text(response)

        # Case 1: Only Function Calls
        if function_calls and not text_content:
            logger.info("Case 1: Only function calls in Model response.")
            api_responses = await handler.process_function_calls(function_calls)
            response = await handler.get_response_to_api_responses(api_responses)
            logger.info(f"Case 1: Model response to api responses: {response}")

        # Case 2: Function Calls and Text
        elif function_calls and text_content:
            logger.info("Case 2: Function calls and text in Model response.")
            api_responses = await handler.process_function_calls(function_calls)
            response = await handler.get_response_to_api_responses(api_responses)
            logger.info(f"Case 2: Model response to api responses: {response}")
            final_response += text_content

        # Case 3: Only Text
        else:
            logger.info("Case 3: Only Text in Model response.")
            function_calling_in_process = False
            final_response += handler.extract_text(response)

    # Add chat to gcs
    try:
        append_chat_message_to_gcs(user_id, ChatMessage(role="user", content=prompt))
        append_chat_message_to_gcs(
            user_id, ChatMessage(role=handler.get_role(), content=final_response)  # type: ignore
        )
    except Exception as e:
        return str(e)

    return final_response
