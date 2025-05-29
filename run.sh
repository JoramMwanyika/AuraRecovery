#!/bin/bash

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export FLASK_APP=app.py
export FLASK_ENV=development

# Initialize database
python -c "from app import app, db; app.app_context().push(); db.create_all()"

# Run the application
flask run --host=0.0.0.0 --port=5000
