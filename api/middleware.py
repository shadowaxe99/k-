from functools import wraps
from flask import request, jsonify
from utils.validators import validate_jwt
from api.exceptions import AuthenticationError

def authenticate_request(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise AuthenticationError("Missing authentication token.")
        
        token = auth_header.split(" ")[1]
        if not validate_jwt(token):
            raise AuthenticationError("Invalid or expired token.")
        
        return f(*args, **kwargs)
    return decorated_function

def log_request(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # This is a placeholder for logging logic
        # In a real-world scenario, you would log the request details
        # to a file or a logging service
        print(f"Handling {request.method} request for {request.path}")
        return f(*args, **kwargs)
    return decorated_function

def handle_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except AuthenticationError as e:
            response = jsonify({"error": str(e)})
            response.status_code = 401
            return response
        except Exception as e:
            response = jsonify({"error": "An unexpected error occurred."})
            response.status_code = 500
            return response
    return decorated_function
