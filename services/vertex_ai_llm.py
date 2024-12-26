import logging

from vertexai.generative_models import GenerativeModel, Part

from config.registry import FUNCTION_REGISTRY
from models.chat_message import ChatMessage
from utils.gcs_history import append_message_to_gcs, load_same_day_messages
from utils.vertex_ai_llm import extract_function_call, extract_text

logger = logging.getLogger(__name__)


async def generate_model_response(
    prompt: str, model: GenerativeModel, user_id: str
) -> str:
    """
    Generate a response from the model given a user prompt.
    """
    logger.info(f"Received prompt from user {user_id}: {prompt}")

    # Retrieve user's chat history for the same day
    history = load_same_day_messages(user_id)

    # Log input tokens and billable characters
    tokens_response = await model.count_tokens_async(history or prompt)
    total_tokens = tokens_response.total_tokens
    total_billable_characters = tokens_response.total_billable_characters
    logger.info(f"total_tokens: {total_tokens}")
    logger.info(f"total_billable_characters: {total_billable_characters}")

    # Start a new chat session with history
    chat = model.start_chat(history=history)

    # Send new prompt to the model
    response = await chat.send_message_async(prompt)

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
        response = await chat.send_message_async(
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

    # Append message to the GCS chat history
    append_message_to_gcs(
        user_id=user_id, message=ChatMessage(role="user", content=prompt)
    )
    append_message_to_gcs(
        user_id=user_id, message=ChatMessage(role="model", content=model_response)
    )

    return model_response
