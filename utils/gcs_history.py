from google.cloud import storage

from config.settings import settings
from utils.date import get_today_date

LLM_BUCKET = settings.LLM_BUCKET
LLM_BUCKET_FOLDER = settings.LLM_BUCKET_FOLDER


def get_gcs_client():
    return storage.Client(project=settings.GOOGLE_CLOUD_PROJECT)


def get_chat_history_file_path(user_id: str) -> str:
    """
    Generate the GCS file path for the current day's chat history for the user.
    """
    today, _ = get_today_date()
    return f"{LLM_BUCKET_FOLDER}/{user_id}/{today}.txt"


def load_same_day_history(user_id: str) -> list:
    """
    Load the current day's chat history for the user from GCS.

    Args:
        user_id (str): Unique identifier for the user.

    Returns:
        list: List of chat history lines, or an empty list if no history exists.
    """
    client = get_gcs_client()
    bucket = client.bucket(LLM_BUCKET)
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
    bucket = client.bucket(LLM_BUCKET)
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


def extract_last_two_turns(history: list) -> list:
    """
    Extracts the last two user-model exchange pairs from the chat history, ignoring blank lines.

    Args:
        history (list): The chat history as a list of lines (each line being a user or model turn).

    Returns:
        list: The last two user-model exchanges in chronological order, excluding blank lines.
    """
    if not history:
        return []

    # Initialize a list to store the last two exchanges
    turns = []

    # We want to loop backwards and collect pairs (user, model), skipping blank lines
    for i in range(len(history) - 1, -1, -1):
        line = history[i].strip()  # Remove leading/trailing whitespace
        if line:  # Ignore blank lines
            turns.append(line)

        # If we've added 4 valid lines (2 user-model pairs), stop collecting
        if len(turns) == 4:
            break

    # Reverse the turns list to maintain the correct chronological order (oldest first)
    return turns[::-1]
