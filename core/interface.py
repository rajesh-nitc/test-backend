from abc import ABC, abstractmethod
from typing import Any

from functions.agent import Agent


class ModelHandler(ABC):
    def __init__(self, agent: Agent):
        self.agent = agent

    @abstractmethod
    async def get_response_to_prompt(self, prompt: str, history: list):
        pass

    @abstractmethod
    def extract_function_calls(self, response) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    async def process_function_calls(self, function_calls: list[dict[str, Any]]):
        pass

    @abstractmethod
    async def get_response_to_api_responses(self, api_responses):
        pass

    @abstractmethod
    def extract_text(self, response) -> str:
        pass

    @abstractmethod
    def get_role(self) -> str:
        pass
