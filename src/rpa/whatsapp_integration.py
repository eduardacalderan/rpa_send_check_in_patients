# src\rpa\whatsapp_integration.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils.retry_decorator_utils import retry
import time
import logging 
logger = logging.getLogger('whatsapp_integration:')

class WhatsApp():
  
  def send_message(self):
    try:      
      self.wait.until(EC.visibility_of_element_located((By.XPATH, '//a[@title="Partilhar no WhatsApp"]'))).click()
      self.wait.until(EC.visibility_of_element_located((By.XPATH, '//a//span[text()="utilize o WhatsApp Web"]'))).click()
      
      self.wait.until_not(EC.visibility_of_element_located((By.XPATH, '//progress')))
      time.sleep(5)
      invalid_phone = self.driver.find_elements(By.XPATH, '//div[contains(text(), "O número de telefone compartilhado por url é inválido.")]')
      if invalid_phone:
        logger.error('Invalid phone number.')
        return 'ERROR'
      
      self.wait_extra_long.until(EC.visibility_of_element_located((By.XPATH, '//button[@aria-label="Enviar"]'))).click()
      
      time.sleep(5)
      
      verify_message_status = self.verify_message_status()
      if verify_message_status == 'SUCCESS':
        logger.debug('Sending a message on WhatsApp.')
        return 'SUCCESS'
      else:
        return 'ERROR'
    except Exception as e:
      logger.error(f'Error sending message on WhatsApp: {e}')
  
  @retry(Exception, tries=3, delay=2, backoff=2)
  def verify_message_status(self) -> str:
    try:
      
      sended_message = self.driver.find_elements(By.XPATH, '//span[contains(@aria-label, "Enviada")]')
      if len(sended_message) > 0:
        logger.debug('Message sent successfully.')
        return 'SUCCESS'
      
      delivered_message = self.driver.find_elements(By.XPATH, '//span[contains(@aria-label, "Entregue")]')
      if len(delivered_message) > 0:
        logger.debug('Message sent successfully.')
        return 'SUCCESS'
    
      read_message = self.driver.find_elements(By.XPATH, '//span[contains(@aria-label, "Lida")]')
      if len(read_message) > 0:
        logger.debug('Message sent successfully.')
        return 'SUCCESS'
      
      error_to_send_message = self.driver.find_elements(By.XPATH, '//span[contains(@data-icon, "error")]')
      if error_to_send_message:
        error_to_send_message[0].click()
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '//div[contains(text(), "Tentar novamente")]//ancestor::button'))).click()

      
      logger.debug('Message not sent successfully.')
      return 'ERROR'
    except Exception as e:
      raise Exception(f'Error verifying message status: {e}')