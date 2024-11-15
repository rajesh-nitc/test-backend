from dotenv import load_dotenv

load_dotenv()
import logging
import os

import uvicorn
import vertexai
from fastapi import FastAPI

from config.logging import setup_logging
from routers import prompt

setup_logging()

logger = logging.getLogger(__name__)

app = FastAPI()

vertexai.init(project=os.getenv("PROJECT_ID"), location=os.getenv("REGION"))

app.include_router(prompt.router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
