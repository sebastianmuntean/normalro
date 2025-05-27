#!/usr/bin/env python3
import os
import sys
import cgitb

# Enable CGI error reporting
cgitb.enable()

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Set environment variables if not set
if not os.environ.get('SECRET_KEY'):
    os.environ['SECRET_KEY'] = 'change-this-to-a-secure-random-string-right-now'
if not os.environ.get('JWT_SECRET_KEY'):
    os.environ['JWT_SECRET_KEY'] = 'change-this-to-another-secure-random-string'
if not os.environ.get('FLASK_ENV'):
    os.environ['FLASK_ENV'] = 'production'

try:
    # Import and create app
    from app import create_app, db
    
    app = create_app('production')
    
    # Initialize database if it doesn't exist
    db_path = os.path.join(current_dir, 'cms.db')
    if not os.path.exists(db_path):
        with app.app_context():
            db.create_all()
    
    # Handle CGI request
    from wsgiref.handlers import CGIHandler
    CGIHandler().run(app)
    
except Exception as e:
    # Print error for debugging
    print("Content-Type: text/html\n")
    print(f"<h1>Error</h1><p>{str(e)}</p>")
    import traceback
    print(f"<pre>{traceback.format_exc()}</pre>") 