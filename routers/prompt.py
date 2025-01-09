from fastapi import APIRouter, Depends

from functions.registry import get_agent
from models.common.prompt import PromptRequest, PromptResponse
from services.common.llm import generate_model_response
from utils.agent import Agent

router: APIRouter = APIRouter()


@router.post("/prompt", response_model=PromptResponse)
async def get_prompt_response(
    request: PromptRequest,
    agent: Agent = Depends(get_agent),
) -> PromptResponse:
    result = await generate_model_response(request.prompt, agent, request.user_id)
    return PromptResponse(response=result)
