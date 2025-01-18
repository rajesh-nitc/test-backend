# Beyond Python and git, this image includes a number of Python tools, zsh, Oh My Zsh!, a non-root vscode user with sudo access, and a set of common dependencies for development
# https://github.com/devcontainers/images/tree/main/src/python#using-this-image
FROM mcr.microsoft.com/devcontainers/python:3.12-bullseye

# Install dependencies
RUN apt-get update && apt-get install -y \
    apt-transport-https \
    ca-certificates \
    gnupg \
    curl

# Install Google Cloud SDK
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list \
    && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg \
    && apt-get update && apt-get install -y google-cloud-sdk
