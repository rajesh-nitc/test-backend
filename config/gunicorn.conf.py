import os

from config.logging import setup_logging
from config.settings import settings

ENV = settings.env

# Set up logging based on the environment's log level
setup_logging(settings.log_level)

# Gunicorn configuration settings
bind = "0.0.0.0:8000"  # Bind to all IPs on port 8000
worker_class = "uvicorn.workers.UvicornWorker"  # Use Uvicorn workers with Gunicorn
worker_connections = 1250  # Max number of simultaneous clients
timeout = 125  # Timeout for workers

# Set Gunicorn log level from settings or default to 'info'
loglevel = settings.log_level or "info"

# Log the decision for worker count
if ENV == "local":
    workers = 1
    print(f"{ENV} dev env detected. Using a single worker.")
else:
    workers = os.cpu_count() or 1  # Use 1 as a fallback if cpu_count() returns None
    print(f"Cloud {ENV} env detected. Using {workers} worker(s) based on CPU count.")
