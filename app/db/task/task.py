from flask import current_app

from logger_setup import logger

class Task:
    def __init__(self, id, project_id, user_id, title, description, steps, color, is_completed, created_at, deadline):
        self.id = id
        self.project_id = project_id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.steps = steps
        self.color = color
        self.is_completed = is_completed
        self.created_at = created_at
        self.deadline = deadline

    def __repr__(self):
        return f"<Task id={self.id} title={self.title}>"

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data['id'],
            project_id=data['project_id'],
            user_id=data['user_id'],
            title=data['title'],
            description=data.get('description'),
            steps=data.get('steps'),
            color=data.get('color'),
            is_completed=data.get('is_completed', False),
            created_at=data.get('created_at'),
            deadline=data.get('deadline')
        )


class TaskManager:
    def __init__(self, app):
        self.db_manager = app.db_manager

    def get_task_by_id(self, task_id):
        query = "SELECT * FROM tasks WHERE id = %s"
        try:
            task_data = self.db_manager.fetch_one(query, (task_id,))
            return Task.from_dict(task_data) if task_data else None
        except Exception as e:
            logger.error(f"Error fetching task by ID: {e}")
            raise
