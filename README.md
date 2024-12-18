# genai-function-calling-api

This API supports function calling with chat history stored in GCS. The current day's history is fed to the model to ensure context-aware and multi-turn responses.

## Features

1. Generation with APIs
2. Generation with Vector Search

## Prerequisites

1. A Google Cloud Project with the Vertex AI API enabled.
2. Appropriate IAM roles.
3. GCS buckets to store conversation history and embeddings.
4. Configure the `.env` file
5. Authenticate locally with GCP:

```
make auth
```

6. Generate embeddings:

```
make generate_embeddings
```

7. Create and deploy Vertex Search Index Endpoint on the console
8. Update `.env` with Index Endpoint related variables

## Run

```
# Run Locally (Without Docker)
python3 -m venv venv
source venv/bin/activate
make run

# Run Locally (With Docker)
make docker

# Tests
make tests

```

## Test

```
make prompt_api # how much did i spend on groceries this year
make prompt_search # suggest some toys over 2500

```
