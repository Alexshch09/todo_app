from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from db.task import TaskManager
from logger_setup import logger

tasks = Blueprint('tasks', __name__)

@tasks.route('/tasks/project/<project_id>', methods=['GET'])
@jwt_required()
def get_user_projects(project_id):
    """Fetch all tasks for the authenticated user in specified project."""
    user_id = get_jwt_identity()
    task_manager = TaskManager(app=current_app)
    
    try:
        tasks = task_manager.get_tasks_for_user_in_project(user_id, project_id)
        tasks_data = [task.to_dict() for task in tasks]
        logger.info("Retrieved tasks for user: %s, in project: %s", user_id, project_id)
        return jsonify(tasks=tasks_data), 200
    except Exception as e:
        logger.error("An error occurred while fetching tasks: %s", str(e))
        return jsonify(error="Internal Server Error"), 500

@tasks.route('/tasks/project/<project_id>', methods=['POST'])
@jwt_required()
def create_project(project_id):
    """Create a new project for the authenticated user."""
    user_id = get_jwt_identity()
    data = request.get_json()
    title = data.get('title')
    task_manager = TaskManager(app=current_app)
    
    if not title:
        return jsonify(error="Task title is required"), 400
    
    try:
        task = task_manager.create_task(project_id=project_id, user_id=user_id, title=title)
        logger.info("Task created with ID: %s for user: %s", task.id, user_id)
        return jsonify(id=project_id), 201
    except Exception as e:
        logger.error("An error occurred while creating the project: %s", str(e))
        return jsonify(error="Internal Server Error"), 500

# @tasks.route('/tasks/<task_id>', methods=['PATCH'])
# @jwt_required()
# def update_project(task_id):
#     """Update the name of a specific project for the authenticated user."""
#     user_id = get_jwt_identity()
#     data = request.get_json()
#     new_name = data.get('name')
#     project_manager = ProjectManager(app=current_app)
    
#     if not new_name:
#         return jsonify(error="New project name is required"), 400

#     try:
#         project = project_manager.get_project_by_id(project_id)
#         if project and project.user_id == user_id:
#             project_manager.update_project(project_id, name=new_name)
#             logger.info("Project %s updated with new name for user: %s", project_id, user_id)
#             return jsonify(success=True), 200
#         else:
#             return jsonify(error="Project not found or access denied"), 404
#     except Exception as e:
#         logger.error("An error occurred while updating the project: %s", str(e))
#         return jsonify(error="Internal Server Error"), 500
    
# @tasks.route('/tasks/<task_id>', methods=['DELETE'])
# @jwt_required()
# def delete_project(task_id):
#     """Delete a specific project for the authenticated user."""
#     user_id = get_jwt_identity()
#     project_manager = ProjectManager(app=current_app)
    
#     try:
#         project = project_manager.get_project_by_id(project_id)
#         if project and project.user_id == user_id:
#             project_manager.delete_project(project_id)
#             logger.info("Project %s deleted for user: %s", project_id, user_id)
#             return jsonify(success=True), 200
#         else:
#             return jsonify(error="Project not found or access denied"), 404
#     except Exception as e:
#         logger.error("An error occurred while deleting the project: %s", str(e))
#         return jsonify(error="Internal Server Error"), 500
