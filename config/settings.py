from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = Field(..., env="APP_NAME")  # type: ignore
    blob_name: str = Field(..., env="BLOB_NAME")  # type: ignore
    bucket_chat: str = Field(..., env="BUCKET_CHAT")  # type: ignore
    bucket_emb: str = Field(..., env="BUCKET_EMB")  # type: ignore
    chat_history_folder: str = Field(..., env="CHAT_HISTORY_FOLDER")  # type: ignore
    default_top_k: int = Field(..., env="DEFAULT_TOP_K")  # type: ignore
    deployed_index_id: str = Field(..., env="DEPLOYED_INDEX_ID")  # type: ignore
    df_head: int = Field(..., env="DF_HEAD")  # type: ignore
    dimensionality: int = Field(..., env="DIMENSIONALITY")  # type: ignore
    env: str = Field(..., env="ENV")  # type: ignore
    google_cloud_project: str = Field(..., env="GOOGLE_CLOUD_PROJECT")  # type: ignore
    index_endpoint: str = Field(..., env="INDEX_ENDPOINT")  # type: ignore
    log_level: str = Field(..., env="LOG_LEVEL")  # type: ignore
    max_tokens: int = Field(..., env="MAX_TOKENS")  # type: ignore
    model_emb: str = Field(..., env="MODEL_EMB")  # type: ignore
    model_llm: str = Field(..., env="MODEL_LLM")  # type: ignore
    region: str = Field(..., env="REGION")  # type: ignore
    task: str = Field(..., env="TASK")  # type: ignore

    class Config:
        env_file = ".env"


settings = Settings()  # type: ignore
