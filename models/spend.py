from typing import Any, Optional

from pydantic import BaseModel


class MockExternalApiRequest(BaseModel):
    category: Optional[str] = None  # category can be None
    start_date: str
    end_date: str


class MockExternalApiResponse(BaseModel):
    response: Any
