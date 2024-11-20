import logging
import os

from config.logging import setup_logging

setup_logging()
logger = logging.getLogger(__name__)
environment = os.getenv("ENV", "dev")  # Default to "dev" if ENV is not set

# Get the number of CPU cores (use it for worker count)
workers = 1 if environment == "dev" else os.cpu_count()

# Gunicorn configuration settings
bind = "0.0.0.0:8000"  # Bind to all IPs on port 8000
worker_class = "uvicorn.workers.UvicornWorker"  # Use Uvicorn workers with Gunicorn
worker_connections = 1250  # Max number of simultaneous clients
timeout = 125  # Timeout for workers
accesslog = "-"  # Log access requests to stdout (or a file)
errorlog = "-"  # Log errors to stdout (or a file)
loglevel = "info"  # Log level for Gunicorn logs

# Dynamically set the number of workers based on the available CPU cores
workers = workers  # Number of workers equals CPU cores

# Log the decision
if environment == "dev":
    logger.info("Development environment detected. Using a single worker.")
else:
    logger.info(
        f"Production environment detected. Using CPU cores for worker count: {workers}"
    )
