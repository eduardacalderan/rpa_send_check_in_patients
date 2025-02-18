# src\utils\retry_decorator_utils.py
import time
import logging

logger = logging.getLogger('retry_decorator_utils:')

def retry(exceptions, tries=3, delay=2, backoff=2):
  def decorator_retry(func):
    def wrapper_retry(*args, **kwargs):
      _tries, _delay = tries, delay
      while _tries > 1:
        try:
          return func(*args, **kwargs)
        except exceptions as e:
          logger.warning(f"{e}, Retrying in {_delay} seconds...")
          time.sleep(_delay)
          _tries -= 1
          _delay *= backoff
      return func(*args, **kwargs)
    return wrapper_retry
  return decorator_retry