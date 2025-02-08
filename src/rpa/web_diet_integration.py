# src\rpa\web_diet_integration.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import logging
import os 
from dotenv import load_dotenv

logger = logging.getLogger('web_diet_integration:')

class WebDietAutomation:
  def __init__(self):
    load_dotenv()
    self.driver = None

  def setup_driver(self):
    """Setup the Selenium WebDriver."""
    try:
      self.driver = webdriver.Chrome()  
      logger.debug('WebDriver initialized successfully.')
      return self.driver
    except Exception as e:
      logger.error(f'Error initializing WebDriver: {e}')
      raise

  def perform_tasks(self):
    """Perform a task using Selenium WebDriver."""
    try:
      self.driver = self.setup_driver()
      # Open the webdiet page
      self.open_web_diet()
      # Perform the login task on the webdiet page
      self.task_login_web_diet()
      
      # Add more tasks as needed
    except Exception as e:
      logger.error(f'Error performing task: {e}')
      raise
    finally:
      self.driver.quit()
      logger.debug('WebDriver closed.')
      
  def open_web_diet(self):
    try:
      self.driver.get('https://pt.webdiet.com.br/login/')
      logger.debug('Navigated to https://pt.webdiet.com.br/login/')
    except Exception as e:
      logger.error(f'Error opening webdiet: {e}')
      raise

  def task_login_web_diet(self):
    try:
      search_box = self.driver.find_element(By.NAME, 'user')
      search_box.send_keys(os.getenv('EMAIL_WEB_DIET') + Keys.TAB + os.getenv('PASSWORD_WEB_DIET') + Keys.RETURN)
      
      logger.debug('Logged in webdiet successfully.')
    except Exception as e:
      logger.error(f'Error login webdiet: {e}')
      raise