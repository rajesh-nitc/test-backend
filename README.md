# function-calling-api

This API enables function calling with chat history stored in GCS, with the current day's history fed to the model to ensure accurate, context-aware, and multi-turn conversations.

## Prerequisites

1. A GCP project with Vertex AI API enabled.
2. A GCS bucket.
3. Roles:

- `roles/aiplatform.user` at the project level.
- `roles/storage.objectUser` on the GCS bucket.

4. Run to authenticate locally:

- `gcloud auth application-default login`
- `gcloud auth application-default set-quota-project prj-bu1-d-sample-base-9208`

5. Ensure the `.env` file is properly configured with environment variables.

## Run

Locally without Docker:

```
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements-test.txt

# Set up pre-commit hooks
pre-commit install

# Start the application
./start.sh

```

Locally with Docker:

```
# Build the Docker image
sudo docker build -t function-calling-api .

# Run the Docker container
sudo docker run -d -p 8000:8000 \
  -v ~/.config/gcloud/application_default_credentials.json:/tmp/keys/credentials.json \
  -e GOOGLE_APPLICATION_CREDENTIALS=/tmp/keys/credentials.json \
  --env-file .env \
  function-calling-api

```

## Test

```
curl -X 'POST' 'http://localhost:8000/api/v1/prompt' \
  -H 'Content-Type: application/json' \
  -d '{ "prompt": "how much did i spend on travel last month", "user_id": "rajesh-nitc" }'

```
