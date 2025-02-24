# src\services\email_service.py
from datetime import datetime
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

from utils.date_utils import Date
class Email(Date): 
  
  def __init__(self):
    Date().__init__()
    
  def send_email(self, subject):
    subject = subject
    body = "Please find the attached logs files."
    
    last_thirty_days = self.get_last_thirty_days()
    attachment_paths = [
      f'already_processed_phones/phone_numbers_{last_thirty_days}.xlsx',
      f'logs/{datetime.today().strftime("%d_%m_%Y")}_logs.log'
    ]

    for attachment_path in attachment_paths:
      self.config_send_email(subject, body, attachment_path)

  def config_send_email(self, subject, body, attachment_path=None):
    msg = MIMEMultipart()
    msg['From'] = os.getenv('SENDER_EMAIL')
    msg['To'] = os.getenv('RECIPIENT_EMAIL')
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    if attachment_path:
      part = MIMEBase('application', 'octet-stream')
      part.set_payload(open(attachment_path, 'rb').read())
      encoders.encode_base64(part)
      part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(attachment_path)}"')
      msg.attach(part)

    server = smtplib.SMTP(os.getenv('SMTP_SERVER'), os.getenv('SMTP_PORT'))
    server.starttls()
    server.login(os.getenv('SENDER_EMAIL'), os.getenv('SENDER_EMAIL_PW'))
    server.sendmail(os.getenv('SENDER_EMAIL'), os.getenv('RECIPIENT_EMAIL'), msg.as_string())
    server.quit()
