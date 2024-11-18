#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Set environment variables
export FLASK_APP=app
export FLASK_ENV=development
export FLASK_DEBUG=1

# Run Flask development server
flask run --host=0.0.0.0 --port=5000
