# src\base\navigator.py
from selenium.webdriver.support.ui import WebDriverWait
from utils.chrome_utils import ChromeUtils
import logging
logger = logging.getLogger('BaseNavigator:')

class BaseNavigator(ChromeUtils):
    def __init__(self):             
        ChromeUtils.__init__(self, profile_directory='Profile 2')
        self.wait = WebDriverWait(self.driver, 30)
        self.wait_long = WebDriverWait(self.driver, 120)
        self.wait_extra_long = WebDriverWait(self.driver, 60*5)
        
    def open_page(self, url:str):
        try:
            self.driver.maximize_window()
            self.driver.get(url)
            
            logger.debug(f'Navigated to {url}')
        except Exception as e:
            logger.debug(f'Error starting driver: {e}')
            
    def teardown_driver(self):
        """Quit the Selenium WebDriver."""
        if self.driver:
            self.driver.quit()
            logger.debug('WebDriver closed.')
    