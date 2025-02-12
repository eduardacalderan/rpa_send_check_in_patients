# src\base\navigator.py
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import logging
from dotenv import load_dotenv

logger = logging.getLogger('BaseNavigator:')

class BaseNavigator:
    def __init__(self):
        load_dotenv()
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        self.wait_long = WebDriverWait(self.driver, 120)
        
    def teardown_driver(self):
        """Quit the Selenium WebDriver."""
        if self.driver:
            self.driver.quit()
            logger.debug('WebDriver closed.')