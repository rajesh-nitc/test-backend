from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = Field(
        "genai-function-calling-api", description="The name of the application."
    )
    EMB_BLOB: str = Field(
        "product_embeddings.json", description="Path to the embeddings blob file."
    )
    EMB_BUCKET: str = Field(
        "bkt-bu1-d-function-calling-api-embedding",
        description="Bucket for storing embeddings.",
    )
    EMB_DEPLOYED_INDEX_ID: str = Field(
        "index_01_deploy_1734488317622", description="Deployed index ID for embeddings."
    )
    EMB_DF_HEAD: int = Field(100, ge=1, description="To avoid quota exceeded error.")
    EMB_DIMENSIONALITY: int = Field(
        768, ge=1, description="Dimensionality of the embeddings."
    )
    EMB_INDEX_ENDPOINT: str = Field(
        "projects/770674777462/locations/asia-south1/indexEndpoints/5963364040964046848",
        description="Endpoint for the embeddings index.",
    )
    EMB_MODEL: str = Field(
        "text-embedding-005", description="The embedding model to use."
    )
    EMB_TASK: str = Field(
        "RETRIEVAL_DOCUMENT", description="The task for which the embeddings are used."
    )
    EMB_TOP_K: int = Field(
        3,
        ge=1,
        description="The number of top results to retrieve from the embeddings.",
    )
    ENV: str = Field("local", description="The environment (local, dev, prod).")
    GOOGLE_CLOUD_PROJECT: str = Field(
        "prj-bu1-d-sample-base-9208", description="The Google Cloud project ID."
    )
    LLM_BUCKET: str = Field(
        "bkt-bu1-d-function-calling-api-chat",
        description="Bucket for storing language model chat histories.",
    )
    LLM_BUCKET_FOLDER: str = Field(
        "chat_histories", description="Folder within the LLM bucket."
    )
    LLM_MAX_OUTPUT_TOKENS: int = Field(
        100, le=100, description="Maximum number of output tokens for the LLM."
    )
    LLM_MODEL: str = Field("gemini-1.5-pro", description="The language model to use.")
    LOG_LEVEL: str = Field("INFO", description="Logging level.")
    REGION: str = Field(
        "asia-south1", description="The region where the service is hosted."
    )
    SYSTEM_INSTRUCTION: str = Field(
        """
        Ask clarifying questions if not enough information is available.
        """,
        description="System instruction for the model.",
    )


settings = Settings()  # type: ignore
