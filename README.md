# genai-function-calling-api

This API supports function calling with Azure OpenAI models and Gemini models on Vertex AI. The model is provided with the day's chat history to maintain multi-turn context.

## Models Tested

- **gpt-4o-mini**
- **gemini-1.5-pro**
- **gemini-1.5-flash**
- **gemini-2.0-flash-exp**

## Features

1. **Generation with APIs** _(get_location_coordinates_func, get_weather_by_coordinates_func, get_spend_func)_
2. **Generation with Vector Search** _(search_toys_func)_

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

1. **Azure OpenAI**: Azure OpenAI service on Azure and model deployment on Azure AI Foundry.
2. **GCP Project**: Vertex AI API is enabled.
3. **GCS Buckets**: Buckets for storing chat and embeddings.
4. **IAM roles**: Appropriate IAM roles on Azure and GCP.
5. **Virtual Environment**:

```

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-test.txt
pre-commit install
```

6. **Embeddings** _(optional, required only if feature #2 is used)_:

```
make embeddings
```

7. **Vector Search** _(optional, required only if feature #2 is used)_: Vector search index is deployed on GCP via the console, using the embeddings JSON generated in previous step.
8. **Configuration**: Configured variables in `config/settings.py` and `Makefile`.
9. **GCP Authentication**:

```
   make auth
```

10. **GCS history**: History is cleared before switching from Azure OpenAI model to Gemini model or vice versa:

```
make clear_bucket
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
