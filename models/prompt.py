from pydantic import BaseModel
from typing import Any

class PromptRequest(BaseModel):
    prompt: str

class PromptResponse(BaseModel):
    response: Any