from fastapi import APIRouter, Depends
from vertexai.generative_models import GenerativeModel

from models.common.prompt import PromptRequest, PromptResponse
from services.common.llm import generate_model_response
from utils.llm import get_model

router: APIRouter = APIRouter()


@router.post("/prompt", response_model=PromptResponse)
async def get_prompt_response(
    request: PromptRequest,
    model: GenerativeModel = Depends(get_model),
) -> PromptResponse:
    result = await generate_model_response(request.prompt, model, request.user_id)
    return PromptResponse(response=result)
