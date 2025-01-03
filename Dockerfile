# Stage 1: Builder stage for installing dependencies
FROM python:3.12-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100

# Create and set work directory
WORKDIR /app

# Install Python dependencies in a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy dependency files first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Stage 2: Final stage for the application
FROM python:3.12-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set non-root user
RUN useradd -m appuser
USER appuser

# Create and set work directory
WORKDIR /app

# Copy application files from the builder stage
COPY --from=builder /opt/venv /opt/venv
COPY . .

# Update PATH to use the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Expose the app's port
EXPOSE 8000

# Command to run the application
ENTRYPOINT ["bash", "./start.sh"]
