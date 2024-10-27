# main.py

# Libraries
from flask import Flask, request
from flask_jwt_extended import JWTManager
from redis import Redis

# Packages
from config import Config
from db_manager import init_db
from logger_setup import logger

# Blueprints Import
from routes.tests import tests
from routes.auth import auth

jwt = JWTManager()


def create_app(config_class=Config):
    """
    Creates app instance
    
    and returns app object
    """

    app = Flask(__name__) # Create app
    app.config.from_object(config_class) # Load config
    app.redis_client = Redis.from_url(app.config['REDIS_URL'])
    
    init_db(app) # Initiate database manager
    jwt.init_app(app) # Initiate jwt handler

    # Register all blueprints
    app.register_blueprint(tests) # Blueprint for beta functions
    app.register_blueprint(auth) # Authentication
    
    logger.info("Flask app initialized with config: %s", config_class)

    return app

app = create_app() # Create app

# Log requests
@app.before_request
def log_request_info():
    logger.info('Request: %s %s', request.method, request.url)

# Log errors
@app.errorhandler(Exception)
def handle_exception(e):
    logger.error("An error occurred: %s", str(e))
    return "Internal Server Error", 500

if __name__ == '__main__':
    logger.info("Starting Flask app on http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=True) # Debug version. Don't use on production
