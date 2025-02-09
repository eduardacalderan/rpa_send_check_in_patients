# src\rpa\web_diet_integration.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import os 
from dotenv import load_dotenv

from utils.date_utils import Date

logger = logging.getLogger('web_diet_integration:')

class WebDietAutomation:
  def __init__(self):
    load_dotenv()
    self.driver = webdriver.Chrome()  
    self.wait = WebDriverWait(self.driver, 10)
    self.wait_long = WebDriverWait(self.driver, 120)
    
    
  def perform_tasks(self):
    """Perform a task using Selenium WebDriver."""
    try:
      # Open the webdiet page
      self.open_web_diet()
      # Perform the login task on the webdiet page
      self.task_login_web_diet()
      # Wait for the page to load
      self.task_waiting_for_loading()
      # Open the scheduling page
      self.task_open_schedule()
      # Wait for the page to load
      self.task_waiting_for_loading()
      
      #  Add more tasks as needed
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
    
  def task_waiting_for_loading(self):
    try:
      self.wait_long.until_not(EC.visibility_of_element_located((By.XPATH, '//div[@id="loadingPage"]')))
      logger.debug('Page loaded successfully.')
    except Exception as e:
      logger.error(f'Error waiting for loading: {e}')
  
  def task_open_schedule(self):
    try:
      office_button = self.driver.find_element(By.XPATH, '//div[contains(text(), "Consultório")]')
      office_button.click()
      
      schedule_link = self.driver.find_element(By.XPATH, '//a[@href="agenda.php"]')
      schedule_link.click() 
      
      self.task_waiting_for_loading()
      
      month_button = self.driver.find_element(By.XPATH, '//button[@title="Mês"]')
      month_button.click()
      
      self.task_waiting_for_loading()
      
      overview = self.driver.find_element(By.XPATH, '//div[text()="Visão geral"]')
      overview.click()
      
      self.task_waiting_for_loading()
      logger.debug('Opened schedule successfully.')
    except Exception as e:
      logger.error(f'Error opening schedule: {e}')
      raise
    
  def task_send_check_in(self):
    try:
      # Search for the last thirty days
      self.search_certain_date()
      # Open the patient scheduled in the last thirty days
      self.open_patient_scheduling_modal()
      # Send WhatsApp message
      logger.debug('Opened scheduling successfully.')
    except Exception as e:
      logger.error(f'Error opening scheduling: {e}')
      raise
  
  def search_certain_date(self):
    try:
      last_thirty_days = Date.get_last_thirty_days()
      logger.debug(f'Searching for date: {last_thirty_days}')
      
      search_for_date = self.driver.find_element(By.XPATH, f'//a[@aria-label="{last_thirty_days}"]')
      while not search_for_date:
        overview = self.driver.find_element(By.XPATH, '//button[@title="Anterior"')
        overview.click()
        self.task_waiting_for_loading()
        search_for_date = self.driver.find_element(By.XPATH, f'//a[@aria-label="{last_thirty_days}"]')
      logger.debug(f'Found date: {last_thirty_days}')  
      
    except Exception as e:
      logger.error(f'Error searching for date: {e}')
      raise
  
  def open_patient_scheduling_modal(self):
    try:
      scheduled_patients = self.driver.find_elements(By.XPATH, '//a[@aria-label="4 de fevereiro de 2025"]//parent::div//following-sibling::div[1]//div//div[contains(@style, "background-color: #1e88e5")]')
            
      for scheduled_patient in scheduled_patients:
        scheduled_patient.click()
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '//div[contains(text(), "solicitar confirmação")]'))).click()
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '''//div[@onclick="avisar('whatsapp_web')"]'''))).click()
        
        self.task_waiting_for_loading()
        
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '//select[@id="modeloMensagem"]'))).click()
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '//option[text()="Check-in"]'))).click()
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="swal2-content"]//div[@class="botao" and text()="confirmar"]'))).click()
        
        self.task_waiting_for_loading()
      logger.debug('Opened patient scheduling modal successfully.')
    except Exception as e:
      logger.error(f'Error opening patient scheduling modal: {e}')
      raise                                     