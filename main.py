from dotenv import load_dotenv

load_dotenv()

import logging

import vertexai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.settings import settings
from routers import health, prompt

logger = logging.getLogger(__name__)

# Initialize the app
app = FastAPI(
    title=settings.APP_NAME,
    description=f"{settings.APP_NAME} with {settings.LLM_MODEL} and {settings.EMB_MODEL}.",
    version="1.0.0",
)

# Add Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Vertex AI SDK
vertexai.init(project=settings.GOOGLE_CLOUD_PROJECT, location=settings.REGION)

# Log startup configuration
logger.info("FastAPI app starting...")
logger.info(f"Running in {settings.ENV.capitalize()} mode.")
logger.info("App is bound to host: 0.0.0.0, port: 8000")

# Include Routers
app.include_router(prompt.router, prefix="/api", tags=["Prompt"])
app.include_router(health.router, prefix="/api", tags=["Health"])
