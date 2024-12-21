import logging

from vertexai.generative_models import GenerativeModel, Part

from config.settings import settings
from services.function_registry import FUNCTION_REGISTRY
from utils.gcs_history import (
    append_chat_to_gcs,
    extract_last_two_turns,
    load_same_day_history,
)
from utils.vertex_ai_llm import (
    count_tokens_with_tiktoken,
    extract_function_call,
    extract_text,
)

logger = logging.getLogger(__name__)
LLM_MAX_INPUT_TOKENS = settings.LLM_MAX_INPUT_TOKENS


def generate_model_response(prompt: str, model: GenerativeModel, user_id: str) -> str:
    """
    Generates a response from the model based on the given prompt, maintains conversation history by user_id,
    and returns the final model response. Chat history is stored in a GCP bucket by day.

    Args:
        prompt (str): The input prompt.
        model (GenerativeModel): The generative model to use.
        user_id (str): The unique identifier for the user.

    Returns:
        str: The final model response.
    """
    logger.info(f"Received prompt from user {user_id}: {prompt}")

    # Count tokens in the prompt
    token_count = count_tokens_with_tiktoken(prompt)
    logger.info(f"Token count: {token_count}")
    if token_count > LLM_MAX_INPUT_TOKENS:
        return f"Oops! Your message has {token_count} tokens, but the limit is {LLM_MAX_INPUT_TOKENS}. Please try a shorter version."

    # Retrieve or initialize the user's chat history for the same day
    history = load_same_day_history(user_id)

    # Extract the last two turns (user-model pairs)
    last_two_turns = extract_last_two_turns(history)  # type: ignore

    # Log Last two turns
    logger.info(f"Last two turns: {last_two_turns}")

    # Combine elements in last_two_turns list into single string, with each element separated by newline char
    conversation = "\n".join(last_two_turns)

    # Add the current user prompt to the conversation
    conversation += f"\n{prompt}"

    # Log Conversation
    logger.info(f"Conversation: {conversation}")

    # Start a new chat session with the model
    chat = model.start_chat()

    # Send the conversation history and new prompt to the model
    response = chat.send_message(conversation)

    # Extract the function call or text from the model's response
    function_call = extract_function_call(response)

    if function_call:
        function_name, function_args = next(iter(function_call.items()))
        logger.info(f"function_name: {function_name}, function_args: {function_args}")

        # Fetch response using the appropriate function handler
        if function_name in FUNCTION_REGISTRY:
            api_response = FUNCTION_REGISTRY[function_name](function_args)
        else:
            raise ValueError(f"Unknown function called: {function_name}")

        # Send api response back to the model
        response = chat.send_message(
            Part.from_function_response(
                name=function_name,
                response={"content": api_response},
            )
        )

        # Extract the final text response from the model
        model_response = extract_text(response)

    else:
        # If there is no function call, extract the text from the initial response
        model_response = extract_text(response)

    # Store the updated history in GCP bucket
    append_chat_to_gcs(user_id, f"user: {prompt}")
    append_chat_to_gcs(user_id, f"model: {model_response}")

    return model_response
