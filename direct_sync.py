import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

CSV_PATH = "reg76_data.csv"
JSON_KEY = "the-program-482110-e4-7ef9d425d794.json"
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1Ecmrq9JUhCerhq4mebO1Jtpw8sD_tTo-79_x3Jabr68"

# Read CSV
df = pd.read_csv(CSV_PATH)
print(f"Loaded {len(df)} rows")

# AGGRESSIVE NaN cleaning - convert entire dataframe to strings first
df_str = df.astype(str)
df_str = df_str.replace('nan', '')
df_str = df_str.replace('NaN', '')
df_str = df_str.replace('inf', '')
df_str = df_str.replace('-inf', '')

# Convert to list format
cleaned_data = [df_str.columns.values.tolist()] + df_str.values.tolist()

print(f"Data prepared: {len(cleaned_data)} rows (including header)")

# Connect to GSheets
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

try:
    creds = Credentials.from_service_account_file(JSON_KEY, scopes=scopes)
    client = gspread.authorize(creds)
    print("Auth Success")
    
    sh = client.open_by_url(SPREADSHEET_URL)
    print(f"Opened spreadsheet: {sh.title}")
    
    worksheet = sh.get_worksheet(0)
    print(f"Accessed worksheet: {worksheet.title}")
    
    # Update sheet
    worksheet.update('A1', cleaned_data, value_input_option='USER_ENTERED')
    print("✅ SUCCESS! Data synced to Google Sheets")
    
except Exception as e:
    print(f"❌ FAILED: {e}")
    import traceback
    traceback.print_exc()
