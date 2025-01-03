import logging

from vertexai.generative_models import GenerationResponse

from config.exceptions import GCSFileError, QuotaUpdateError
from models.common.chat import ChatMessage
from utils.gcs import append_chat_message_to_gcs, update_quota_to_gcs

logger = logging.getLogger(__name__)


async def postchecks(
    prompt: str, final_response: str, response: GenerationResponse, user_id: str
) -> None:
    """
    Perform postchecks after the response is generated.

    :param prompt: The prompt string.
    :param final_response: The final response content.
    :param response: The full response object from the model.
    :param user_id: The user ID.
    """
    try:
        # Append user and model messages to GCS chat history
        append_chat_message_to_gcs(
            user_id=user_id, message=ChatMessage(role="user", content=prompt)
        )
        append_chat_message_to_gcs(
            user_id=user_id, message=ChatMessage(role="model", content=final_response)
        )
    except GCSFileError as e:
        logger.error(f"Failed to append chat messages for user {user_id}: {e}")
        raise

    try:
        # Update quota usage in GCS
        update_quota_to_gcs(response, user_id)
    except QuotaUpdateError as e:
        logger.error(f"Failed to update quota for user {user_id}: {e}")
        raise
