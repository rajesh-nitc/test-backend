import logging

from vertexai.generative_models import GenerativeModel

from utils.genai import extract_function_calls, extract_text

logger = logging.getLogger(__name__)


def generate_model_response(prompt: str, model: GenerativeModel) -> str:
    chat = model.start_chat()
    response = chat.send_message(prompt)

    # Extract function calls from the model's response
    function_calls = extract_function_calls(response)

    if function_calls:
        for k, v in function_calls[0].items():
            return v

    # If no function calls, return the extracted text from the response
    return extract_text(response)
