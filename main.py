from dotenv import load_dotenv

load_dotenv()


import logging

import vertexai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.settings import settings
from routers import prompt

logger = logging.getLogger(__name__)

# Initialize the app
app = FastAPI(
    title="genai-function-calling-api",
    description=f"genai-function-calling-api with {settings.model_llm} and {settings.model_emb}.",
    version="1.0.0",
)

# Add Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins.split(","),  # Restrict origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Vertex AI SDK
vertexai.init(project=settings.google_cloud_project, location=settings.region)

# Log startup configuration
logger.info("FastAPI app starting...")
logger.info(f"Running in {settings.env} mode.")
logger.info("App is bound to host: 0.0.0.0, port: 8000")

# Include Routers
app.include_router(prompt.router, prefix="/api/v1", tags=["Prompt"])


# Health Check Route
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}
