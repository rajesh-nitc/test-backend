from fastapi import APIRouter, Depends
from vertexai.generative_models import GenerativeModel

from models.prompt import PromptRequest, PromptResponse
from services.vertex_ai import generate_model_response
from utils.vertex_ai import get_model

router = APIRouter()

history = []


@router.post("/prompt", response_model=PromptResponse)
async def get_prompt_response(
    request: PromptRequest, model: GenerativeModel = Depends(get_model)
):
    result = generate_model_response(request.prompt, model, history)
    return PromptResponse(response=result)
