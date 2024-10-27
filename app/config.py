import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DATABASE_URL=os.environ.get('DATABASE_URL')
    REDIS_URL=os.environ.get('REDIS_URL')