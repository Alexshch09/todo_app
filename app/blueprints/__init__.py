from flask import Flask
from .tests.routes import tests

def register_blueprints(app: Flask):
    app.register_blueprint(tests)
