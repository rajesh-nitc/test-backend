import json
import logging

from google.cloud import storage
from vertexai.generative_models import Content, Part

from config.exceptions import GCSClientError, GCSFileError
from config.settings import settings
from models.common.chat import ChatMessage
from utils.date import get_today_date

LLM_CHAT_BUCKET = settings.LLM_CHAT_BUCKET

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


def get_chat_messages(agent, user_id: str) -> list:
    """
    Get the same day messages for the user, formatted for the specified model type.

    :param user_id: The ID of the user.
    :param model_type: The type of model ('gemini' for Google Vertex AI, 'openai' for OpenAI).
    :return: A list of messages formatted for the specified model type.
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

        if agent.model.startswith("google"):
            # Convert ChatMessage to Content objects for Gemini
            contents = [
                Content(
                    role=chat_message.role, parts=[Part.from_text(chat_message.content)]
                )
                for chat_message in chat_messages
            ]
        elif agent.model.startswith("openai"):
            # Convert ChatMessage to simple dicts for OpenAI
            contents = [
                {"role": chat_message.role, "content": chat_message.content}
                for chat_message in chat_messages
            ]
        else:
            raise ValueError(f"Unsupported model type: {agent.model}")

        return contents

    except Exception as e:
        logger.error(f"Error fetching chat messages for user {user_id}: {e}")
        raise GCSFileError("Failed to fetch chat messages.")


def append_chat_message_to_gcs(agent, user_id: str, message: ChatMessage) -> None:
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

        messages.append(message.model_dump())

        # Upload the updated list back to GCS
        blob.upload_from_string(json.dumps(messages), content_type="application/json")
    except Exception as e:
        logger.error(f"Error appending chat message for user {user_id}: {e}")
        raise GCSFileError("Failed to append chat message.")
