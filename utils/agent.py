from collections.abc import Callable
from typing import Any

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
    functions: list[Callable[..., Any]]

    def get_model(self) -> GenerativeModel:
        """
        Initialize the GenerativeModel.
        """
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        }

        return GenerativeModel(
            self.model,
            generation_config=GenerationConfig(
                temperature=0,
                candidate_count=1,
                max_output_tokens=settings.LLM_MAX_OUTPUT_TOKENS,
            ),
            tools=[
                Tool(
                    function_declarations=[
                        FunctionDeclaration.from_func(i) for i in self.functions
                    ]
                )
            ],
            safety_settings=safety_settings,
            system_instruction=self.system_instruction,
        )
