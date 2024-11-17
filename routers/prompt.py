import os

from fastapi import APIRouter, Depends
from vertexai.generative_models import GenerationConfig, GenerativeModel

from models.prompt import PromptRequest, PromptResponse
from services.vertex_ai import generate_model_response
from tools.spend import spend_tool

router = APIRouter()


def get_model() -> GenerativeModel:
    """_summary_

    Raises:
        ValueError: _description_

    Returns:
        GenerativeModel: _description_
    """
    model_name = os.getenv("MODEL_NAME")
    if not model_name:
        raise ValueError("MODEL_NAME environment variable is not set.")
    return GenerativeModel(
        model_name,
        generation_config=GenerationConfig(temperature=0, candidate_count=1),
        tools=[spend_tool],
    )


@router.post("/prompt", response_model=PromptResponse)
async def get_prompt_response(
    request: PromptRequest, model: GenerativeModel = Depends(get_model)
):
    result = generate_model_response(request.prompt, model)
    return PromptResponse(response=result)
