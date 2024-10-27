# main.py
from flask import Flask, request
from config import Config
from redis import Redis
from routes.tests import tests
from db_manager import init_db
from logger_setup import logger

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.redis_client = Redis.from_url(app.config['REDIS_URL'])
    
    init_db(app)

    app.register_blueprint(tests)
    
    logger.info("Flask app initialized with config: %s", config_class)

    return app

app = create_app()

@app.before_request
def log_request_info():
    logger.info('Request: %s %s', request.method, request.url)

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error("An error occurred: %s", str(e))
    return "Internal Server Error", 500

if __name__ == '__main__':
    logger.info("Starting Flask app on http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
