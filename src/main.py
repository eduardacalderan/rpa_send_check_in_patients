# src\main.py
from configs.logging_config import setup_logging
import logging 

from rpa.web_diet_integration import WebDietAutomation

if __name__ == "__main__":
  setup_logging()
  logger = logging.getLogger('main:')
  logger.debug('This is a test debug message')
  
  web_diet_automation = WebDietAutomation()
  web_diet_automation.perform_tasks()

