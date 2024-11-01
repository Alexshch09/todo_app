from flask import current_app
from datetime import datetime

from logger_setup import logger

class Task:
    def __init__(self, id, project_id, user_id, title, description, color, is_completed, created_at, deadline):
        self.id = id
        self.project_id = project_id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.color = color
        self.is_completed = is_completed
        self.created_at = created_at
        self.deadline = deadline

    def __repr__(self):
        return f"<Task id={self.id} title={self.title}>"
    
    def to_dict(self):
        """Convert the Task instance to a dictionary."""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "color": self.color,
            "is_completed": self.is_completed,
            "created_at": self.created_at,
            "deadline": self.deadline
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data['id'],
            project_id=data['project_id'],
            user_id=data['user_id'],
            title=data['title'],
            description=data.get('description'),
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
    
    def get_tasks_for_user_in_project(self, user_id, project_id):
        query = "SELECT * FROM tasks WHERE user_id = %s AND project_id = %s"
        try:
            tasks_data = self.db_manager.fetch_all(query, (user_id, project_id))
            return [Task.from_dict(task) for task in tasks_data]
        except Exception as e:
            logger.error(f"Error fetching tasks for user in project: {e}")
            raise

    def get_tasks_for_user(self, user_id):
        query = "SELECT * FROM tasks WHERE user_id = %s"
        try:
            tasks_data = self.db_manager.fetch_all(query, (user_id,))
            return [Task.from_dict(task) for task in tasks_data]
        except Exception as e:
            logger.error(f"Error fetching tasks for user: {e}")
            raise

    def create_task(self, project_id, user_id, title, description="", steps="[]", color="#ff0000", is_completed=False, created_at=None, deadline=None):
        """Create a new task and insert it into the database."""

        now = datetime.now()
        timestamp = now.strftime("%a, %d %b %Y %H:%M:%S GMT")

        query = """
        INSERT INTO tasks (project_id, user_id, title, description, color, is_completed, created_at, deadline)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
        """
        values = (project_id, user_id, title, description, color, is_completed, timestamp, deadline)


        try:
            # Insert task and fetch the generated ID
            task_id = self.db_manager.insert_returning_id(query, values)
            logger.info(f"Task {task_id} created successfully.")
            return Task(
                id=task_id,
                project_id=project_id,
                user_id=user_id,
                title=title,
                description=description,
                color=color,
                is_completed=is_completed,
                created_at=now,
                deadline=deadline
            )
        except Exception as e:
            logger.error(f"Error creating task: {e}")
            raise

    def update_task(self, task_id, **kwargs):
        columns = ', '.join(f"{key} = %s" for key in kwargs)
        values = tuple(kwargs.values()) + (task_id,)
        query = f"UPDATE tasks SET {columns} WHERE id = %s"
        try:
            self.db_manager.insert(query, values)
            logger.info(f"Task {task_id} updated successfully.")
        except Exception as e:
            logger.error(f"Error updating task {task_id}: {e}")
            raise

    def complete_task(self, task_id):
        query = "UPDATE tasks SET is_completed = TRUE WHERE id = %s"
        try:
            self.db_manager.insert(query, (task_id,))
            logger.info(f"Task {task_id} marked as completed.")
        except Exception as e:
            logger.error(f"Error completing task {task_id}: {e}")
            raise

    def delete_task(self, task_id):
        query = "DELETE FROM tasks WHERE id = %s"
        try:
            self.db_manager.insert(query, (task_id,))
            logger.info(f"Task {task_id} deleted successfully.")
        except Exception as e:
            logger.error(f"Error deleting task {task_id}: {e}")
            raise
