from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = Field(..., env="APP_NAME")  # type: ignore
    EMB_BLOB: str = Field(..., env="EMB_BLOB")  # type: ignore
    EMB_BUCKET: str = Field(..., env="EMB_BUCKET")  # type: ignore
    EMB_DEPLOYED_INDEX_ID: str = Field(..., env="EMB_DEPLOYED_INDEX_ID")  # type: ignore
    EMB_DF_HEAD: int = Field(..., env="EMB_DF_HEAD")  # type: ignore
    EMB_DIMENSIONALITY: int = Field(..., env="EMB_DIMENSIONALITY")  # type: ignore
    EMB_INDEX_ENDPOINT: str = Field(..., env="EMB_INDEX_ENDPOINT")  # type: ignore
    EMB_MODEL: str = Field(..., env="EMB_MODEL")  # type: ignore
    EMB_TASK: str = Field(..., env="EMB_TASK")  # type: ignore
    EMB_TOP_K: int = Field(..., env="EMB_TOP_K")  # type: ignore
    ENV: str = Field(..., env="ENV")  # type: ignore
    GOOGLE_CLOUD_PROJECT: str = Field(..., env="GOOGLE_CLOUD_PROJECT")  # type: ignore
    LLM_BUCKET_FOLDER: str = Field(..., env="LLM_BUCKET_FOLDER")  # type: ignore
    LLM_BUCKET: str = Field(..., env="LLM_BUCKET")  # type: ignore
    LLM_MAX_TOKENS: int = Field(..., env="LLM_MAX_TOKENS")  # type: ignore
    LLM_MODEL: str = Field(..., env="LLM_MODEL")  # type: ignore
    LOG_LEVEL: str = Field(..., env="LOG_LEVEL")  # type: ignore
    REGION: str = Field(..., env="REGION")  # type: ignore

    class Config:
        env_file = ".env"


settings = Settings()  # type: ignore
