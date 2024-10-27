import psycopg2
from psycopg2.extras import RealDictCursor
from flask import current_app

class DBManager:
    def __init__(self, db_url):
        self.db_url = db_url
        self.conn = None

    def connect(self):
        if self.conn is None or self.conn.closed:
            self.conn = psycopg2.connect(self.db_url, cursor_factory=RealDictCursor)

    def close(self):
        if self.conn and not self.conn.closed:
            self.conn.close()

    def query(self, query, params=None, fetch_one=False):
        """Execute a query and return results."""
        self.connect()
        with self.conn.cursor() as cursor:
            cursor.execute(query, params)
            if fetch_one:
                return cursor.fetchone()
            return cursor.fetchall()

    def insert(self, query, params=None):
        """Execute an INSERT query and commit the changes."""
        self.connect()
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, params)
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()  # Откатить транзакцию в случае ошибки
            raise e  # Перекинем исключение для дальнейшей обработки

# Функция для инициализации DBManager в приложении Flask
def init_db(app):
    app.db_manager = DBManager(app.config['DATABASE_URL'])
