# genai-function-calling-api

This API supports function calling with Gemini models. User history from the same day is fed to the model to maintain multi-turn context.

## Features

1. Generation with APIs
2. Generation with Vector Search

## Getting Started

### Prerequisites

1. A Google Cloud Project with the Vertex AI API enabled
2. GCS buckets: one for chat history and one for embeddings
3. IAM roles: Vertex AI User and Storage Object User
4. Update `config/settings.py` and variables in `Makefile`
5. Authenticate locally with GCP: ```make auth```
6. Generate embeddings: ```make embeddings```
7. Deploy vertex search index endpoint on the console
8. Update `config/settings.py` with endpoint variables
9. Create virtual environment:

```
python3 -m venv venv
source venv/bin/activate
```

### Run

```
# Run Locally (Without Docker)
make run

# Run Locally (With Docker)
make docker

```

### Test

```
# Generation with APIs
make prompt PROMPT='how much did i spend on entertainment this year?'

# Generation with Vector Search
make prompt PROMPT='suggest toys like Uno under $$25?'

```
