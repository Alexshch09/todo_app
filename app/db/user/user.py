from flask import current_app

class UserManager:
    def __init__(self, app):
        """Initialize UserManager with app context for database and Redis clients."""
        self.db_manager = app.db_manager
        self.redis = app.redis_client

    def get_user_by_id(self, user_id):
        """Fetch a user by ID from the database."""
        query = "SELECT * FROM users WHERE id = %s"
        params = (user_id,)
        
        try:
            user = self.db_manager.fetch_one(query, params=params)
            return user
        except Exception as e:
            current_app.logger.error(f"Error fetching user by ID: {e}")
            return {"error": "An error occurred while fetching the user"}, 500

    def create_user(self, name, email):
        """Insert a new user into the database."""
        query = "INSERT INTO users (name, email) VALUES (%s, %s)"
        params = (name, email)

        try:
            self.db_manager.insert(query, params=params)
            return {"message": "User added successfully"}, 201
        except Exception as e:
            current_app.logger.error(f"Error creating user: {e}")
            return {"error": "An error occurred while creating the user"}, 500
