import psycopg2
from psycopg2.extras import RealDictCursor
from flask import current_app
from logger_setup import logger  # Импортируем ваш logger

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
            try:
                self.conn = psycopg2.connect(self.db_url, cursor_factory=RealDictCursor)
                logger.info("Database connection established.")
            except Exception as e:
                logger.critical("Failed to connect to database: %s", e)
                raise

    def close(self):
        """Close the database connection if open."""
        if self.conn and not self.conn.closed:
            self.conn.close()
            logger.info("Database connection closed.")

    def fetch_all(self, query, params=None):
        """Execute a SELECT query and return all results."""
        self.connect()
        try:
            with self.conn.cursor() as cursor:
                logger.debug("Executing query: %s with params: %s", query, params)
                cursor.execute(query, params)
                result = cursor.fetchall()
                logger.info("Query executed successfully.")
                return result
        except Exception as e:
            logger.error("Error executing fetch_all query: %s", e)
            raise

    def fetch_one(self, query, params=None):
        """Execute a SELECT query and return a single result."""
        self.connect()
        try:
            with self.conn.cursor() as cursor:
                logger.debug("Executing query: %s with params: %s", query, params)
                cursor.execute(query, params)
                result = cursor.fetchone()
                logger.info("Query executed successfully.")
                return result
        except Exception as e:
            logger.error("Error executing fetch_one query: %s", e)
            raise

    def insert(self, query, params=None):
        """Execute an INSERT query and commit the changes."""
        self.connect()
        try:
            with self.conn.cursor() as cursor:
                logger.debug("Executing insert query: %s with params: %s", query, params)
                cursor.execute(query, params)
                self.conn.commit()
                logger.info("Insert query committed successfully.")
        except Exception as e:
            self.conn.rollback()
            logger.error("Error executing insert query: %s. Rolled back.", e)
            raise e

# Initialize DBManager in Flask app context
def init_db(app):
    """Initialize DBManager instance for Flask app."""
    app.db_manager = DBManager(app.config['DATABASE_URL'])
    logger.info("DBManager initialized with DATABASE_URL: %s", app.config['DATABASE_URL'])
