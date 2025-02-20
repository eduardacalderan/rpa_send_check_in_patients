# src\rpa\whatsapp_integration.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils.retry_decorator_utils import retry
import logging 
logger = logging.getLogger('whatsapp_integration:')
class WhatsApp():
  
  def send_message(self):
    try:      
      self.wait.until(EC.visibility_of_element_located((By.XPATH, '//a[@title="Compartilhe no WhatsApp"]'))).click()
      self.wait.until(EC.visibility_of_element_located((By.XPATH, '//a//span[text()="usar o WhatsApp Web"]'))).click()
      
      self.wait.until_not(EC.visibility_of_element_located((By.XPATH, '//progress')))
      
      invalid_phone = self.driver.find_elements(By.XPATH, '//div[contains(text(), "O número de telefone compartilhado por url é inválido.")]')
      if invalid_phone:
        logger.error('Invalid phone number.')
        return 'ERROR'
      
      self.wait_extra_long.until(EC.visibility_of_element_located((By.XPATH, '//button[@aria-label="Enviar"]'))).click()
      
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
      
      logger.debug('Message not sent successfully.')
      return 'ERROR'
    except Exception as e:
      logger.error(f'Error verifying message status: {e}')
      raise