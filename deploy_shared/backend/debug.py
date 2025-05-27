#!/usr/bin/env python3
print("Content-Type: text/html\n")

try:
    print("<h1>Python CGI Debug</h1>")
    
    # Test 1: Basic Python
    print("<h2>✅ Python is working!</h2>")
    
    # Test 2: Environment
    import os
    print(f"<p><strong>Python Version:</strong> {os.sys.version}</p>")
    print(f"<p><strong>Current Directory:</strong> {os.getcwd()}</p>")
    print(f"<p><strong>Script Directory:</strong> {os.path.dirname(os.path.abspath(__file__))}</p>")
    
    # Test 3: Environment Variables
    print("<h3>Environment Variables:</h3>")
    print(f"<p>FLASK_ENV: {os.environ.get('FLASK_ENV', 'Not Set')}</p>")
    print(f"<p>SECRET_KEY: {os.environ.get('SECRET_KEY', 'Not Set')}</p>")
    print(f"<p>PYTHONPATH: {os.environ.get('PYTHONPATH', 'Not Set')}</p>")
    
    # Test 4: Python Path
    import sys
    print("<h3>Python Path:</h3>")
    for path in sys.path:
        print(f"<p>{path}</p>")
    
    # Test 5: Try importing Flask
    try:
        import flask
        print(f"<p>✅ Flask version: {flask.__version__}</p>")
    except ImportError as e:
        print(f"<p>❌ Flask import error: {e}</p>")
    
    # Test 6: Try importing our app
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, current_dir)
        
        from app import create_app
        print("<p>✅ App import successful!</p>")
        
        app = create_app('production')
        print("<p>✅ App creation successful!</p>")
        
    except Exception as e:
        print(f"<p>❌ App import/creation error: {e}</p>")
        import traceback
        print(f"<pre>{traceback.format_exc()}</pre>")

except Exception as e:
    print(f"<h1>Critical Error</h1><p>{e}</p>")
    import traceback
    print(f"<pre>{traceback.format_exc()}</pre>") 