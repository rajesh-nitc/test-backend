import logging

from vertexai.generative_models import GenerativeModel, Part

from config.exceptions import PromptExceededError, QuotaExceededError
from config.registry import FUNCTION_REGISTRY
from utils.gcs import get_same_day_chat_messages
from utils.llm import extract_function_call, extract_text
from utils.postchecks import postchecks
from utils.prechecks import prechecks

logger = logging.getLogger(__name__)


async def generate_model_response(
    prompt: str, model: GenerativeModel, user_id: str
) -> str:
    """
    Generate model response.
    """
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
    history = get_same_day_chat_messages(user_id)

    # Start a new chat session with history
    chat = model.start_chat(history=history)

    # Send new prompt to the model
    response = await chat.send_message_async(prompt)

    # Function calling loop
    function_calling_in_process = True
    while function_calling_in_process:

        function_call = extract_function_call(response)
        if function_call:
            function_name, function_args = next(iter(function_call.items()))
            logger.info(
                f"function_name: {function_name}, function_args: {function_args}"
            )

            # Call function handler from the registry
            api_response = await FUNCTION_REGISTRY[function_name](function_args)

            # Send api response back to the model
            response = await chat.send_message_async(
                Part.from_function_response(
                    name=function_name,
                    response={"content": api_response},
                )
            )

            # "response" could be a function call or text. Hence, the loop

        else:
            function_calling_in_process = False
            response_final = extract_text(response)

    # Perform postchecks
    await postchecks(prompt, response_final, response, user_id)

    return response_final
