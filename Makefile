# Variables
APP_NAME=genai-function-calling-api
GOOGLE_CLOUD_PROJECT=prj-bu1-d-sample-base-9208
LLM_CHAT_BUCKET=bkt-bu1-d-function-calling-api-chat

# Adding so that make does not conflict with files or directory with the same names as target
# For e.g. "make tests" won't work unless we add tests as a phony target
.PHONY: help gcp_app_auth gcp_gcloud_auth gcp_clear_history gcp_credentials_base64 gcp_embeddings \
run prompt tests notebook precommit docker docker_clean

help: ## Self-documenting help command
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

check_venv:
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "Error: Virtual environment is not activated. Please activate it and try again."; \
		exit 1; \
	fi

gcp_app_auth: ## App Auth with Google Cloud
	gcloud auth application-default login
	gcloud auth application-default set-quota-project $(GOOGLE_CLOUD_PROJECT)
	gcloud config set project $(GOOGLE_CLOUD_PROJECT)

gcp_gcloud_auth: ## gcloud Auth (Required for gsutil command in gcp_clear_history)
	gcloud auth login

gcp_clear_history: ## Clear gcs bucket contents (To clear the history)
	gsutil -m rm -r gs://$(LLM_CHAT_BUCKET)/**

gcp_credentials_base64: ## Base64 encode GCP creds JSON (Use this for Github Actions Repository secret)
	base64 ~/.config/gcloud/application_default_credentials.json > credentials.json.base64
	cat credentials.json.base64
	rm credentials.json.base64

gcp_embeddings: check_venv ## Generate embeddings using the helper module
	PYTHONPATH=. python3 helpers/generate_embeddings.py

run: check_venv ## Run the application locally after authentication
	bash ./start.sh

prompt: ## Send a prompt request using cURL (requires PROMPT)
	curl -X 'POST' 'http://localhost:8000/api/prompt' \
  	-H 'Content-Type: application/json' \
  	-d '{ "prompt": "$(PROMPT)", "user_id": "rajesh-nitc" }'

# Run test cases with --test-cases="weather,toys"
tests: check_venv ## Run test use cases
	pytest -m integration --test-cases="weather,toys"

notebook: check_venv ## Create jupyter notebook from python module
	jupytext --to notebook helpers/generate_embeddings.py

precommit: check_venv ## Run pre-commit checks
	pre-commit run --all-files

# Add AZURE_OPENAI_API_KEY and OpenWeather API key
docker: ## Build and run the application in Docker
	sudo docker build -t $(APP_NAME) .
	sudo docker run -d -p 8000:8000 \
        -v ~/.config/gcloud/application_default_credentials.json:/tmp/keys/credentials.json \
        -e GOOGLE_APPLICATION_CREDENTIALS=/tmp/keys/credentials.json \
        -e APP_NAME=$(APP_NAME) \
		-e AZURE_OPENAI_API_KEY="" \
		-e AZURE_OPENAI_ENDPOINT="https://oai-function-calling-api.openai.azure.com/" \
        -e EMB_BUCKET="bkt-bu1-d-function-calling-api-embedding" \
        -e EMB_DEPLOYED_INDEX_ID="index_01_deploy_1734488317622" \
        -e EMB_INDEX_ENDPOINT="projects/770674777462/locations/us-central1/indexEndpoints/5963364040964046848" \
        -e EMB_MODEL="text-embedding-005" \
        -e EMB_TOP_K=3 \
        -e ENV="local" \
        -e GOOGLE_CLOUD_PROJECT=$(GOOGLE_CLOUD_PROJECT) \
		-e HTTP_CLIENT_BASE_URL="https://api.openweathermap.org" \
        -e LLM_CHAT_BUCKET="bkt-bu1-d-function-calling-api-chat" \
        -e LLM_MODEL="google/gemini-2.0-flash-exp" \
        -e LLM_SYSTEM_INSTRUCTION="Ask clarifying questions if not enough information is available. Don't explain what you are doing, just provide the result" \
        -e LOG_LEVEL="INFO" \
		-e OPENWEATHER_API_KEY="" \
        -e REGION="us-central1" \
        --name $(APP_NAME) \
        $(APP_NAME)

docker_clean: ## Stop and remove the Docker container
	sudo docker stop $(APP_NAME)
	sudo docker rm $(APP_NAME)
