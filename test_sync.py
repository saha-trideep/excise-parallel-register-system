import gspread
from google.oauth2.service_account import Credentials
import os
import traceback

JSON_KEY = "the-program-482110-e4-7ef9d425d794.json"
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1Ecmrq9JUhCerhq4mebO1Jtpw8sD_tTo-79_x3Jabr68"

def test_connection():
    if not os.path.exists(JSON_KEY):
        print(f"ERROR: {JSON_KEY} not found")
        return

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    try:
        print("Starting Auth...")
        creds = Credentials.from_service_account_file(JSON_KEY, scopes=scopes)
        client = gspread.authorize(creds)
        print("Auth Success")
        
        print(f"Opening URL: {SPREADSHEET_URL}")
        sh = client.open_by_url(SPREADSHEET_URL)
        print(f"Opened spreadsheet: {sh.title}")
        
        worksheet = sh.get_worksheet(0)
        print(f"Accessed worksheet: {worksheet.title}")
        
    except Exception:
        traceback.print_exc()

if __name__ == "__main__":
    test_connection()
