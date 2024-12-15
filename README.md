# function-calling-api

This API enables function calling with chat history stored in GCS. The current day's history is fed to the model to ensure accurate, context-aware, and multi-turn conversations.

## Features
1. APIs
2. RAG *(TODO)*

## Prerequisites

1. A Google Cloud Project with the Vertex AI API enabled.
2. A GCS bucket to store conversation history.
3. Appropriate IAM roles:

- Vertex AI User on the project.
- Storage Object User on the GCS bucket.

4. Configure the `.env` file with required environment variables.
5. Authenticate with GCP:

```
make auth
```

## Run

### Run Locally (Without Docker)

1. Create a virtual environment:

```
python3 -m venv venv
source venv/bin/activate
```

2. Run

```
make run
```

### Run Locally (With Docker)

```
make docker
```

## Tests

`make tests`

## Send prompt

To send a test prompt to the api:

`make prompt`
