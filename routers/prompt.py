from fastapi import APIRouter, Depends

from config.agent import get_agent
from core.agent import Agent
from models.common.prompt import PromptRequest, PromptResponse
from services.common.llm import generate_model_response

router: APIRouter = APIRouter()


@router.post("/prompt", response_model=PromptResponse)
async def get_prompt_response(
    request: PromptRequest,
    agent: Agent = Depends(get_agent),
) -> PromptResponse:
    result = await generate_model_response(agent, request.prompt, request.user_id)
    return PromptResponse(response=result)
