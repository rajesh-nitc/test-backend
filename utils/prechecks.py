import json

from vertexai.generative_models import GenerativeModel

from config.exceptions import PromptExceededError, QuotaExceededError
from config.settings import settings
from utils.gcs import get_file_path, get_gcs_client

LLM_CHAT_BUCKET = settings.LLM_CHAT_BUCKET
LLM_QUOTA_BUCKET = settings.LLM_QUOTA_BUCKET
LLM_QUOTA_TOKENS_LIMIT = settings.LLM_QUOTA_TOKENS_LIMIT
LLM_PROMPT_TOKENS_LIMIT = settings.LLM_PROMPT_TOKENS_LIMIT


async def prechecks(prompt: str, model: GenerativeModel, user_id: str) -> None:
    """
    Perform prechecks before prompt is passed to the Model.

    :param prompt: The prompt string.
    :param model: The generative model to use for counting tokens.
    :param user_id: The user ID.
    :raises QuotaExceededError: If the total token count exceeds the limit.
    :raises PromptExceededError: If the prompt token count exceeds the limit.
    """
    await check_quota(user_id, LLM_QUOTA_TOKENS_LIMIT)
    await check_prompt(prompt, model, user_id, LLM_PROMPT_TOKENS_LIMIT)


async def check_quota(user_id: str, quota_limit: int) -> None:
    """
    Check if the user's total token count exceeds the specified LLM Quota limit.

    :param user_id: The user ID.
    :param quota_limit: The maximum allowed token count.
    :raises QuotaExceededError: If the total token count exceeds the limit.
    """
    client = get_gcs_client()
    bucket = client.bucket(LLM_QUOTA_BUCKET)
    file_path = get_file_path(user_id)
    blob = bucket.blob(file_path)

    try:
        if blob.exists():
            # Load current quota usage
            data = json.loads(blob.download_as_text())
            total_token_count = data.get("total_token_count", 0)
        else:
            # If file doesn't exist, assume no usage
            total_token_count = 0
    except json.JSONDecodeError as e:
        print(f"Error decoding quota JSON for user {user_id}: {e}")
        total_token_count = 0  # Default to no usage on error

    # Check if the total token count exceeds the limit
    if total_token_count > quota_limit:
        raise QuotaExceededError(
            f"Quota exceeded for user {user_id}: {total_token_count} tokens used, "
            f"but the limit is {quota_limit}."
        )


async def check_prompt(
    prompt: str, model: GenerativeModel, user_id: str, prompt_limit: int
) -> None:
    """
    Check if the prompt's token count exceeds the specified LLM Prompt limit.

    :param prompt: The prompt string.
    :param model: The generative model to use for counting tokens.
    :param user_id: The user ID.
    :raises PromptExceededError: If the prompt token count exceeds the limit.
    """
    tokens_response = await model.count_tokens_async(prompt)
    tokens = tokens_response.total_tokens
    if tokens > prompt_limit:
        raise PromptExceededError(
            f"Prompt exceeded for user {user_id}: {tokens} tokens used, "
            f"but the limit is {prompt_limit}."
        )
