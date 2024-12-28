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
worker_connections = 1250  # Max number of simultaneous clients
timeout = 125  # Timeout for workers
loglevel = "WARNING"  # Log only warnings and errors

# Log the decision for worker count
workers = os.cpu_count() or 1  # Default to 1 worker if cpu_count() is None
logger.info(
    f"{ENV.capitalize()} environment detected. Using {workers} worker(s) based on CPU count."
)
