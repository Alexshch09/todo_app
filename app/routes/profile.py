from flask import Blueprint, jsonify, current_app, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from db.user import UserManager
from logger_setup import logger
from cloudinary.uploader import upload as cloudinary_upload

profile = Blueprint('profile', __name__)

@profile.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    """Fetch user data"""
    user_manager = UserManager(app=current_app)

    user_id = get_jwt_identity()

    try:
        user = user_manager.get_user_by_id(user_id)
        if user:
            logger.info("Retrieved user: %s", user_id)
            user_data = user.to_safe_dict()

            return jsonify(user=user_data)
        else:
            return jsonify(error="User not found")

    except Exception as e:
        logger.error("An error occurred while processing the request: %s", str(e))
        return jsonify(error="Internal Server Error"), 500
    

@profile.route('/user/<id>', methods=['GET'])
@jwt_required()
def get_user_by_id(id):
    """Fetch user data"""
    user_manager = UserManager(app=current_app)

    user_id = get_jwt_identity()

    try:
        user = user_manager.get_user_by_id(id)
        if user:
            logger.info("Retrieved user: %s", id)
            user_data = user.to_safe_dict()

            return jsonify(user=user_data)
        else:
            return jsonify(error="User not found")

    except Exception as e:
        logger.error("An error occurred while processing the request: %s", str(e))
        return jsonify(error="Internal Server Error"), 500


@profile.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    """Fetch all users."""
    user_manager = UserManager(app=current_app)
    
    try:
        users = user_manager.get_all_users()
        users_data = [user.to_safe_dict() for user in users]
        logger.info("Retrieved all users: %s", users_data)
        return jsonify(users=users_data), 200

    except Exception as e:
        logger.error("An error occurred while fetching users: %s", str(e))
        return jsonify(error="Internal Server Error"), 500


@profile.route('/user/upload_image', methods=['POST'])
@jwt_required()
def upload_profile_image():
    """Upload and update user profile image"""
    user_manager = UserManager(app=current_app)
    user_id = get_jwt_identity()

    if 'image' not in request.files:
        return jsonify(error="No image file found"), 400

    file = request.files['image']

    try:
        # Upload to Cloudinary
        upload_result = cloudinary_upload(
            file, 
            folder="profile_images/",
            transformation=[
                {'width': 64, 'height': 64},
            ])
        
        image_url = upload_result.get("secure_url")

        # Update user in the database with the new image URL
        updated_user = user_manager.update_user(user_id, image=image_url)

        logger.info("Profile image updated for user: %s", user_id)
        return jsonify(user=updated_user.to_safe_dict()), 200

    except Exception as e:
        logger.error("An error occurred while uploading the profile image: %s", str(e))
        return jsonify(error="Internal Server Error"), 500