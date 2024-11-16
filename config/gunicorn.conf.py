import os

# Get the number of CPU cores (use it for worker count)
workers = os.cpu_count()

# Gunicorn configuration settings
bind = "0.0.0.0:8000"  # Bind to all IPs on port 8000
worker_class = "uvicorn.workers.UvicornWorker"  # Use Uvicorn workers with Gunicorn
worker_connections = 2500  # Max number of simultaneous clients
timeout = 25  # Timeout for workers
accesslog = "-"  # Log access requests to stdout (or a file)
errorlog = "-"  # Log errors to stdout (or a file)
loglevel = "info"  # Log level for Gunicorn logs

# Dynamically set the number of workers based on the available CPU cores
workers = workers  # Number of workers equals CPU cores
