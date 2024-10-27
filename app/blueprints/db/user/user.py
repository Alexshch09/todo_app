from flask import current_app

class UserManager:
    def __init__(self, app, user_id):
        self.db_manager = app.db_manager
        self.redis = app.redis_client
        self.user_id = user_id

    def get_user_by_id(self, a):
        query = "SELECT * FROM users WHERE id = %s"
        params = (self.user_id,)
        user = self.db_manager.query(query, params=params, fetch_one=True)
        return user

    def create_user(self, name, email):
        query = "INSERT INTO users (name, email) VALUES (%s, %s)"
        params = (name, email)

        try:
            self.db_manager.insert(query, params=params)
            return {"message": "User added successfully"}
        except Exception as e:
            return {"error": "Try Again"}, 500
