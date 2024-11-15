from typing import Any

from pydantic import BaseModel


class PromptRequest(BaseModel):
    prompt: str


class PromptResponse(BaseModel):
    response: Any
