#!/bin/bash

set -e

exec gunicorn main:app --config config/gunicorn.conf.py
