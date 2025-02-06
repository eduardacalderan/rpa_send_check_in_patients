# src\main.py
from configs.logging_config import setup_logging
import logging 

if __name__ == "__main__":
  setup_logging()
  logger = logging.getLogger('main')
  logger.debug('This is a test debug message')
