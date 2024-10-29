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

@tasks.route('/tasks/<task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    """Update an existing task for the authenticated user."""
    user_id = get_jwt_identity()
    data = request.get_json()

    # Extract fields from the request
    title = data.get('title')
    description = data.get('description')
    color = data.get('color')
    deadline = data.get('deadline')

    task_manager = TaskManager(app=current_app)

    try:
        # Update the task
        task_manager.update_task(task_id, title=title, description=description, color=color, deadline=deadline)
        logger.info("Task %s updated for user: %s", task_id, user_id)
        return jsonify(message="Task updated successfully"), 200
    except Exception as e:
        logger.error("An error occurred while updating task %s: %s", task_id, str(e))
        return jsonify(error="Internal Server Error"), 500


@tasks.route('/tasks/<task_id>/complete', methods=['PATCH'])
@jwt_required()
def complete_task(task_id):
    """Mark a task as completed for the authenticated user."""
    user_id = get_jwt_identity()
    task_manager = TaskManager(app=current_app)

    try:
        task_manager.complete_task(task_id)
        logger.info("Task %s marked as completed for user: %s", task_id, user_id)
        return jsonify(message="Task marked as completed"), 200
    except Exception as e:
        logger.error("An error occurred while completing task %s: %s", task_id, str(e))
        return jsonify(error="Internal Server Error"), 500


@tasks.route('/tasks/<task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    """Delete a task for the authenticated user."""
    user_id = get_jwt_identity()
    task_manager = TaskManager(app=current_app)

    try:
        task_manager.delete_task(task_id)
        logger.info("Task %s deleted for user: %s", task_id, user_id)
        return jsonify(message="Task deleted successfully"), 204
    except Exception as e:
        logger.error("An error occurred while deleting task %s: %s", task_id, str(e))
        return jsonify(error="Internal Server Error"), 500