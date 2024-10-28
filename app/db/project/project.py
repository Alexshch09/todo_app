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
