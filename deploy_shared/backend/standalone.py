#!/usr/bin/env python3
import cgi
import cgitb
import json
import os
import sys
from urllib.parse import parse_qs

# Enable CGI error reporting
cgitb.enable()

# Print content type
print("Content-Type: application/json\n")

try:
    # Get request method and path
    request_method = os.environ.get('REQUEST_METHOD', 'GET')
    path_info = os.environ.get('PATH_INFO', '/')
    query_string = os.environ.get('QUERY_STRING', '')
    
    # Simple API responses
    if '/init-admin' in path_info:
        response = {
            "status": "success",
            "message": "Standalone API is working!",
            "info": {
                "method": request_method,
                "path": path_info,
                "query": query_string,
                "python_version": sys.version,
                "working_directory": os.getcwd()
            },
            "next_steps": [
                "This confirms Python CGI is working",
                "Now we need to install Flask dependencies",
                "Or configure your hosting to support Flask"
            ]
        }
        print(json.dumps(response, indent=2))
        
    elif '/pages' in path_info:
        response = {
            "pages": [
                {
                    "id": 1,
                    "title": "Test Page",
                    "content": "This is a test page from standalone API",
                    "slug": "test-page",
                    "status": "published",
                    "created_at": "2024-01-01T00:00:00",
                    "author": "system"
                }
            ],
            "pagination": {
                "page": 1,
                "limit": 10,
                "total": 1,
                "totalPages": 1,
                "hasNext": False,
                "hasPrev": False
            },
            "message": "Standalone API working - Flask not required for this test"
        }
        print(json.dumps(response, indent=2))
        
    else:
        response = {
            "status": "error",
            "message": f"Unknown endpoint: {path_info}",
            "available_endpoints": ["/init-admin", "/pages"],
            "request_info": {
                "method": request_method,
                "path": path_info,
                "query": query_string
            }
        }
        print(json.dumps(response, indent=2))

except Exception as e:
    error_response = {
        "status": "error",
        "message": str(e),
        "type": "standalone_api_error"
    }
    print(json.dumps(error_response, indent=2)) 