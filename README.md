# function-calling-api

This API supports function calling with chat history stored in GCS, ensuring that each user's conversation is preserved and accessible to the model for the current day. This enables the model to maintain context and deliver more accurate, context-aware responses.

## Prerequisites

1. A GCP project with Vertex AI API enabled.
2. A GCS bucket.
3. Roles:
   - `roles/aiplatform.user` (Vertex AI User) at the project level.
   - `roles/storage.objectAdmin` (Storage Object Admin) on the GCS bucket.
4. Run `gcloud auth application-default login` to authenticate locally.
5. Ensure the `.env` file is properly configured with environment variables.


## Project structure
```
tree -a -I "__pycache__|venv|.git"
.
├── .dockerignore
├── .env
├── .gitattributes
├── .gitignore
├── .pre-commit-config.yaml
├── Dockerfile
├── README.md
├── config
│   ├── gunicorn.conf.py
│   └── logging.py
├── function_declarations
│   └── spend.py
├── main.py
├── models
│   ├── mock_external_api.py
│   └── prompt.py
├── requirements.txt
├── routers
│   └── prompt.py
├── services
│   ├── mock_external_api.py
│   └── vertex_ai.py
├── start.sh
├── tools
│   └── spend.py
└── utils
    ├── date.py
    ├── gcs_history.py
    └── vertex_ai.py
```

## Run

Locally without Docker:
```
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up pre-commit hooks
pre-commit install

# Start the application
./start.sh

```

Locally with Docker:
```
# Build the Docker image
docker build -t function-calling-api .

# Run the Docker container
docker run -d -p 8000:8000 \
  -v ~/.config/gcloud/application_default_credentials.json:/tmp/keys/credentials.json \
  -e GOOGLE_APPLICATION_CREDENTIALS=/tmp/keys/credentials.json \
  --env-file .env \
  function-calling-api

```

## Test
```
curl -X 'POST' 'http://localhost:8000/api/v1/prompt' \
  -H 'Content-Type: application/json' \
  -d '{ "prompt": "how much did i spend on travel last month", "user_id": "25" }'

```
