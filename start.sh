#!/bin/bash

set -e

ENV=${ENV:-local}

if [ "$ENV" == "local" ]; then
    echo "Running Gunicorn in local mode."
    # Run Gunicorn with the --reload option for local development
    exec gunicorn main:app --config config/gunicorn.conf.py --reload
else
    echo "Running Gunicorn in cloud $ENV mode."
    # Run Gunicorn without --reload in production
    exec gunicorn main:app --config config/gunicorn.conf.py
fi
