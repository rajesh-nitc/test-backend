import logging

from vertexai.generative_models import GenerativeModel, Part

from config.exceptions import PromptExceededError, QuotaExceededError
from config.registry import FUNCTION_REGISTRY
from utils.gcs import get_same_day_chat_messages
from utils.llm import extract_function_calls, extract_text
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

    # Log response
    logger.info(f"Model response: {response}")

    # Function calling loop
    function_calling_in_process = True
    while function_calling_in_process:

        # Extract function calls
        function_calls = extract_function_calls(response)
        if function_calls:
            # Create a list to hold all the api responses
            api_responses = []

            for function_call in function_calls:
                function_name, function_args = next(iter(function_call.items()))
                logger.info(
                    f"function_name: {function_name}, function_args: {function_args}"
                )

                # Call the function handler and store the response
                api_response = await FUNCTION_REGISTRY[function_name](function_args)

                # Append api response
                api_responses.append(
                    Part.from_function_response(
                        name=function_name,
                        response={"content": api_response},
                    )
                )

            # Ensure the number of api responses match the number of function calls
            if len(api_responses) != len(function_calls):
                logger.error(
                    "Mismatch in the number of api responses and function calls."
                )
                raise ValueError(
                    "Mismatch in the number of api responses and function calls."
                )

            # Send all responses as a list of Part objects
            response = await chat.send_message_async(api_responses)

        else:
            function_calling_in_process = False
            response_final = extract_text(response)

    # Perform postchecks
    await postchecks(prompt, response_final, response, user_id)

    return response_final
