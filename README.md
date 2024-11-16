# hello-genai

Work in progress

```
.
├── README.md
├── config
│   ├── gunicorn.conf.py
│   └── logging.py
├── function_declarations
│   └── spend.py
├── main.py
├── models
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

## Test
```
curl -X 'POST' 'http://localhost:8000/api/v1/prompt' -H 'Content-Type: application/json' -d '{ "prompt": "how much did i spend on travel last month" }'
```