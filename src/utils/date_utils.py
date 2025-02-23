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
      last_thirty_days = today - timedelta(days=29)
      formatted_date = last_thirty_days.strftime('%d de %B de %Y')
      return formatted_date
    except Exception as e:
      logger.error(f'Error getting last thirty days: {e}')
      raise
    
  def validate_monday(self):
    """Validate if today is Monday."""
    try:
      today = datetime.today()
      if today.weekday() == 0:
        return True
      return False
    except Exception as e:
      logger.error(f'Error validating Monday: {e}')
      raise
  