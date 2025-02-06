# src\configs\logging_config.py
import logging 
from datetime import datetime
import os 

def setup_logging():
  # Ensure the logs directory exists
  if not os.path.exists('logs'):
    os.makedirs('logs')
  # Define the log filename with the current date
  log_filename = f'logs/{datetime.today().strftime("%d_%m_%Y")}_logs.log'
  # Configure logging
  configure_logging(log_filename)
  # Create a console handler
  create_console_handler()
  
def configure_logging(log_filename):
  logging.basicConfig(
    format='%(asctime)s %(name)s %(message)s',
    datefmt='%d/%m/%Y %I:%M:%S %p',
    filename=log_filename,
    encoding='utf-8',
    level=logging.DEBUG
  )

def create_console_handler():
  console_handler = logging.StreamHandler()
  console_handler.setLevel(logging.DEBUG)
  console_handler.setFormatter(logging.Formatter('%(asctime)s %(name)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p'))
  # Add the console handler to the root logger
  logging.getLogger().addHandler(console_handler)
