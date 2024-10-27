from flask import Blueprint

tests = Blueprint('tests', __name__)

from . import routes  # Импортируйте роуты, чтобы они были подключены
