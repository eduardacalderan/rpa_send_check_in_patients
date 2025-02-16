# src\base\navigator.py
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import logging
from dotenv import load_dotenv

logger = logging.getLogger('BaseNavigator:')
<<<<<<< webdiet-selenium-integration

class BaseNavigator:
    def __init__(self):
        load_dotenv()
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
=======
class BaseNavigator(ChromeUtils):
    def __init__(self):             
        ChromeUtils.__init__(self, profile_directory='Profile 2')
        self.wait = WebDriverWait(self.driver, 30)
>>>>>>> local
        self.wait_long = WebDriverWait(self.driver, 120)
        self.wait_extra_long = WebDriverWait(self.driver, 60*5)
        
    def teardown_driver(self):
        """Quit the Selenium WebDriver."""
        if self.driver:
            self.driver.quit()
            logger.debug('WebDriver closed.')