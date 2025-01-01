from typing import Any

from pydantic import BaseModel


class PromptRequest(BaseModel):
    prompt: str
    user_id: str


class PromptResponse(BaseModel):
    response: Any
