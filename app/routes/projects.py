from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from db.project import ProjectManager
from logger_setup import logger

projects = Blueprint('projects', __name__)

@projects.route('/projects', methods=['GET'])
@jwt_required()
def get_user_projects():
    """Fetch all projects for the authenticated user."""
    user_id = get_jwt_identity()
    project_manager = ProjectManager(app=current_app)
    
    try:
        projects = project_manager.get_projects_for_user(user_id)
        projects_data = [project.to_dict() for project in projects]
        logger.info("Retrieved projects for user: %s", user_id)
        return jsonify(projects=projects_data), 200
    except Exception as e:
        logger.error("An error occurred while fetching projects: %s", str(e))
        return jsonify(error="Internal Server Error"), 500

@projects.route('/projects', methods=['POST'])
@jwt_required()
def create_project():
    """Create a new project for the authenticated user."""
    user_id = get_jwt_identity()
    data = request.get_json()
    name = data.get('name')
    icon = data.get('icon')
    color = data.get('color')
    project_manager = ProjectManager(app=current_app)
    
    if not name:
        return jsonify(error="Project name is required"), 400
    
    try:
        project_id = project_manager.create_project(user_id, name, icon=icon, color=color)
        logger.info("Project created with ID: %s for user: %s", project_id, user_id)
        return jsonify(id=project_id), 201
    except Exception as e:
        logger.error("An error occurred while creating the project: %s", str(e))
        return jsonify(error="Internal Server Error"), 500

@projects.route('/projects/<project_id>', methods=['PATCH'])
@jwt_required()
def update_project(project_id):
    """Update the name of a specific project for the authenticated user."""
    user_id = get_jwt_identity()
    data = request.get_json()
    new_name = data.get('name')
    project_manager = ProjectManager(app=current_app)
    
    if not new_name:
        return jsonify(error="New project name is required"), 400

    try:
        project = project_manager.get_project_by_id(project_id)
        if project and project.user_id == user_id:
            project_manager.update_project(project_id, name=new_name)
            logger.info("Project %s updated with new name for user: %s", project_id, user_id)
            return jsonify(success=True), 200
        else:
            return jsonify(error="Project not found or access denied"), 404
    except Exception as e:
        logger.error("An error occurred while updating the project: %s", str(e))
        return jsonify(error="Internal Server Error"), 500
    
@projects.route('/projects/<project_id>', methods=['DELETE'])
@jwt_required()
def delete_project(project_id):
    """Delete a specific project for the authenticated user."""
    user_id = get_jwt_identity()
    project_manager = ProjectManager(app=current_app)
    
    try:
        project = project_manager.get_project_by_id(project_id)
        if project and project.user_id == user_id:
            project_manager.delete_project(project_id)
            logger.info("Project %s deleted for user: %s", project_id, user_id)
            return jsonify(success=True), 200
        else:
            return jsonify(error="Project not found or access denied"), 404
    except Exception as e:
        logger.error("An error occurred while deleting the project: %s", str(e))
        return jsonify(error="Internal Server Error"), 500
