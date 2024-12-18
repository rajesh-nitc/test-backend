include .env

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
	sudo docker build -t function-calling-api .
	sudo docker run -d -p 8000:8000 \
	-v ~/.config/gcloud/application_default_credentials.json:/tmp/keys/credentials.json \
	-e GOOGLE_APPLICATION_CREDENTIALS=/tmp/keys/credentials.json \
	--env-file .env \
	--name function-calling-api \
	function-calling-api

docker_clean:
	sudo docker stop function-calling-api
	sudo docker rm function-calling-api

# Run tests
tests:
	pytest -s

# Send a prompt request using cURL
prompt_api:
	curl -X 'POST' 'http://localhost:8000/api/v1/prompt' \
  	-H 'Content-Type: application/json' \
  	-d '{ "prompt": "how much did i spend on entertainment this year?", "user_id": "rajesh-nitc" }'

prompt_search:
	curl -X 'POST' 'http://localhost:8000/api/v1/prompt' \
  	-H 'Content-Type: application/json' \
  	-d '{ "prompt": "suggest toys over $$2500?", "user_id": "rajesh-nitc" }'

# Generate embeddings
generate_embeddings:
	python3 helpers/generate_embeddings.py
