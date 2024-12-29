from fastapi import APIRouter, Depends
from vertexai.generative_models import GenerativeModel

from models.prompt import PromptRequest, PromptResponse
from services.vertex_ai_llm import generate_model_response
from utils.vertex_ai_llm import get_model

router: APIRouter = APIRouter()


@router.post("/prompt", response_model=PromptResponse)
async def get_prompt_response(
    request: PromptRequest,
    model: GenerativeModel = Depends(get_model),
) -> PromptResponse:
    result = await generate_model_response(request.prompt, model, request.user_id)
    return PromptResponse(response=result)
