from flask import Blueprint, jsonify, current_app, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

from logger_setup import logger

from db.user import UserManager

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    user_manager = UserManager(app=current_app)
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify(error="Missing fields"), 400

    try:
        hashed_password = generate_password_hash(password)
        user = user_manager.create_user(username=username, email=email, password=hashed_password)
        logger.info(f"New user registered: {email}")
        return jsonify(user=user.to_safe_dict()), 201

    except Exception as e:
        logger.error(f"Error registering user: {e}")
        return jsonify(error="Registration failed"), 500


@auth.route('/login', methods=['POST'])
def login():
    """Authenticate a user and return a JWT token."""
    user_manager = UserManager(app=current_app)
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify(error="Missing email or password"), 400

    try:
        user = user_manager.get_user_by_email(email)
        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id)
            logger.info(f"User logged in: {email}")
            return jsonify(access_token=access_token, user=user.to_safe_dict()), 200
        else:
            return jsonify(error="Invalid credentials"), 401

    except Exception as e:
        logger.error(f"Error during login: {e}")
        return jsonify(error="Login failed"), 500


@auth.route('/change_username', methods=['PUT'])
@jwt_required()
def change_username():
    """Change the username of the authenticated user."""
    user_manager = UserManager(app=current_app)
    user_id = get_jwt_identity()
    data = request.get_json()
    new_username = data.get("username")

    if not new_username:
        return jsonify(error="New username not provided"), 400

    try:
        user = user_manager.update_user(user_id, username=new_username)
        logger.info(f"Username changed for user: {user_id}")
        return jsonify(user=user.to_safe_dict()), 200

    except Exception as e:
        logger.error(f"Error changing username for user {user_id}: {e}")
        return jsonify(error="Failed to change username"), 500


@auth.route('/delete_user', methods=['DELETE'])
@jwt_required()
def delete_user():
    """Delete the authenticated user."""
    user_manager = UserManager(app=current_app)
    user_id = get_jwt_identity()

    try:
        user_manager.delete_user(user_id)
        logger.info(f"User {user_id} deleted")
        return jsonify(message="User deleted successfully"), 200

    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {e}")
        return jsonify(error="Failed to delete user"), 500