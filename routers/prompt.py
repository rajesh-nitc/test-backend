from fastapi import APIRouter, Depends
from models.prompt import PromptRequest,PromptResponse
from services.vertex_ai import process_prompt
from vertexai.generative_models import (
    GenerationConfig,
    GenerativeModel,
)

import os
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
async def get_prompt_response(request: PromptRequest, model: GenerativeModel = Depends(get_model)):
    response_text = process_prompt(request.prompt, model)
    return PromptResponse(response=response_text)
