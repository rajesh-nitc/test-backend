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

    # Start a new chat session with history
    chat = model.start_chat(history=history)

    # Log input tokens and billable characters
    tokens_response = await model.count_tokens_async(chat.history or prompt)
    logger.info(f"total_tokens: {tokens_response.total_tokens}")
    logger.info(
        f"total_billable_characters: {tokens_response.total_billable_characters}"
    )

    # Send new prompt to the model
    response = await chat.send_message_async(prompt)

    function_calling_in_process = True
    while function_calling_in_process:
        function_call = extract_function_call(response)

        if function_call:
            function_name, function_args = next(iter(function_call.items()))
            logger.info(
                f"function_name: {function_name}, function_args: {function_args}"
            )

            # Call function from the registry
            if function_name in FUNCTION_REGISTRY:
                api_response = FUNCTION_REGISTRY[function_name](function_args)

            # Send api response back to the model
            response = await chat.send_message_async(
                Part.from_function_response(
                    name=function_name,
                    response={"content": api_response},
                )
            )

            # "response" could be a function call or text. Hence, the while loop

        else:
            function_calling_in_process = False
            response_final = extract_text(response)

    # Append message to the GCS chat history
    append_message_to_gcs(
        user_id=user_id, message=ChatMessage(role="user", content=prompt)
    )
    append_message_to_gcs(
        user_id=user_id, message=ChatMessage(role="model", content=response_final)
    )

    return response_final
