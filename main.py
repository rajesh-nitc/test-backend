from dotenv import load_dotenv

load_dotenv()
import logging
import os

import vertexai
from fastapi import FastAPI

from config.logging import setup_logging
from routers import prompt

setup_logging()
logger = logging.getLogger(__name__)
logger.info(f"Use CPU cores for worker count: {os.cpu_count()}")

app = FastAPI()
logger.info("FastAPI app starting...")
logger.info(f"Running in {os.getenv('ENV', 'development')} mode.")
logger.info(f"App is bound to host: 0.0.0.0, port: 8000")

vertexai.init(project=os.getenv("PROJECT_ID"), location=os.getenv("REGION"))

app.include_router(prompt.router, prefix="/api/v1")
