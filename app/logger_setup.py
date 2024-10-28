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

# Get the current date for log file naming
current_date = datetime.now(pytz.timezone("Europe/Warsaw")).strftime('%Y-%m-%d')
log_file_path = os.path.join(log_directory, f'app_{current_date}.log')
formatter = CustomFormatter('%(asctime)s | %(levelname)s | %(pathname)s:%(lineno)d - %(message)s')

# File handler setup
file_handler = FileHandler(log_file_path)
file_handler.setFormatter(formatter)

# Stream handler setup
stream_handler = StreamHandler()
stream_handler.setFormatter(formatter)

# Get the logger instance
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

logger.propagate = False
