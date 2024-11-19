import logging

from vertexai.generative_models import GenerativeModel, Part

from services.mock_external_api import fetch_mock_data
from utils.dict import user_chat_histories
from utils.vertex_ai import extract_function_call, extract_text

logger = logging.getLogger(__name__)


def generate_model_response(prompt: str, model: GenerativeModel, user_id: str) -> str:
    """
    Generates a response from the model based on the given prompt, maintains conversation history by user_id,
    and returns the final model response.

    Args:
        prompt (str): The input prompt.
        model (GenerativeModel): The generative model to use.
        user_id (str): The unique identifier for the user.

    Returns:
        str: The final model response.
    """
    logger.info(f"***** Received new prompt from user {user_id}: {prompt} *****")

    # Retrieve or initialize the user's chat history
    if user_id not in user_chat_histories:
        user_chat_histories[user_id] = []

    history = user_chat_histories[user_id]

    chat = model.start_chat()

    # Construct the full conversation context from the history
    conversation = ""
    for entry in history:
        conversation += f"{entry}\n"  # Each entry is a user or model response

    # Add the current user prompt to the conversation
    conversation += f"user: {prompt}\nmodel:"

    logger.info(f"===== Conversation: {conversation} =====")

    history.append(f"user: {prompt}")

    # Send the conversation history and new prompt to the model
    response = chat.send_message(conversation)

    # Extract the function call or text from the model's response
    function_call = extract_function_call(response)

    if function_call:
        function_name, function_args = next(iter(function_call.items()))
        logger.info(f"function_name: {function_name}, function_args: {function_args}")

        # Fetch mock data based on the function arguments
        api_response = fetch_mock_data(function_args)

        # Send the function response back to the model
        response = chat.send_message(
            Part.from_function_response(
                name=function_name,
                response={"content": api_response},
            )
        )
        # After sending the API response, return the text response from the model
        return extract_text(response, user_id)

    # If there is no function call, return the text from the initial response
    return extract_text(response, user_id)
