from flasgger import swag_from
from flask import Blueprint, jsonify, request
from src.api.v1.models.user import User, user_schema
from src.constants.http_status_codes import HTTP_200_OK, HTTP_409_CONFLICT, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from flask_jwt_extended import create_refresh_token, create_access_token, get_jwt_identity, jwt_required
from werkzeug.security import check_password_hash
import validators


auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post('/register')
@swag_from('../../../docs/auth/register.yaml')
def register():
    first_name = request.get_json().get('first_name', None)
    last_name = request.get_json().get('last_name', None)
    email = request.get_json().get('email', None)
    password = request.get_json().get('password', '')

    if len(password) < 6:
        return jsonify({'error': "password is too short"}), HTTP_400_BAD_REQUEST

    if not first_name:
        return jsonify({'error': "first name cannot be empty"}), HTTP_400_BAD_REQUEST

    if not last_name:
        return jsonify({'error': 'last name cannot be empty'})

    if not validators.email(email):
        return jsonify({'error': "email is not valid"}), HTTP_400_BAD_REQUEST

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'error': "email is taken"}), HTTP_409_CONFLICT

    new_user = User(first_name, last_name, email, password)
    new_user.create()
    return user_schema.jsonify(new_user), HTTP_200_OK


@auth.get('/login')
@swag_from('../../../docs/auth/login.yaml')
def login():
    
    email = request.authorization['username']
    password = request.authorization['password']
    user = User.query.filter_by(email=email).first()

    if user:
        valid_password = check_password_hash(user.password, password)
        if valid_password:
            access = create_access_token(identity=user.id)
            refresh = create_refresh_token(identity=user.id)
            return jsonify({
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'created_at': user.created_at,
                'updated_at': user.updated_at,
                'access': access,
                'refresh': refresh
            }), HTTP_200_OK
        return jsonify({'error': 'invalid password'}), HTTP_401_UNAUTHORIZED

    return jsonify({'error': 'email does not exist'}), HTTP_401_UNAUTHORIZED


@auth.get('/token/access_token')
@jwt_required(refresh=True)
def access_token():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)
    return jsonify({'access': access_token}), HTTP_200_OK
