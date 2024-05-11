```python
import re
import hashlib
import jwt
import os
from datetime import datetime, timedelta

def validate_email(email):
    """
    Validates the format of an email address.
    """
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return re.match(email_regex, email) is not None

def hash_password(password):
    """
    Hashes a password using SHA-256.
    """
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def generate_jwt(user_id):
    """
    Generates a JWT token for a given user ID.
    """
    jwt_secret = os.getenv('JWT_SECRET', 'your_jwt_secret')
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    token = jwt.encode(payload, jwt_secret, algorithm='HS256')
    return token

def decode_jwt(token):
    """
    Decodes a JWT token to retrieve the payload.
    """
    jwt_secret = os.getenv('JWT_SECRET', 'your_jwt_secret')
    try:
        payload = jwt.decode(token, jwt_secret, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError("The token has expired.")
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError("Invalid token.")

def get_influencer_data():
    """
    Retrieves the influencer data from a predefined source.
    """
    # This function is a placeholder and should be implemented to retrieve
    # actual influencer data from a database or an external API.
    influencer_data = {
        'name': 'Kylie Jenner',
        'description': 'Kylie Jenner is a glamorous and trendsetting personality...',
        'content': 'Kylie\'s Instagram (@kyliejenner) showcases her life...'
    }
    return influencer_data
```