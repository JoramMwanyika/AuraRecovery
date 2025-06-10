#!/bin/bash

# Run database initialization
python init_db.py

# Start the Flask application
flask run --host=0.0.0.0 --port=$PORT 