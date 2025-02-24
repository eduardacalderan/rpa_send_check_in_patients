# src\utils\chrome_utils.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import os
class ChromeUtils:
  def __init__(self, profile_directory:str='Default'):
    self.option = webdriver.ChromeOptions()
    self.option.add_argument('--disable-notifications')
    self.option.add_argument('--mute-audio')
    self.option.add_argument('--no-sandbox')
    self.option.add_argument('--disable-dev-shm-usage')
    self.option.add_argument('--disable-browser-side-navigation')
    self.option.add_argument('--disable-gpu')
    self.option.add_argument('--new-window')
    self.option.add_argument('--disable-extensions')
    self.option.add_argument(f'user-data-dir={os.getenv("CHROME_USER_DATA_DIR")}')
    self.option.add_argument(f"--profile-directory={profile_directory}")
    self.driver = webdriver.Chrome(service=ChromeService(
    ChromeDriverManager().install()), options=self.option)
