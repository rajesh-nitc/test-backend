import logging
import os

import vertexai
from dotenv import load_dotenv
from fastapi import FastAPI

from config.logging import setup_logging
from routers import prompt

load_dotenv()


setup_logging()
logger = logging.getLogger(__name__)
logger.info(f"Use CPU cores for worker count: {os.cpu_count()}")

app = FastAPI()
logger.info("FastAPI app starting...")
logger.info(f"Running in {os.getenv('ENV', 'development')} mode.")
logger.info("App is bound to host: 0.0.0.0, port: 8000")

vertexai.init(project=os.getenv("PROJECT_ID"), location=os.getenv("REGION"))

app.include_router(prompt.router, prefix="/api/v1")
