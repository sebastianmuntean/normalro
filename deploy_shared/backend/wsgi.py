#!/usr/bin/env python3
import os
import sys

# Add the backend directory to Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    env_file = os.path.join(backend_dir, '.env')
    if os.path.exists(env_file):
        load_dotenv(env_file)
except ImportError:
    pass

from app import create_app, db

# Create the Flask application instance
app = create_app(os.environ.get('FLASK_ENV', 'production'))

# Initialize database
with app.app_context():
    db.create_all()

# For CGI execution
if __name__ == "__main__":
    from wsgiref.handlers import CGIHandler
    CGIHandler().run(app) 