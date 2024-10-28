from flask import current_app

from logger_setup import logger

class User:
    def __init__(self, id, username, email, password, image=None):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.image = image

    def __repr__(self):
        return f"<User id={self.id} username={self.username} email={self.email}>"

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data['id'],
            username=data['username'],
            email=data['email'],
            password=data['password'],
            image=data.get('image')
        )


class UserManager:
    def __init__(self, app):
        self.db_manager = app.db_manager

    def get_user_by_id(self, user_id):
        query = "SELECT * FROM users WHERE id = %s"
        try:
            user_data = self.db_manager.fetch_one(query, (user_id,))
            return User.from_dict(user_data) if user_data else None
        except Exception as e:
            logger.error(f"Error fetching user by ID: {e}")
            raise

    def get_all_users(self):
        query = "SELECT * FROM users"
        try:
            users_data = self.db_manager.fetch_all(query)
            return [User.from_dict(user) for user in users_data]
        except Exception as e:
            logger.error(f"Error fetching all users: {e}")
            raise
