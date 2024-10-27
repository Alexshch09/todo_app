from . import tests
from flask import jsonify, current_app
from ..db.user.user import UserManager

@tests.route('/')
def index():
    redis_client = current_app.redis_client
    user_manager = UserManager(app=current_app, user_id=2)

    user = user_manager.get_user_by_id(1)


    redis_client.set("hello_keyt", "Hello from Redis!2121")
    message = redis_client.get("hello_keyt").decode("utf-8")

    return jsonify(message=message, user=user)









# from . import example_bp
# from flask import jsonify, current_app, request
# from ..db.user.user import UserManager

# user_manager = UserManager(current_app.db_manager)

# @example_bp.route('/user/<int:user_id>', methods=['GET'])
# def get_user(user_id):
#     user = user_manager.get_user_by_id(user_id)
#     if user:
#         return jsonify(user=user)
#     return jsonify(error="User not found"), 404

# @example_bp.route('/add_user', methods=['GET'])
# def add_user():
#     name = request.args.get('name')
#     email = request.args.get('email')
#     if not name or not email:
#         return jsonify(error="Missing name or email"), 400

#     user_response = user_manager.create_user(name, email)
#     return jsonify(user_response), 201

