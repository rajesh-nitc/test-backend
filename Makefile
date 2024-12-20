include .env

# Include this so that we can run "make tests"
.PHONY: tests

# Google Cloud Authentication
auth:
	gcloud auth application-default login
	gcloud auth application-default set-quota-project $(GOOGLE_CLOUD_PROJECT)

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
	--env-file .env \
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
