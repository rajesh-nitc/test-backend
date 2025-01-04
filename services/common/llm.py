import logging

from vertexai.generative_models import GenerativeModel

from config.exceptions import PromptExceededError, QuotaExceededError
from utils.gcs import get_chat_messages, update_quota_to_gcs
from utils.llm import extract_function_calls, extract_text, process_function_calls
from utils.postchecks import postchecks
from utils.prechecks import prechecks
from utils.text import dedent_and_strip

logger = logging.getLogger(__name__)


async def generate_model_response(
    prompt: str, model: GenerativeModel, user_id: str
) -> str:
    """
    Generate Model response.
    """
    prompt = dedent_and_strip(prompt)
    logger.info(f"Received prompt from user {user_id}: {prompt}")

    # Perform prechecks
    try:
        await prechecks(prompt, model, user_id)
    except QuotaExceededError as e:
        logger.error(f"Quota check failed for user {user_id}: {str(e)}")
        return f"Error: {str(e)}"
    except PromptExceededError as e:
        logger.error(f"Prompt check failed for user {user_id}: {str(e)}")
        return f"Error: {str(e)}"

    # Retrieve user's chat history for the same day
    history = get_chat_messages(user_id)

    # Start a new chat session with history
    chat = model.start_chat(history=history)

    # Send new prompt to Model
    response = await chat.send_message_async(prompt)

    # Update quota usage
    update_quota_to_gcs(response, user_id)

    # Log Model response to prompt
    logger.info(f"Model response to prompt: {response}")

    # Final Model response
    final_response = ""

    # Function calling loop
    function_calling_in_process = True
    while function_calling_in_process:

        function_calls = extract_function_calls(response)
        text_content = extract_text(response)

        # Case 1: Only Function Calls
        if function_calls and not text_content:
            logger.info("Case 1: Only function calls in Model response.")
            api_responses = await process_function_calls(function_calls)
            response = await chat.send_message_async(api_responses)
            logger.info(f"Case 1: Model response to api responses: {response}")
            update_quota_to_gcs(response, user_id)

        # Case 2: Function Calls and Text
        elif function_calls and text_content:
            logger.info("Case 2: Function calls and text in Model response.")
            api_responses = await process_function_calls(function_calls)
            response = await chat.send_message_async(api_responses)
            logger.info(f"Case 2: Model response to api responses: {response}")
            final_response += text_content
            update_quota_to_gcs(response, user_id)

        # Case 3: Only Text
        else:
            logger.info("Case 3: Only Text in Model response.")
            function_calling_in_process = False
            final_response += extract_text(response)

    # Perform postchecks
    await postchecks(prompt, final_response, user_id)

    return final_response
