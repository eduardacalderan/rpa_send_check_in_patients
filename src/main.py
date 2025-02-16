# src\main.py
import logging 
from configs.logging_config import setup_logging
from rpa.web_diet_integration import WebDietAutomation

from dotenv import load_dotenv

if __name__ == "__main__":
  load_dotenv()

  setup_logging()
  logger = logging.getLogger('main:')
  logger.debug('This is a test debug message')
  
  web_diet_automation = WebDietAutomation()  
  web_diet_automation.perform_tasks()

