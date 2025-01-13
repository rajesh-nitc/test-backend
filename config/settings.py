from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings

from utils.text import dedent_and_strip


class Settings(BaseSettings):
    APP_NAME: str = Field(
        "genai-function-calling-api", description="Name of the application."
    )
    AZURE_OPENAI_API_KEY: str = Field(
        ...,  # Required field (this means it must be provided through env)
        json_schema_extra={"env": "AZURE_OPENAI_API_KEY"},
        description="Azure OpenAI API key.",
    )
    AZURE_OPENAI_ENDPOINT: str = Field(
        "https://oai-function-calling-api-02.openai.azure.com/",
        description="Azure OpenAI endpoint.",
    )
    EMB_BUCKET: str = Field(
        "bkt-bu1-d-function-calling-api-embedding",
        description="Bucket for storing embeddings JSON file.",
    )
    EMB_DEPLOYED_INDEX_ID: str = Field(
        "index_01_deploy_1734488317622", description="Vector search index ID."
    )
    EMB_INDEX_ENDPOINT: str = Field(
        "projects/770674777462/locations/us-central1/indexEndpoints/5963364040964046848",
        description="Vector search index endpoint.",
    )
    EMB_MODEL: Literal["text-embedding-004", "text-embedding-005"] = Field(
        "text-embedding-005", description="The text embedding Model to use."
    )
    EMB_TOP_K: int = Field(
        3,
        ge=1,
        description="Default top results to retrieve.",
    )
    ENV: Literal["local", "dev", "npr", "prd"] = Field(
        "local", description="Application environment."
    )
    GOOGLE_CLOUD_PROJECT: str = Field(
        "prj-bu1-d-sample-base-9208", description="The Google Cloud project ID."
    )
    HTTP_CLIENT_BASE_URL: str = Field(
        "https://api.openweathermap.org", description="OpenWeather API base url"
    )
    LLM_CHAT_BUCKET: str = Field(
        "bkt-bu1-d-function-calling-api-chat",
        description="Bucket for storing chat history.",
    )
    LLM_MODEL: Literal[
        "openai/gpt-4",
        "openai/gpt-4o",
        "openai/gpt-4o-mini",
        "google/gemini-1.5-pro",
        "google/gemini-1.5-flash",
        "google/gemini-2.0-flash-exp",
    ] = Field("google/gemini-2.0-flash-exp", description="The foundation model to use.")
    LLM_SYSTEM_INSTRUCTION: str = Field(
        dedent_and_strip(
            """
        Ask clarifying questions if not enough information is available.
        Don't explain what you are doing, just provide the result.
        """
        ),
        description="System instruction for the Model.",
    )
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        "INFO", description="Logging level."
    )
    OPENWEATHER_API_KEY: str = Field(
        ...,  # Required field (this means it must be provided through env)
        json_schema_extra={"env": "OPENWEATHER_API_KEY"},
        description="OpenWeather API key.",
    )
    REGION: Literal["us-central1"] = Field("us-central1", description="The GCP region.")


settings = Settings()  # type: ignore
