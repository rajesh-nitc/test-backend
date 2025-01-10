# genai-function-calling-api

This API supports function calling with Gemini LLM models on Vertex AI. The model is provided with the day's chat history to maintain multi-turn context. The model's usage limit can be configured to manage costs.

## Features

1. Generation with APIs _(get_location_coordinates_func, get_weather_by_coordinates_func, get_spend_func)_
2. Generation with Vector Search _(search_toys_func)_

## Agent

```
def get_agent() -> Agent:

    return Agent(
        name=f"{settings.APP_NAME}-agent",
        model=settings.LLM_MODEL,
        system_instruction=settings.LLM_SYSTEM_INSTRUCTION,
        functions=[
            get_location_coordinates_func,
            get_weather_by_coordinates_func,
            get_spend_func,
            search_toys_func,
        ],
    )
```

## 🚀 Getting Started

### Prerequisites

1. **GCP Project**: Ensure Vertex AI API is enabled.
2. **GCS Buckets**: Create buckets for storing chat, quota and embeddings.
3. **IAM Roles**: Ensure that your user account has at least the following roles:
   - Vertex AI User
   - Storage Object User
4. **Virtual Environment**:

```

python3 -m venv .venv
source .venv/bin/activate
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
make prompt PROMPT='how is the weather in bengaluru and mumbai?'
make prompt PROMPT='how much did i spend on entertainment this year?'

# Generation with Vector Search
make prompt PROMPT='suggest toys like Uno under $$25?'

```
