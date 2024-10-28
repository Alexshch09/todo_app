from flask import Blueprint, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from logger_setup import logger

from db.user import UserManager

auth = Blueprint('auth', __name__)

@auth.route('/protected', methods=["POST"])
@jwt_required()
def index():
    user_id = get_jwt_identity()

    redis_client = current_app.redis_client
    user_manager = UserManager(app=current_app)

    try:
        user = user_manager.get_user_by_id(user_id)
        logger.info("Retrieved user: %s", user=user.__dict__)

        redis_client.set("hello_keyt", "Hello from Redis!2121")
        message = redis_client.get("hello_keyt").decode("utf-8")

        logger.info("Set and retrieved message from Redis: %s", message)

        return jsonify(message=message, user=user.__dict__)

    except Exception as e:
        logger.error("An error occurred while processing the request: %s", str(e))
        return jsonify(error="Internal Server Error"), 500
