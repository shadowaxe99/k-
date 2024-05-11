```python
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from utils.validators import validateEmail
from database.models import User
from database.database_connection import insertUser, getUserByEmail
from utils.helpers import generateJWT
from api.exceptions import AuthenticationError, ValidationError

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        raise ValidationError('Username, email, and password are required.')

    if not validateEmail(email):
        raise ValidationError('Invalid email address.')

    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User(username=username, email=email, password=hashed_password)

    try:
        insertUser(new_user)
    except Exception as e:
        raise AuthenticationError(f'Error during registration: {str(e)}')

    return jsonify({'message': 'User registered successfully.'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        raise ValidationError('Email and password are required.')

    user = getUserByEmail(email)

    if not user or not check_password_hash(user.password, password):
        raise AuthenticationError('Invalid credentials.')

    token = generateJWT(user.id)

    return jsonify({'token': token}), 200
```