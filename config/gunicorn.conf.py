import logging
import os

from config.logging import setup_logging
from config.settings import settings

ENV = settings.ENV

# Set up logging
setup_logging(settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

# Gunicorn configuration
bind = "0.0.0.0:8000"  # Bind to all IPs on port 8000
worker_class = "uvicorn.workers.UvicornWorker"  # Use Uvicorn workers with Gunicorn
worker_connections = 250  # Max number of simultaneous clients
timeout = 25  # Timeout for workers
loglevel = "WARNING"  # Log only warnings and errors
workers = max(2, os.cpu_count() // 2)  # type: ignore # Use half the CPU cores or at least 2 workers

logger.info(f"{ENV.capitalize()} environment detected. Using {workers} worker(s).")
