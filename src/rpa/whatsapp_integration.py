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
      logger.debug('Sending a message on WhatsApp.')
    except Exception as e:
      logger.error(f'Error sending message on WhatsApp: {e}')
      raise
      