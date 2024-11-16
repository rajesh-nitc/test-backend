# hello-genai

Mostly function calling

```
tree -a -I "__pycache__|venv|.git|.ruff_cache"
.
├── .dockerignore
├── .env
├── .gitattributes
├── .gitignore
├── .pre-commit-config.yaml
├── Dockerfile
├── README.md
├── config
│   ├── gunicorn.conf.py
│   └── logging.py
├── function_declarations
│   └── spend.py
├── main.py
├── models
│   ├── mock_external_api.py
│   └── prompt.py
├── requirements.txt
├── routers
│   └── prompt.py
├── services
│   ├── mock_external_api.py
│   └── vertex_ai.py
├── start.sh
├── tools
│   └── spend.py
└── utils
    └── genai.py
```

## Run
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pre-commit install
# Update PROJECT_ID in .env
./start.sh
```

With Docker:
```
docker build -t hello-genai .
docker run -d -p 8000:8000 \
  -v ~/.config/gcloud/application_default_credentials.json:/tmp/keys/credentials.json \
  -e GOOGLE_APPLICATION_CREDENTIALS=/tmp/keys/credentials.json \
  -e ENV=dev \
  -e PROJECT_ID=$PROJECT_ID \
  -e REGION=europe-west4 \
  -e MODEL_NAME=gemini-1.5-pro \
  -e LOG_LEVEL=INFO \
  hello-genai
```
## Test
```
curl -X 'POST' 'http://localhost:8000/api/v1/prompt' -H 'Content-Type: application/json' -d '{ "prompt": "how much did i spend on travel last month" }'
```
