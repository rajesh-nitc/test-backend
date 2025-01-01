from typing import Literal

from pydantic import BaseModel


class SearchToysApiRequestData(BaseModel):
    top_k: int | None = None
    operator: (
        Literal["LESS", "LESS_EQUAL", "EQUAL", "GREATER_EQUAL", "GREATER"] | None
    ) = None
    price: float | None = None
    query: str
