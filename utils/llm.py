import logging

from vertexai.generative_models import (
    GenerationConfig,
    GenerationResponse,
    GenerativeModel,
    HarmBlockThreshold,
    HarmCategory,
)

from config.exceptions import ResponseExtractionError
from config.settings import settings
from tools.tool import tool

logger = logging.getLogger(__name__)


def get_model() -> GenerativeModel:
    """
    Initialize the GenerativeModel.
    candidate_count=1 is intentional.
    """
    LLM_MODEL = settings.LLM_MODEL
    if not LLM_MODEL:
        raise ValueError("LLM_MODEL environment variable is not set.")

    logger.info(f"Initializing GenerativeModel with LLM_MODEL: {LLM_MODEL}")

    safety_settings = {
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    }

    return GenerativeModel(
        LLM_MODEL,
        generation_config=GenerationConfig(
            temperature=0,
            candidate_count=1,
            max_output_tokens=settings.LLM_MAX_OUTPUT_TOKENS,
        ),
        tools=[tool],
        safety_settings=safety_settings,
        system_instruction=settings.SYSTEM_INSTRUCTION,
    )


def extract_function_call(response: GenerationResponse) -> dict:
    """
    Extracts function call from the model's response.
    """
    try:
        if response.candidates and response.candidates[0].function_calls:
            function_call = response.candidates[0].function_calls[0]
            function_call_dict = {function_call.name: dict(function_call.args)}
            return function_call_dict

        logger.info("No function call found in the model response.")
        return {}
    except Exception as e:
        logger.error(f"Error extracting function call from response: {e}")
        raise ResponseExtractionError("Failed to extract function call from response.")


def extract_text(response: GenerationResponse) -> str:
    """
    Extracts text from the model's response.
    """
    try:
        # Extract text from the model's response
        text = response.candidates[0].content.parts[0].text
        logger.info(f"Found text: {text}")

        return text
    except Exception as e:
        logger.error(f"Error extracting text from response: {e}")
        raise ResponseExtractionError("Failed to extract text from response.")
