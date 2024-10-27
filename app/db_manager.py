import psycopg2
from psycopg2.extras import RealDictCursor
from flask import current_app

class DBManager:
    """Database manager for handling PostgreSQL connections and queries."""
    
    def __init__(self, db_url):
        """Initialize with the database URL."""
        self.db_url = db_url
        self.conn = None

    def __enter__(self):
        """Enter context for connection management."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit context and close the connection."""
        self.close()

    def connect(self):
        """Establish a connection to the database if not already connected."""
        if not self.conn or self.conn.closed:
            self.conn = psycopg2.connect(self.db_url, cursor_factory=RealDictCursor)

    def close(self):
        """Close the database connection if open."""
        if self.conn and not self.conn.closed:
            self.conn.close()

    def fetch_all(self, query, params=None):
        """Execute a SELECT query and return all results."""
        self.connect()
        with self.conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

    def fetch_one(self, query, params=None):
        """Execute a SELECT query and return a single result."""
        self.connect()
        with self.conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchone()

    def insert(self, query, params=None):
        """Execute an INSERT query and commit the changes."""
        self.connect()
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, params)
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()  # Rollback transaction on error
            raise e

# Initialize DBManager in Flask app context
def init_db(app):
    """Initialize DBManager instance for Flask app."""
    app.db_manager = DBManager(app.config['DATABASE_URL'])
