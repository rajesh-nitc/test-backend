import os

from config.logging import setup_logging
from config.settings import settings

ENV = settings.ENV

# Set up logging based on the environment's log level
setup_logging(settings.LOG_LEVEL)

# Gunicorn configuration settings
bind = "0.0.0.0:8000"  # Bind to all IPs on port 8000
worker_class = "uvicorn.workers.UvicornWorker"  # Use Uvicorn workers with Gunicorn
worker_connections = 1250  # Max number of simultaneous clients
timeout = 125  # Timeout for workers

# Set Gunicorn log level from settings or default to 'info'
loglevel = settings.LOG_LEVEL or "info"

# Log the decision for worker count
workers = os.cpu_count() or 1  # Default to 1 worker if cpu_count() is None
print(
    f"{ENV.capitalize()} environment detected. Using {workers} worker(s) based on CPU count."
)
