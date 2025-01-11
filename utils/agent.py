from collections.abc import Callable
from typing import Any

from openai import AzureOpenAI
from pydantic import BaseModel
from vertexai.generative_models import (
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

    def get_client(self):
        """
        Initialize the GenerativeModel or OpenAI client.
        """
        if self.model.startswith("google"):
            # Google Gemini-specific setup
            safety_settings = {
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            }

            return GenerativeModel(
                self.model.split("/")[1],
                generation_config=GenerationConfig(
                    temperature=0,
                    candidate_count=1,
                    max_output_tokens=settings.LLM_MAX_OUTPUT_TOKENS,
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

            # Initialize the Azure OpenAI client
            client = AzureOpenAI(
                azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
                api_key=settings.AZURE_OPENAI_API_KEY,
                api_version="2024-02-01",
            )
            return client

        else:
            raise ValueError(f"Unsupported model type: {self.model}")
