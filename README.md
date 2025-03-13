# test-backend

This API supports function calling with both Azure OpenAI models and Gemini models on Vertex AI. The model is provided with the day's chat history to maintain multi-turn context.

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

## Getting Started 🚀

### Prerequisites

1. **Azure Authentication**:

```
echo 'export AZURE_OPENAI_API_KEY=YOUR_API_KEY_HERE' >> ~/.zshrc
```

2. **GCP Authentication**:

```
make gcp_app_auth
make gcp_gcloud_auth
```

3. **OpenWeather Authentication**:

```
echo 'export OPENWEATHER_API_KEY=YOUR_API_KEY_HERE' >> ~/.zshrc
```

4. **Application Settings**: Update `config/settings.py`

5. **Text Embeddings** (required only if using Feature #2): Generate embeddings JSON and deploy a Vector Search index via the GCP console.

```
make gcp_embeddings
```

6. **Additional Notes**:

- Dev Containers require Linux or WSL on Windows, along with VS Code (with the Dev Containers extension) and Docker Desktop.
- After updating environment variables in steps 1 and 3, open a new terminal to ensure the changes take effect.
- Clear the chat history before switching between Azure OpenAI and Gemini models to avoid conflicts:

```
make gcp_clear_history
```

- Makefile help:

```
make help
```

### Run

```
# Run Locally
make run

# Run Locally (With Docker) - update variables in Makefile
make docker

```

### Test

```
# Generation with APIs
make prompt PROMPT='what is 1+1 and how is the weather in bengaluru and mumbai?'

# Generation with Vector Search
make prompt PROMPT='suggest indoor toys like Uno under $$25?'

```
