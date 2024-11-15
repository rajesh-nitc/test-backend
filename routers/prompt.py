import os

from fastapi import APIRouter, Depends
from vertexai.generative_models import GenerationConfig, GenerativeModel

from models.prompt import PromptRequest, PromptResponse
from services.vertex_ai import generate_model_response

router = APIRouter()


def get_model() -> GenerativeModel:
    model_name = os.getenv("MODEL_NAME")
    if not model_name:
        raise ValueError("MODEL_NAME environment variable is not set.")
    return GenerativeModel(
        model_name,
        generation_config=GenerationConfig(temperature=0),
    )


@router.post("/prompt", response_model=PromptResponse)
async def get_prompt_response(
    request: PromptRequest, model: GenerativeModel = Depends(get_model)
):
    # Call service function to generate response and handle function calls
    result = generate_model_response(request.prompt, model)

    # Response handling: Return the appropriate response
    if isinstance(result, list):  # This means we have function calls
        # Process function calls if needed
        return PromptResponse(response=result)
    else:
        # If it's just text, return it as the response
        return PromptResponse(response=result)
