# src\utils\date_utils.py
import logging
import locale
from datetime import datetime, timedelta

logger = logging.getLogger('web_diet_integration:')

class Date:
  def get_last_thirty_days(self):
    """Get the last thirty days from today."""
    try:
      locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
      today = datetime.today()
      
      if Date.validate_monday():
        last_twenty_nine_days = today - timedelta(days=29)
        formatted_date_twenty_nine = last_twenty_nine_days.strftime('%d de %B de %Y')
        
        last_thirty_days = today - timedelta(days=30)
        formatted_date_thirty = last_thirty_days.strftime('%d de %B de %Y')
        
        last_thirty_one_days = today - timedelta(days=31)
        formatted_date_thirty_one = last_thirty_one_days.strftime('%d de %B de %Y')
        
        if formatted_date_twenty_nine[0].startswith('0'):
          formatted_date_twenty_nine = formatted_date_twenty_nine[1:]
        
        if formatted_date_thirty[0].startswith('0'):
          formatted_date_thirty = formatted_date_thirty[1:]

        if formatted_date_thirty_one[0].startswith('0'):
          formatted_date_thirty_one = formatted_date_thirty_one[1:]

        return formatted_date_thirty_one, formatted_date_thirty, formatted_date_twenty_nine
        
      last_thirty_days = today - timedelta(days=29)
      formatted_date = last_thirty_days.strftime('%d de %B de %Y')

      if formatted_date[0].startswith('0'):
        formatted_date = formatted_date[1:]
      
      return formatted_date
    except Exception as e:
      raise Exception(f'Error getting last thirty days: {e}')
  
  @staticmethod  
  def validate_monday():
    """Validate if today is Monday."""
    try:
      today = datetime.today()
      if today.weekday() == 0:
        return True
      return False
    except Exception as e:
      raise Exception(f'Error validating Monday: {e}')
  