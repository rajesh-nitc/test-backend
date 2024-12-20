# genai-function-calling-api

This API supports function calling with chat history stored in GCS. The last two turns of conversation are retrieved and fed to the model to ensure context-aware, multi-turn responses.

## Features

1. Grounded generation with APIs
2. Grounded generation with Vector Search

## Prerequisites

1. A Google Cloud Project with the Vertex AI API enabled.
2. Appropriate IAM roles.
3. GCS buckets to store conversation history and embeddings.
4. Configure `config/settings.py` and vars in `Makefile`
5. Authenticate locally with GCP:

```
make auth
```

6. Generate embeddings:

```
make embeddings
```

7. Deploy vertex search index endpoint on the console
8. Update `config/settings.py` with endpoint related variables

## Run

```
# Run Locally (Without Docker)
python3 -m venv venv
source venv/bin/activate
make run

# Run Locally (With Docker)
make docker

```

## Test

```
make prompt PROMPT='how much did i spend on entertainment this year?'
make prompt PROMPT='suggest indoor toys for kids over $$2500?'

```
