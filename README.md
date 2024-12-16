# function-calling-api

This API supports function calling with chat history stored in GCS. The current day's history is fed to the model to ensure accurate, context-aware, and multi-turn conversations.

## Features

1. APIs
2. RAG _(In Progress)_

## Use Case 1: APIs

### Prerequisites

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

### Run
```
# Run Locally (Without Docker)
python3 -m venv venv
source venv/bin/activate
make run

# Run Locally (With Docker)
make docker

# Tests
make tests

# Send prompt
make prompt
```

## Use Case 2: RAG

### Prerequisites

1. Generate embeddings

```
make generate_embeddings
```

2. Create Vertex Search Index Endpoint on the console
3. Configure the `.env` file with required environment variables.
4. Query Index Endpoint
```
make query_index
```
