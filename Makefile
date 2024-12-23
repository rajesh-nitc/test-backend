# Variables
APP_NAME=genai-function-calling-api
GOOGLE_CLOUD_PROJECT=prj-bu1-d-sample-base-9208

# Adding so that make does not conflict with files or directory with the same names as target
# For e.g. "make tests" won't work unless we add tests as a phony target
.PHONY: help auth run docker docker_clean tests prompt embeddings notebook precommit

help: ## Self-documenting help command
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

check_venv:
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "Error: Virtual environment is not activated. Please activate it and try again."; \
		exit 1; \
	fi

auth: ## Authenticate with Google Cloud
	gcloud auth application-default login
	gcloud auth application-default set-quota-project $(GOOGLE_CLOUD_PROJECT)
	gcloud config set project $(GOOGLE_CLOUD_PROJECT)

run: check_venv ## Run the application locally after authentication
	pip install -r requirements-test.txt
	pre-commit install
	bash ./start.sh

docker: ## Build and run the application in Docker
	sudo docker build -t $(APP_NAME) .
	sudo docker run -d -p 8000:8000 \
        -v ~/.config/gcloud/application_default_credentials.json:/tmp/keys/credentials.json \
        -e GOOGLE_APPLICATION_CREDENTIALS=/tmp/keys/credentials.json \
        -e APP_NAME=$(APP_NAME) \
        -e EMB_BLOB="product_embeddings.json" \
        -e EMB_BUCKET="bkt-bu1-d-function-calling-api-embedding" \
        -e EMB_DEPLOYED_INDEX_ID="index_01_deploy_1734488317622" \
        -e EMB_DF_HEAD=100 \
        -e EMB_DIMENSIONALITY=768 \
        -e EMB_INDEX_ENDPOINT="projects/770674777462/locations/asia-south1/indexEndpoints/5963364040964046848" \
        -e EMB_MODEL="text-embedding-005" \
        -e EMB_TASK="RETRIEVAL_DOCUMENT" \
        -e EMB_TOP_K=3 \
        -e ENV="local" \
        -e GOOGLE_CLOUD_PROJECT=$(GOOGLE_CLOUD_PROJECT) \
        -e LLM_BUCKET="bkt-bu1-d-function-calling-api-chat" \
        -e LLM_BUCKET_FOLDER="chat_histories" \
        -e LLM_MAX_INPUT_TOKENS=25 \
        -e LLM_MAX_OUTPUT_TOKENS=100 \
        -e LLM_MODEL="gemini-1.5-pro" \
        -e LOG_LEVEL="INFO" \
        -e REGION="asia-south1" \
        -e SYSTEM_INSTRUCTION="- The conversation history is formatted as:\n  - Previous turns have 'user:' and 'model:' prefixes.\n  - A new user query is provided **without** these prefixes.\n- Always treat new user queries (those without 'user:' and 'model:' prefixes) as independent prompts.\n- Ignore the conversation history when determining the correct function to call. Focus **only on the new user query**.\n- Only call functions for queries related to specific tasks like:\n  - Toy or game recommendations (e.g., 'suggest toys', 'find games').\n  - Spending or expense queries (e.g., 'how much did I spend on groceries', 'show my expenses for travel').\n- For general conversational queries (e.g., greetings like 'hi', 'how are you?'), respond with natural language text and **do not call any functions**." \
        --name $(APP_NAME) \
        $(APP_NAME)

docker_clean: ## Stop and remove the Docker container
	sudo docker stop $(APP_NAME)
	sudo docker rm $(APP_NAME)

tests: check_venv ## Run basic tests
	pytest -s

prompt: ## Send a prompt request using cURL (requires PROMPT)
	curl -X 'POST' 'http://localhost:8000/api/v1/prompt' \
  	-H 'Content-Type: application/json' \
  	-d '{ "prompt": "$(PROMPT)", "user_id": "rajesh-nitc" }'

embeddings: check_venv ## Generate embeddings using the helper module
	python3 helpers/generate_embeddings.py

notebook: check_venv ## Create notebook from helper module
	jupytext --to notebook helpers/generate_embeddings.py

precommit: check_venv ## Run pre-commit checks
	pre-commit run --all-files
