# genai-function-calling-api

This API supports function calling with Gemini models. User history from the same day is fed to the model to maintain multi-turn context.

## Features

1. Generation with APIs
2. Generation with Vector Search

## Getting Started

### Prerequisites

1. **GCP Project**: Ensure Vertex AI API is enabled.
2. **GCS Buckets**: Create buckets for storing chat history and embeddings.
3. **IAM Roles**: Assign the following roles to your user account:
   - Vertex AI User
   - Storage Object User
4. **Virtual Environment**: Set up and activate a Python virtual environment:

```

python3 -m venv venv
source venv/bin/activate
```

5. **Embeddings** _(optional, required only if feature #2 is used)_:

```
make embeddings
```

6. **Vector Search** _(optional, required only if feature #2 is used)_: Deploy a search index via the console, using the embeddings JSON generated in previous step.
7. **Configuration**: Update variables in `config/settings.py` and `Makefile` as per your project setup.
8. **Authentication**: Authenticate locally with GCP:

```
   make auth
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
make prompt PROMPT='how is the weather in bangalore and mumbai'
make prompt PROMPT='how much did i spend on entertainment this year?'

# Generation with Vector Search
make prompt PROMPT='suggest toys like Uno under $$25?'

```
