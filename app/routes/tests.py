from flask import Blueprint, jsonify, current_app
from db.user import UserManager
from logger_setup import logger

tests = Blueprint('tests', __name__)

@tests.route('/')
def index():
    redis_client = current_app.redis_client
    user_manager = UserManager(app=current_app)

    try:
        user = user_manager.get_user_by_id(1)
        logger.info("Retrieved user: %s", user)

        redis_client.set("hello_keyt", "Hello from Redis!2121")
        message = redis_client.get("hello_keyt").decode("utf-8")

        logger.info("Set and retrieved message from Redis: %s", message)

        return jsonify(message=message, user=user)

    except Exception as e:
        logger.error("An error occurred while processing the request: %s", str(e))
        return jsonify(error="Internal Server Error"), 500
