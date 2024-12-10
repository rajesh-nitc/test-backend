#!/bin/bash

set -e

ENV=${ENV:-dev}

if [ "$ENV" == "dev" ]; then
    echo "Running Gunicorn in development mode."
    # Run Gunicorn with the --reload option for development
    exec gunicorn main:app --config config/gunicorn.conf.py --reload
else
    echo "Running Gunicorn in production mode."
    # Run Gunicorn without --reload in production
    exec gunicorn main:app --config config/gunicorn.conf.py
fi
