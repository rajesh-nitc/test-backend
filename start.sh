#!/bin/bash

# Set the default environment to 'dev' if not specified
ENV=${ENV:-dev}

if [ "$ENV" == "dev" ]; then
    echo "Running Gunicorn in development mode."
    # Run Gunicorn with the --reload option for development
    gunicorn main:app --config config/gunicorn.conf.py --reload
else
    echo "Running Gunicorn in production mode."
    # Run Gunicorn without --reload in production
    gunicorn main:app --config config/gunicorn.conf.py
fi
