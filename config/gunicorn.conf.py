import os

from config.logging import setup_logging
from config.settings import settings

setup_logging(settings.log_level)

ENV = settings.env

# Get the number of CPU cores (use it for worker count)
workers = 1 if ENV == "local" else os.cpu_count()

# Gunicorn configuration settings
bind = "0.0.0.0:8000"  # Bind to all IPs on port 8000
worker_class = "uvicorn.workers.UvicornWorker"  # Use Uvicorn workers with Gunicorn
worker_connections = 1250  # Max number of simultaneous clients
timeout = 125  # Timeout for workers
accesslog = "-"  # Log access requests to stdout (or a file)
errorlog = "-"  # Log errors to stdout (or a file)
loglevel = "info"  # Log level for Gunicorn logs

# Log the decision
if ENV == "local":
    print("Local development env detected. Using a single worker.")
else:
    print(
        f"Cloud {ENV} environment detected. Using CPU cores for worker count: {workers}"
    )
