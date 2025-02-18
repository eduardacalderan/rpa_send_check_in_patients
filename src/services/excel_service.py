# src\services\excel_service.py
import os 
import pandas as pd 

class ExcelService:
  def create_excel_with_phone_numbers(self, phone_number, date, status):
    file_path = f"already_processed_phones/phone_numbers_{date}.xlsx"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    if os.path.exists(file_path):
      df = pd.read_excel(file_path)
    else:
      df = pd.DataFrame(columns=["Phone Numbers", "Date", "Status"])

    new_entry = pd.DataFrame([[phone_number, date, status]], columns=["Phone Numbers", "Date", "Status"])
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_excel(file_path, index=False)
  
  def verify_phone_number_already_processed(self, phone_number, date):
    file_path = f"already_processed_phones/phone_numbers_{date}.xlsx"
    if os.path.exists(file_path):
      df = pd.read_excel(file_path)
      phone_number = str(phone_number).replace(" ", "").replace("+55", "").replace("-", "")
      if not df[(df['Phone Numbers'] == phone_number) & (df['Status'] == 'Sent')].empty:
          print(f"Phone number {phone_number} already processed.")
          return 'ALREADY_PROCESSED'
    return None