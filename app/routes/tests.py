from flask import Blueprint, jsonify, current_app
from db.user import UserManager
from logger_setup import logger

tests = Blueprint('tests', __name__)

@tests.route('/')
def index():
    """Test route to check Redis and retrieve a user by ID."""
    redis_client = current_app.redis_client
    user_manager = UserManager(app=current_app)

    try:
        user = user_manager.get_user_by_id(1)
        logger.info("Retrieved user: %s", user)

        redis_client.set("hello_keyt", "Hello from Redis!2121")
        message = redis_client.get("hello_keyt").decode("utf-8")

        logger.info("Set and retrieved message from Redis: %s", message)
        logger.info(user.name)

        # Преобразуем объект User в словарь перед сериализацией в JSON
        user_data = user.__dict__ if user else None

        return jsonify(message=message, user=user_data)

    except Exception as e:
        logger.error("An error occurred while processing the request: %s", str(e))
        return jsonify(error="Internal Server Error"), 500

@tests.route('/users', methods=['GET'])
def get_all_users():
    """Fetch all users."""
    user_manager = UserManager(app=current_app)
    
    try:
        users = user_manager.get_all_users()
        users_data = [user.__dict__ for user in users]
        logger.info("Retrieved all users: %s", users_data)
        return jsonify(users=users_data), 200

    except Exception as e:
        logger.error("An error occurred while fetching users: %s", str(e))
        return jsonify(error="Internal Server Error"), 500