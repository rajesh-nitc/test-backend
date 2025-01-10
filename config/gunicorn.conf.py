import logging
import multiprocessing

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

if ENV == "local":
    workers = 2
else:
    num_cpus = multiprocessing.cpu_count()
    workers = (num_cpus * 2) + 1

logger.info(f"{ENV.capitalize()} environment detected. Using {workers} worker(s).")
