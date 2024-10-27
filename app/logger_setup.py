# logger_setup.py
import os
import logging
from logging import StreamHandler, FileHandler
import pytz
from datetime import datetime


log_directory = './logs'
os.makedirs(log_directory, exist_ok=True)

class CustomFormatter(logging.Formatter):
    """Custom logging formatter to set timezone in logs."""
    def formatTime(self, record, datefmt=None):
        # Set the desired timezone
        timezone = pytz.timezone("Europe/Warsaw")
        dt = datetime.fromtimestamp(record.created, tz=timezone)
        return dt.strftime(datefmt or "%Y-%m-%d %H:%M:%S")

# Log file path
log_file_path = os.path.join(log_directory, 'app.log')
formatter = CustomFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# File handler setup
file_handler = FileHandler(log_file_path)
file_handler.setFormatter(formatter)

# Stream handler setup
stream_handler = StreamHandler()
stream_handler.setFormatter(formatter)

# Get the logger instance
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


logger.propagate = False
