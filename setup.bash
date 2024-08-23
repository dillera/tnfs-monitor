#!/bin/bash

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required packages
pip install Flask flask_sqlalchemy ping3

# Export Flask app environment variable
export FLASK_APP=app

# Set PYTHONPATH to the current directory
export PYTHONPATH=$(pwd)

# Create initial database
cat <<EOF > create_db.py
from app import create_app
from app.models import db

app = create_app()

with app.app_context():
    db.create_all()
    print("Database created successfully.")
EOF

# Run the script to create the database
python create_db.py

# Clean up the temporary Python script
rm create_db.py

# Deactivate virtual environment
deactivate

echo "Setup complete. The virtual environment is ready, and the database has been initialized."