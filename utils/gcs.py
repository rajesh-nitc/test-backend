import json

from google.cloud import storage
from vertexai.generative_models import Content, Part

from config.settings import settings
from models.common.chat_message import ChatMessage
from utils.date import get_today_date

LLM_BUCKET = settings.LLM_BUCKET
LLM_BUCKET_FOLDER = settings.LLM_BUCKET_FOLDER


def get_gcs_client() -> storage.Client:
    """
    Get a Google Cloud Storage client.
    """
    return storage.Client(project=settings.GOOGLE_CLOUD_PROJECT)


def get_chat_history_file_path(user_id: str) -> str:
    """
    Generate the GCS file path for the current day's chat history for the user.
    """
    today, _ = get_today_date()
    return f"{LLM_BUCKET_FOLDER}/{user_id}/{today}.json"


def load_same_day_messages(user_id: str) -> list[Content]:
    """
    Load the same day messages for the user.
    """
    client = get_gcs_client()
    bucket = client.bucket(LLM_BUCKET)
    file_path = get_chat_history_file_path(user_id)

    blob = bucket.blob(file_path)
    if blob.exists():
        messages = json.loads(blob.download_as_text())
        # Convert dicts to ChatMessage instances
        chat_messages = [ChatMessage(**msg) for msg in messages]
    else:
        chat_messages = []

    # Convert ChatMessage to Content objects
    contents = [
        Content(role=chat_message.role, parts=[Part.from_text(chat_message.content)])
        for chat_message in chat_messages
    ]
    return contents


def append_message_to_gcs(user_id: str, message: ChatMessage) -> None:
    """
    Append a new message to the same day messages for the user.
    """
    client = get_gcs_client()
    bucket = client.bucket(LLM_BUCKET)
    file_path = get_chat_history_file_path(user_id)
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
