# src\rpa\whatsapp_integration.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import logging 

logger = logging.getLogger('web_diet_integration:')
class WhatsApp():
    
  def send_message(self):
    try:      
      self.wait.until(EC.visibility_of_element_located((By.XPATH, '//a[@title="Compartilhe no WhatsApp"]'))).click()
      self.wait.until(EC.visibility_of_element_located((By.XPATH, '//a//span[text()="usar o WhatsApp Web"]'))).click()
      self.wait_extra_long.until(EC.visibility_of_element_located((By.XPATH, '//button[@aria-label="Enviar"]'))).click()
      
      verify_message_status = self.verify_message_status()
      if verify_message_status == 'SUCCESS':
        logger.debug('Sending a message on WhatsApp.')
        return 'SUCCESS'
      else:
        return 'ERROR'
    except Exception as e:
      logger.error(f'Error sending message on WhatsApp: {e}')
      raise
  
  def verify_message_status(self) -> str:
    try:
      
      sended_message = self.wait_long.until(EC.visibility_of_element_located((By.XPATH, '//span[contains(@aria-label, "Enviada")]')))
      self.verify_success_status_check(sended_message)
      
      delivered_message = self.wait_long.until(EC.visibility_of_element_located((By.XPATH, '//span[contains(@aria-label, "Entregue")]')))
      self.verify_success_status_check(delivered_message)
     
      read_message = self.wait_long.until(EC.visibility_of_element_located((By.XPATH, '//span[contains(@aria-label, "Lida")]')))
      self.verify_success_status_check(read_message)
      
      logger.debug('Message not sent successfully.')
      return 'ERROR'
    except Exception as e:
      logger.error(f'Error verifying message status: {e}')
      raise
  
  def verify_success_status_check(status_required) -> str | None:
    if status_required:
      logger.debug('Message sent successfully.')
      return 'SUCCESS'