# genai-function-calling-api

This API supports function calling with Azure OpenAI models and Gemini models on Vertex AI. The model is provided with the day's chat history to maintain multi-turn context.

## Models Tested

- **openai/gpt-4**
- **openai/gpt-4o**
- **openai/gpt-4o-mini**
- **google/gemini-1.5-pro**
- **google/gemini-1.5-flash**
- **google/gemini-2.0-flash-exp**

## Features

1. **Generation with APIs** (e.g., `get_location_coordinates_func`, `get_weather_by_coordinates_func`)
2. **Generation with Vector Search** (e.g., `search_toys_func`)

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
            search_toys_func,
        ],
    )
```

## 🚀 Getting Started

### Prerequisites

1. **Azure OpenAI**: An Azure OpenAI service with the model deployed on Azure AI Foundry.
2. **GCP Project**: A Google Cloud project with Vertex AI API enabled.
3. **IAM Roles**: Appropriate IAM roles configured for Azure and GCP.
4. **GCS Buckets**: Buckets set up for storing chat history and embeddings.
5. **Virtual Environment**:

```

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-test.txt
pre-commit install
```

6. **Text Embeddings** (optional, required only if Feature #2 is used):

```
make gcp_embeddings
```

7. **Vector Search** (optional, required only if Feature #2 is used): A Vector Search index deployed via the console using the embeddings JSON generated in the previous step.
8. **Configuration**: Variables are set in `config/settings.py` and `Makefile`.
9. **GCP Authentication**:

```
   make gcp_auth
```

10. **Model Switch**: The chat history is cleared before switching between Azure OpenAI and Gemini models:

```
make gcp_clear_history
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
make prompt PROMPT='what is 1+1 and how is the weather in bengaluru and mumbai?'

# Generation with Vector Search
make prompt PROMPT='suggest toys like Uno under $$25?'

```
