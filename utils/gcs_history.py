import os
from datetime import datetime

from google.cloud import storage

from utils.date import get_today_date

BUCKET_NAME = os.getenv("BUCKET_NAME")
CHAT_HISTORY_FOLDER = os.getenv("CHAT_HISTORY_FOLDER")


def get_gcs_client():
    return storage.Client()


def get_chat_history_file_path(user_id: str) -> str:
    """
    Generate the GCS file path for the current day's chat history for the user.
    """
    today, _ = get_today_date()
    return f"{CHAT_HISTORY_FOLDER}/{user_id}/{today}.txt"


def load_same_day_history(user_id: str) -> list:
    """
    Load the current day's chat history for the user from GCS.

    Args:
        user_id (str): Unique identifier for the user.

    Returns:
        list: List of chat history lines, or an empty list if no history exists.
    """
    client = get_gcs_client()
    bucket = client.bucket(BUCKET_NAME)
    file_path = get_chat_history_file_path(user_id)

    blob = bucket.blob(file_path)
    if blob.exists():
        # Download and split the history into lines
        return blob.download_as_text().splitlines()
    return []


def append_chat_to_gcs(user_id: str, message: str):
    """
    Append a message to the current day's chat history for the user in GCS.

    Args:
        user_id (str): Unique identifier for the user.
        message (str): Message to append to the history.
    """
    client = get_gcs_client()
    bucket = client.bucket(BUCKET_NAME)
    file_path = get_chat_history_file_path(user_id)

    blob = bucket.blob(file_path)
    if blob.exists():
        # Append to existing file
        existing_data = blob.download_as_text()
        new_data = f"{existing_data}\n{message}"
    else:
        # Start a new file
        new_data = message

    # Upload the updated chat history
    blob.upload_from_string(new_data, content_type="text/plain")
