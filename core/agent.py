from collections.abc import Callable
from typing import Any

from pydantic import BaseModel
from vertexai.generative_models import ChatSession


class Agent(BaseModel):
    name: str
    model: str
    system_instruction: str
    messages: list = []
    functions: list[Callable[..., Any]]
    chat: ChatSession | None = None
    temperature: float = 0
    n: int = 1
    max_tokens: int = 125
    top_p: float = 1.0
    seed: int = 25
    tool_choice: str = "auto"
    api_version: str = "2024-02-01"

    class Config:
        arbitrary_types_allowed = True
