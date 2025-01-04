import json
import logging

from google.cloud import storage
from vertexai.generative_models import Content, GenerationResponse, Part

from config.exceptions import GCSClientError, GCSFileError, QuotaUpdateError
from config.settings import settings
from models.common.chat import ChatMessage
from utils.date import get_today_date

LLM_CHAT_BUCKET = settings.LLM_CHAT_BUCKET
LLM_QUOTA_BUCKET = settings.LLM_QUOTA_BUCKET

logger = logging.getLogger(__name__)


def get_gcs_client() -> storage.Client:
    """
    Get a Google Cloud Storage client.
    """
    try:
        return storage.Client(project=settings.GOOGLE_CLOUD_PROJECT)
    except Exception as e:
        logger.error(f"Failed to initialize GCS client: {e}")
        raise GCSClientError("Failed to initialize GCS client.")


def get_file_path(user_id: str) -> str:
    """
    Generate the GCS file path for the current day's chat history for the user.
    """
    today, _ = get_today_date()
    return f"{user_id}/{today}.json"


def get_chat_messages(user_id: str) -> list[Content]:
    """
    Get the same day messages for the user.
    """
    try:
        client = get_gcs_client()
        bucket = client.bucket(LLM_CHAT_BUCKET)
        file_path = get_file_path(user_id)

        blob = bucket.blob(file_path)
        if blob.exists():
            messages = json.loads(blob.download_as_text())
            # Convert dicts to ChatMessage instances
            chat_messages = [ChatMessage(**msg) for msg in messages]
        else:
            chat_messages = []

        # Convert ChatMessage to Content objects
        contents = [
            Content(
                role=chat_message.role, parts=[Part.from_text(chat_message.content)]
            )
            for chat_message in chat_messages
        ]
        return contents
    except Exception as e:
        logger.error(f"Error fetching chat messages for user {user_id}: {e}")
        raise GCSFileError("Failed to fetch chat messages.")


def append_chat_message_to_gcs(user_id: str, message: ChatMessage) -> None:
    """
    Append a new message to the same day messages for the user.
    """
    try:
        client = get_gcs_client()
        bucket = client.bucket(LLM_CHAT_BUCKET)
        file_path = get_file_path(user_id)
        blob = bucket.blob(file_path)
        if blob.exists():
            # Download the existing file
            messages = json.loads(blob.download_as_text())
        else:
            # Start with an empty list if the file does not exist
            messages = []

        # Convert ChatMessage to dict and append
        messages.append(message.model_dump())

        # Upload the updated list back to GCS
        blob.upload_from_string(json.dumps(messages), content_type="application/json")
    except Exception as e:
        logger.error(f"Error appending chat message for user {user_id}: {e}")
        raise GCSFileError("Failed to append chat message.")


def update_quota_to_gcs(response: GenerationResponse, user_id: str) -> None:
    """
    Update quota after each Model response.
    """
    try:
        client = get_gcs_client()
        bucket = client.bucket(LLM_QUOTA_BUCKET)
        file_path = get_file_path(user_id)
        blob = bucket.blob(file_path)

        # Extract token counts from response
        usage_metadata = response.usage_metadata
        prompt_token_count = usage_metadata.prompt_token_count
        candidates_token_count = usage_metadata.candidates_token_count
        total_token_count = usage_metadata.total_token_count

        # Default quota structure
        default_quota = {
            "prompt_token_count": 0,
            "candidates_token_count": 0,
            "total_token_count": 0,
        }

        # Load existing quota if available
        if blob.exists():
            try:
                current_quota = json.loads(blob.download_as_text())
            except json.JSONDecodeError as e:
                print(f"Error decoding quota JSON for user {user_id}: {e}")
                current_quota = default_quota
        else:
            current_quota = default_quota

        # Update quota with new values
        current_quota["prompt_token_count"] += prompt_token_count
        current_quota["candidates_token_count"] += candidates_token_count
        current_quota["total_token_count"] += total_token_count

        # Save updated quota back to GCS
        blob.upload_from_string(
            json.dumps(current_quota), content_type="application/json"
        )
    except Exception as e:
        logger.error(f"Error updating quota for user {user_id}: {e}")
        raise QuotaUpdateError("Failed to update quota.")
