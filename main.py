from dotenv import load_dotenv

load_dotenv()

import logging
import os

import vertexai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import prompt

# Initialize logging
logger = logging.getLogger(__name__)

# Initialize the app
app = FastAPI(
    title="function-calling-api",
    description=f"An API leveraging Vertex AI with {os.getenv("MODEL_NAME")} model.",
    version="1.0.0",
)

# Add Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(
        ","
    ),  # Restrict origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Vertex AI SDK
vertexai.init(project=os.getenv("GOOGLE_CLOUD_PROJECT"), location=os.getenv("REGION"))

# Log startup configuration
logger.info("FastAPI app starting...")
logger.info(f"Running in {os.getenv('ENV', 'development')} mode.")
logger.info("App is bound to host: 0.0.0.0, port: 8000")

# Include Routers
app.include_router(prompt.router, prefix="/api/v1", tags=["Prompt"])


# Health Check Route
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}
