import psycopg2
from psycopg2.extras import RealDictCursor
from flask import current_app
from logger_setup import logger

def with_transaction(func):
    """Decorator to ensure automatic rollback on transaction errors."""
    def wrapper(self, *args, **kwargs):
        self.connect()
        try:
            result = func(self, *args, **kwargs)
            self.conn.commit()
            return result
        except Exception as e:
            self.conn.rollback()
            logger.error("Transaction error in %s: %s. Rolled back.", func.__name__, e)
            raise e
    return wrapper

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

    @with_transaction
    def fetch_all(self, query, params=None):
        """Execute a SELECT query and return all results."""
        with self.conn.cursor() as cursor:
            logger.debug("Executing query: %s with params: %s", query, params)
            cursor.execute(query, params)
            result = cursor.fetchall()
            logger.info("Query executed successfully.")
            return result

    @with_transaction
    def fetch_one(self, query, params=None):
        """Execute a SELECT query and return a single result."""
        with self.conn.cursor() as cursor:
            logger.debug("Executing query: %s with params: %s", query, params)
            cursor.execute(query, params)
            result = cursor.fetchone()
            logger.info("Query executed successfully.")
            return result

    @with_transaction
    def insert(self, query, params=None):
        """Execute an INSERT query and commit the changes."""
        with self.conn.cursor() as cursor:
            logger.debug("Executing insert query: %s with params: %s", query, params)
            cursor.execute(query, params)
            logger.info("Insert query committed successfully.")

    @with_transaction
    def insert_returning_id(self, query, params=None):
        """Execute an INSERT query and return the generated ID."""
        with self.conn.cursor() as cursor:
            logger.debug("Executing insert query: %s with params: %s", query, params)
            cursor.execute(query, params)
            generated_id = cursor.fetchone()['id']  # Предполагаем, что возвращается id
            logger.info("Insert query committed successfully. Generated ID: %s", generated_id)
            return generated_id


# Initialize DBManager in Flask app context
def init_db(app):
    """Initialize DBManager instance for Flask app."""
    app.db_manager = DBManager(app.config['DATABASE_URL'])
    logger.info("DBManager initialized with DATABASE_URL: %s", app.config['DATABASE_URL'])
