from flask import Flask
from config import Config
from redis import Redis
from blueprints import register_blueprints
from db_manager import init_db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.redis_client = Redis.from_url(app.config['REDIS_URL'])
    
    init_db(app)

    # Регистрируем все blueprints
    register_blueprints(app)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
