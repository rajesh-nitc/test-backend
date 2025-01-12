from abc import ABC, abstractmethod
from typing import Any

from functions.agent import Agent


class ModelHandler(ABC):
    def __init__(self, agent: Agent):
        self.agent = agent

    @abstractmethod
    def extract_function_calls(self, response) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    def extract_text(self, response) -> str:
        pass

    @abstractmethod
    async def process_function_calls(self, function_calls: list[dict[str, Any]]):
        pass

    @abstractmethod
    async def get_response(
        self, chat: Any | None = None, api_responses: list | None = None
    ):
        pass

    @abstractmethod
    def get_role(self):
        pass
