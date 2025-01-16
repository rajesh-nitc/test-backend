from collections.abc import Callable
from typing import Any

import vertexai
from openai import AsyncAzureOpenAI
from pydantic import BaseModel
from vertexai.generative_models import (
    ChatSession,
    FunctionDeclaration,
    GenerationConfig,
    GenerativeModel,
    HarmBlockThreshold,
    HarmCategory,
    Tool,
)

from config.settings import settings


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

    def get_client(self):
        """
        Initialize the GenerativeModel or OpenAI client.
        """
        if self.model.startswith("google"):

            vertexai.init(
                project=settings.GOOGLE_CLOUD_PROJECT, location=settings.REGION
            )

            safety_settings = {
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            }

            return GenerativeModel(
                self.model.split("/")[1],
                generation_config=GenerationConfig(
                    temperature=self.temperature,
                    candidate_count=self.n,
                    max_output_tokens=self.max_tokens,
                    top_p=self.top_p,
                    seed=self.seed,
                ),
                tools=[
                    Tool(
                        function_declarations=[
                            FunctionDeclaration.from_func(func)
                            for func in self.functions
                        ]
                    )
                ],
                safety_settings=safety_settings,
                system_instruction=self.system_instruction,
            )
        elif self.model.startswith("openai"):

            return AsyncAzureOpenAI(
                azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
                api_key=settings.AZURE_OPENAI_API_KEY,
                api_version=self.api_version,
            )

        else:
            raise ValueError(f"Unsupported model type: {self.model}")
