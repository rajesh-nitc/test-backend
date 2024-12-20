APP_NAME=genai-function-calling-api
GOOGLE_CLOUD_PROJECT=prj-bu1-d-sample-base-9208

# Include this so that we can run "make tests"
.PHONY: tests

# Google Cloud Authentication
auth:
	gcloud auth application-default login
	gcloud auth application-default set-quota-project $(GOOGLE_CLOUD_PROJECT)
	gcloud config set project $(GOOGLE_CLOUD_PROJECT)

# Run the application locally
run:
	pip install -r requirements-test.txt
	pre-commit install
	bash ./start.sh

# Build and run the application in Docker
docker:
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
        -e LLM_MAX_TOKENS=25 \
        -e LLM_MODEL="gemini-1.5-pro" \
        -e LOG_LEVEL="INFO" \
        -e REGION="asia-south1" \
        -e SYSTEM_INSTRUCTION="- The conversation history is formatted as:\n  - Previous turns have 'user:' and 'model:' prefixes.\n  - A new user query is provided **without** these prefixes.\n- Always treat new user queries (those without 'user:' and 'model:' prefixes) as independent prompts.\n- Ignore the conversation history when determining the correct function to call. Focus **only on the new user query**.\n- Only call functions for queries related to specific tasks like:\n  - Toy or game recommendations (e.g., 'suggest toys', 'find games').\n  - Spending or expense queries (e.g., 'how much did I spend on groceries', 'show my expenses for travel').\n- For general conversational queries (e.g., greetings like 'hi', 'how are you?'), respond with natural language text and **do not call any functions**." \
        --name $(APP_NAME) \
        $(APP_NAME)

docker_clean:
	sudo docker stop $(APP_NAME)
	sudo docker rm $(APP_NAME)

# Run tests
tests:
	pytest -s

# Send a prompt request using cURL
prompt:
	curl -X 'POST' 'http://localhost:8000/api/v1/prompt' \
  	-H 'Content-Type: application/json' \
  	-d '{ "prompt": "$(PROMPT)", "user_id": "rajesh-nitc" }'

# Generate embeddings
embeddings:
	python3 helpers/generate_embeddings.py

# Create notebook from py:
notebook:
	jupytext --to notebook helpers/generate_embeddings.py
