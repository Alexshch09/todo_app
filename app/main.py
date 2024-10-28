# main.py

# Libraries
from flask import Flask, request
from flask_jwt_extended import JWTManager
from redis import Redis
import sentry_sdk
import cloudinary

# Packages
from config import Config
from db_manager import init_db
from logger_setup import logger
from error_handlers import register_error_handlers

# Blueprints Import
from routes.tests import tests
from routes.auth import auth
from routes.profile import profile

jwt = JWTManager()

def register_blueprints(app):
    """
    Registers Flask blueprints for route organization.
    """
    app.register_blueprint(tests)     # Blueprint for beta functions
    app.register_blueprint(auth)       # Authentication
    app.register_blueprint(profile) # Profile



def create_app(config_class=Config):
    """
    Creates app instance
    
    and returns app object
    """

    app = Flask(__name__) # Create app
    app.config.from_object(config_class) # Load config

    # Sentry for error tracking (Optional)
    if app.config.get("SENTRY_DSN"):
        sentry_sdk.init(
            dsn=app.config['SENTRY_DSN'],
            traces_sample_rate=1.0,
            _experiments={"continuous_profiling_auto_start": True},
        )
    
    cloudinary.config(
        cloud_name=app.config['CLOUDINARY_CLOUD_NAME'],
        api_key=app.config['CLOUDINARY_API_KEY'],
        api_secret=app.config['CLOUDINARY_API_SECRET']
    )

    app.redis_client = Redis.from_url(app.config['REDIS_URL'])
    
    init_db(app) # Initiate database manager
    jwt.init_app(app) # Initiate jwt handler

    # Register blueprints
    register_blueprints(app)

    # Register error handlers
    register_error_handlers(app)
    
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
