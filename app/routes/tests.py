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
        user = user_manager.get_user_by_id("ce036791-5451-403c-b846-cd0aab969783")
        if user:
            logger.info("Retrieved user: %s", user)

            redis_client.set("hello_keyt", "Hello from Redis!2121")
            message = redis_client.get("hello_keyt").decode("utf-8")

            logger.info("Set and retrieved message from Redis: %s", message)
            logger.info(user.username)


            user_data = user.__dict__ if user else None

            return jsonify(message=message, user=user_data)
        else:
            return jsonify(error="User not found")

    except Exception as e:
        logger.error("An error occurred while processing the request: %s", str(e))
        return jsonify(error="Internal Server Error"), 500
