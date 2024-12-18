from typing import Any

from pydantic import BaseModel


class MockExternalApiRequest(BaseModel):
    category: str | None = None  # category can be None
    start_date: str
    end_date: str


class MockExternalApiResponse(BaseModel):
    response: Any
