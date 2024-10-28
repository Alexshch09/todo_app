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
    
    def to_safe_dict(self):
        """Return a dictionary representation of the user without sensitive information."""
        return {
            'id': self.id,
            'username': self.username,
            'image': self.image
        }


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

    def create_user(self, username, email, password, image=None):
        """Create a new user in the database."""
        query = """
            INSERT INTO users (username, email, password, image)
            VALUES (%s, %s, %s, %s)
            RETURNING *
        """
        try:
            user_data = self.db_manager.fetch_one(query, (username, email, password, image))
            logger.info(f"User created successfully with email: {email}")
            return User.from_dict(user_data)
        except Exception as e:
            logger.error(f"Error creating user with email {email}: {e}")
            raise

    def update_user(self, user_id, **kwargs):
        """Update a user's information."""
        columns = ', '.join(f"{key} = %s" for key in kwargs)
        values = tuple(kwargs.values()) + (user_id,)
        query = f"UPDATE users SET {columns} WHERE id = %s RETURNING *"
        try:
            user_data = self.db_manager.fetch_one(query, values)
            logger.info(f"User {user_id} updated successfully.")
            return User.from_dict(user_data)
        except Exception as e:
            logger.error(f"Error updating user {user_id}: {e}")
            raise

    def update_password(self, user_id, new_password):
        """Update a user's password."""
        query = "UPDATE users SET password = %s WHERE id = %s"
        try:
            self.db_manager.insert(query, (new_password, user_id))
            logger.info(f"Password updated successfully for user {user_id}.")
        except Exception as e:
            logger.error(f"Error updating password for user {user_id}: {e}")
            raise

    def delete_user(self, user_id):
        """Delete a user from the database."""
        query = "DELETE FROM users WHERE id = %s"
        try:
            self.db_manager.insert(query, (user_id,))
            logger.info(f"User {user_id} deleted successfully.")
        except Exception as e:
            logger.error(f"Error deleting user {user_id}: {e}")
            raise
