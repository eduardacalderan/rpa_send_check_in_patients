# src\services\excel_service.py
import os 
import pandas as pd 

class ExcelService:
  @staticmethod
  def create_excel_with_phone_numbers_and_names(self, phone_number, name, date, status):
    file_path = f"already_processed_phones/phone_numbers_{date}.xlsx"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    if os.path.exists(file_path):
      df = pd.read_excel(file_path)
    else:
      df = pd.DataFrame(columns=["Phone Numbers","Name", "Date", "Status"])

    phone_number = str(phone_number).replace(" ", "").replace("+55", "").replace("-", "")
    df['Phone Numbers'] = df['Phone Numbers'].astype(str)
    df['Name'] = df['Name'].astype(str)
    new_entry = pd.DataFrame([[phone_number, name, date, status]], columns=["Phone Numbers", "Name", "Date", "Status"])
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_excel(file_path, index=False)
  
  @staticmethod
  def verify_phone_number_already_processed(self, phone_number, date):
    file_path = f"already_processed_phones/phone_numbers_{date}.xlsx"
    if os.path.exists(file_path):
      df = pd.read_excel(file_path)
      phone_number = str(phone_number).replace(" ", "").replace("+55", "").replace("-", "")
      
      df['Phone Numbers'] = df['Phone Numbers'].astype(str)
      phone_number_already_processed = df.loc[df['Phone Numbers'] == phone_number]
      if not phone_number_already_processed.empty:
        if 'Sent' in phone_number_already_processed['Status'].values:
          print(f"Phone number {phone_number} already processed.")
          return 'ALREADY_PROCESSED'
    return None