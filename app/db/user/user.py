from flask import current_app

# Define the User class
class User:
    """A class representing a user with basic attributes."""

    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

    def __repr__(self):
        return f"<User id={self.id} name={self.name} email={self.email}>"

    @classmethod
    def from_dict(cls, data):
        """Create a User instance from a dictionary."""
        return cls(id=data['id'], name=data['name'], email=data['email'])


# Update the UserManager class to return User instances
class UserManager:
    """
    User manager
    ---

    Manages user-related database operations.
    """
    def __init__(self, app):
        """Initialize UserManager with app context for database and Redis clients."""
        self.db_manager = app.db_manager
        self.redis = app.redis_client

    def get_user_by_id(self, user_id):
        """Fetch a user by ID from the database and return as a User instance."""
        query = "SELECT * FROM users WHERE id = %s"
        params = (user_id,)

        try:
            user_data = self.db_manager.fetch_one(query, params=params)
            return User.from_dict(user_data) if user_data else None
        except Exception as e:
            current_app.logger.error(f"Error fetching user by ID: {e}")
            return {"error": "An error occurred while fetching the user"}, 500

    def get_all_users(self):
        """Fetch all users from the database and return as a list of User instances."""
        query = "SELECT * FROM users"
        
        try:
            users_data = self.db_manager.fetch_all(query)
            return [User.from_dict(user) for user in users_data]
        except Exception as e:
            current_app.logger.error(f"Error fetching users: {e}")
            return {"error": "An error occurred while fetching users"}, 500

    def create_user(self, name, email):
        """Insert a new user into the database."""
        query = "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id"
        params = (name, email)

        try:
            self.db_manager.insert(query, params=params)
            user_data = self.db_manager.fetch_one("SELECT * FROM users WHERE email = %s", (email,))
            return User.from_dict(user_data), 201
        except Exception as e:
            current_app.logger.error(f"Error creating user: {e}")
            return {"error": "An error occurred while creating the user"}, 500
