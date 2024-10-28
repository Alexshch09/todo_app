# error_handlers.py
from flask import jsonify
from logger_setup import logger

def register_error_handlers(app):
    @app.errorhandler(405)
    def method_not_allowed(e):
        logger.info("405 error occurred: %s", str(e))
        return jsonify(error="Method Not Allowed"), 405

    @app.errorhandler(404)
    def not_found(e):
        logger.info("404 error occurred: %s", str(e))
        return jsonify(error="Not Found"), 404

    @app.errorhandler(Exception)
    def handle_exception(e):
        logger.error("An error occurred: %s", str(e), exc_info=True)
        return jsonify(error="Internal Server Error"), 500
