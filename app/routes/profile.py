from flask import Blueprint, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from db.user import UserManager
from db.project import ProjectManager
from db.task import TaskManager
from logger_setup import logger

profile = Blueprint('profile', __name__)

@profile.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    """Fetch user data"""
    user_manager = UserManager(app=current_app)
    project_manager = ProjectManager(app=current_app)
    task_manager = TaskManager(app=current_app)

    user_id = get_jwt_identity()

    try:
        user = user_manager.get_user_by_id(user_id)
        if user:
            logger.info("Retrieved user: %s", user_id)
            user_data = user.to_safe_dict()

            projects = project_manager.get_projects_for_user(user_id)
            projects_data = []

            for project in projects:
                project_dict = project.to_dict()
                
                tasks = task_manager.get_tasks_for_user_in_project(user_id, project.id)
                tasks_data = [task.to_dict() for task in tasks]
                
                project_dict['tasks'] = tasks_data
                projects_data.append(project_dict)

            return jsonify(user=user_data, projects=projects_data)
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