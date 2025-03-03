# src\main.py
from datetime import datetime
import logging 
from configs.logging_config import setup_logging
from rpa.web_diet_integration import WebDietAutomation
from services.email_service import Email
from dotenv import load_dotenv
if __name__ == "__main__":
  if datetime.today().weekday() >= 5:  # 5 = Saturday, 6 = Sunday
    exit()
  else:  
    load_dotenv()

    setup_logging()
    logger = logging.getLogger('main:')
    logger.debug('This is a test debug message')
    web_diet_automation = WebDietAutomation()  
    email = Email()
    
    if web_diet_automation.perform_tasks():
      email.send_email('ENVIO CHECK-IN FINALIZADO, CONFERIR ARQUIVOS')
      exit()
    else:
      email.send_email('ERRO AO ENVIAR CHECK-IN, VERIFICAR ARQUIVOS/LOGS')
      exit()

