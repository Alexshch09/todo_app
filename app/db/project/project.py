from flask import current_app

from logger_setup import logger

class Project:
    def __init__(self, id, user_id, name, icon=None, color=None):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.icon = icon
        self.color = color

    def __repr__(self):
        return f"<Project id={self.id} name={self.name}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'icon': self.icon,
            'color': self.color
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data['id'],
            user_id=data['user_id'],
            name=data['name'],
            icon=data.get('icon'),
            color=data.get('color')
        )


class ProjectManager:
    def __init__(self, app):
        self.db_manager = app.db_manager

    def get_project_by_id(self, project_id):
        query = "SELECT * FROM projects WHERE id = %s"
        try:
            project_data = self.db_manager.fetch_one(query, (project_id,))
            return Project.from_dict(project_data) if project_data else None
        except Exception as e:
            logger.error(f"Error fetching project by ID: {e}")
            raise
    
    def get_projects_for_user(self, user_id):
        query = "SELECT * FROM projects WHERE user_id = %s"
        try:
            projects_data = self.db_manager.fetch_all(query, (user_id,))
            return [Project.from_dict(project) for project in projects_data]
        except Exception as e:
            logger.error(f"Error fetching projects for user: {e}")
            raise

    def create_project(self, user_id, name, icon=None, color=None):
        query = """
        INSERT INTO projects (user_id, name, icon, color)
        VALUES (%s, %s, %s, %s) RETURNING id
        """
        try:
            project_id = self.db_manager.fetch_one(query, (user_id, name, icon, color))['id']
            logger.info(f"Project {project_id} created successfully.")
            return project_id
        except Exception as e:
            logger.error(f"Error creating project: {e}")
            raise

    def update_project(self, project_id, **kwargs):
        columns = ', '.join(f"{key} = %s" for key in kwargs)
        values = tuple(kwargs.values()) + (project_id,)
        query = f"UPDATE projects SET {columns} WHERE id = %s"
        try:
            self.db_manager.insert(query, values)
            logger.info(f"Project {project_id} updated successfully.")
        except Exception as e:
            logger.error(f"Error updating project {project_id}: {e}")
            raise

    def delete_project(self, project_id):
        query = "DELETE FROM projects WHERE id = %s"
        try:
            self.db_manager.insert(query, (project_id,))
            logger.info(f"Project {project_id} deleted successfully.")
        except Exception as e:
            logger.error(f"Error deleting project {project_id}: {e}")
            raise