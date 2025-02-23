# src\rpa\web_diet_integration.py
import os 
import time
from datetime import timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from base.navigator import BaseNavigator
from utils.date_utils import Date
from .whatsapp_integration import WhatsApp
from selenium.webdriver.support.ui import WebDriverWait
from services.excel_service import ExcelService
from utils.retry_decorator_utils import retry

import logging
logger = logging.getLogger('web_diet_integration:')

class WebDietAutomation(BaseNavigator, Date, WhatsApp):
  def __init__(self):
    super().__init__()
    
    self.wait = WebDriverWait(self.driver, 30)
    self.wait_long = WebDriverWait(self.driver, 120)

  @retry(Exception, tries=3, delay=2, backoff=2)
  def perform_tasks(self):
    """Perform a task using Selenium WebDriver."""
    try:
      # Open the webdiet page
      self.open_page(url='https://pt.webdiet.com.br/login/')
      # Perform the login task on the webdiet page
      self.task_login_web_diet()
      # Wait for the page to load
      self.task_waiting_for_loading()
      # Open the scheduling page
      self.task_open_schedule()
      # Send the check-in message
      self.task_send_check_in()
      
      self.teardown_driver()    
      return True
    except Exception as e:
      logger.error(f'Error performing task: {e}')
      raise
      
  def task_login_web_diet(self):
    try:  
      self.wait.until(EC.visibility_of_element_located((By.NAME, 'user'))).send_keys(Keys.CONTROL + 'a' + Keys.DELETE)    
      self.wait.until(EC.visibility_of_element_located((By.NAME, 'user'))).send_keys(os.getenv('EMAIL_WEB_DIET') + Keys.TAB + os.getenv('PASSWORD_WEB_DIET') + Keys.RETURN)
      
      logger.debug('Logged in webdiet successfully.')
    except Exception as e:
      logger.error(f'Error login webdiet: {e}')
      raise
    
  def task_waiting_for_loading(self):
    try:
      self.wait_long.until_not(EC.visibility_of_element_located((By.XPATH, '//div[@id="loadingPage"]')))
      logger.debug('Page loaded successfully.')
    except Exception as e:
      logger.error(f'Erorr waiting for loading: {e}')
      raise
    
  def task_open_schedule(self):
    try:      
      self.wait.until(EC.visibility_of_element_located((By.XPATH, '//div[contains(text(), "Consultório")]'))).click()
      
      self.wait.until(EC.visibility_of_element_located((By.XPATH, '//a[@href="agenda.php"]'))).click()
      self.task_waiting_for_loading()
      
      self.wait.until(EC.visibility_of_element_located((By.XPATH, '//div[text()="Visão geral"]'))).click()
      self.task_waiting_for_loading()
      
      self.wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@title="Mês"]'))).click()
      self.task_waiting_for_loading()
            
      logger.debug('Opened schedule successfully.')
    except Exception as e:
      logger.error(f'Error opening schedule: {e}')
      raise
    
  def task_send_check_in(self,):
    try:
      last_thirty_days = self.get_last_thirty_days()
      logger.debug(f'Searching for date: {last_thirty_days}')
      
      # Search for the last thirty days
      self.search_certain_date(last_thirty_days)
      # Open the patient scheduled in the last thirty days
      self.task_open_patient_scheduling_modal_and_send_message(last_thirty_days)
      # Send WhatsApp message
      logger.debug('Opened scheduling successfully.')
    except Exception as e:
      logger.error(f'Error opening scheduling: {e}')
      raise
    
  def search_certain_date(self, last_thirty_days):
    try:      
      search_for_date = self.driver.find_elements(By.XPATH, f'//a[@aria-label="{last_thirty_days}"]')
      while not search_for_date:
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@title="Anterior"]'))).click()
        self.task_waiting_for_loading()
        search_for_date = self.driver.find_elements(By.XPATH, f'//a[@aria-label="{last_thirty_days}"]')
      logger.debug(f'Found date: {last_thirty_days}')  
      
    except Exception as e:
      logger.error(f'Error searching for date: {e}')
      raise
    
  def task_open_patient_scheduling_modal_and_send_message(self, last_thirty_days):
    try:
      time.sleep(5)
      
      if not self.validate_monday():
        scheduled_patients = self.driver.find_elements(By.XPATH, f'//a[@aria-label="{last_thirty_days}"]//parent::div//following-sibling::div[1]//div//div[contains(@style, "background-color: #1e88e5") or contains(@style, "background-color: #54a0ff")]')
      else: 
        scheduled_patients = self.driver.find_elements(By.XPATH, f'//a[@aria-label="{last_thirty_days}" or @aria-label="{last_thirty_days - timedelta(days=30)}" or @aria-label="{last_thirty_days - timedelta(days=31)}"]//parent::div//following-sibling::div[1]//div//div[contains(@style, "background-color: #1e88e5") or contains(@style, "background-color: #54a0ff")]')  
        
      for scheduled_patient in scheduled_patients:      
        scheduled_patient.click()
        
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '//div[contains(text(), "solicitar confirmação")]'))).click()
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '''//div[@onclick="avisar('whatsapp_web')"]'''))).click()
        
        self.task_waiting_for_loading()
        
        
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '//select[@id="modeloMensagem"]'))).click()
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '//option[text()="Check-in"]'))).click()
        
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="swal2-content"]//div[@class="botao" and text()="confirmar"]'))).click()
        
        self.task_waiting_for_loading()
        
        # Switch to the new window opened by WhatsApp Web
        self.driver.switch_to.window(self.driver.window_handles[-1])
        logger.debug('Switched to WhatsApp Web window.')
        
        phone_number = self.get_phone_number_patient()
        phone_number = str(phone_number).replace(" ", "").replace("+55", "").replace("-", "")
        verify_phone_number_already_processed = ExcelService.verify_phone_number_already_processed(self, phone_number, last_thirty_days)
        if verify_phone_number_already_processed == 'ALREADY_PROCESSED':
          self.driver.close()
          self.driver.switch_to.window(self.driver.window_handles[0])
          continue
        
        # get whatsapp funtions .
        send_message = self.send_message()
        
        status_processed = ''
        if send_message == 'SUCCESS':
          status_processed = 'Sent'
        else: 
          status_processed = 'Not sent'
        ExcelService.create_excel_with_phone_numbers(self, phone_number, self.get_last_thirty_days(), status_processed)
        
        # Switch back to the original window
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        
        logger.debug('Switched back to the original window.')
        
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@title="Mês"]'))).click()

      logger.debug('Opened patients scheduling modal and sended messages successfully.')
    except Exception as e:
      logger.error(f'Error opening patient scheduling modal: {e}')
      raise
    
  def get_phone_number_patient(self):
    try:
      phone_number = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//p[contains(text(), "Conversar com")]//span'))).text
      logger.debug(f'Phone number: {phone_number}')

      return phone_number
    except Exception as e:
      logger.error(f'Error getting phone number: {e}')
      raise 