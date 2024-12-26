from typing import Literal

from pydantic import BaseModel

Role = Literal["user", "model"]


class ChatMessage(BaseModel):
    role: Role
    content: str
