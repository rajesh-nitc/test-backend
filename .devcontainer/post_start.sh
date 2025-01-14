#!/bin/bash

set -e

# Define the virtual environment directory
VENV_DIR="./.venv"
REQUIREMENTS_FILE="requirements-dev.txt"

# Check if the virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv "$VENV_DIR"
fi

# Activate the virtual environment
source "$VENV_DIR/bin/activate"

# Check if the 'openai' package is installed
if ! pip show openai > /dev/null 2>&1; then
    echo "'openai' package not found. Assuming a fresh start."
    echo "Installing all dependencies from $REQUIREMENTS_FILE..."
    pip install -r "$REQUIREMENTS_FILE"
    pre-commit install
    echo "Dependencies installed successfully."
else
    echo "'openai' package is already installed. Skipping installation."
fi
