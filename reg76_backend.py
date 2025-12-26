import os
import pandas as pd
from datetime import datetime
from schema import COLUMNS
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import gspread
from google.oauth2.service_account import Credentials

CSV_PATH = "reg76_data.csv"
JSON_KEY = "the-program-482110-e4-7ef9d425d794.json"
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1Ecmrq9JUhCerhq4mebO1Jtpw8sD_tTo-79_x3Jabr68"

def get_google_client():
    """Returns a direct gspread client using service account"""
    try:
        if os.path.exists(JSON_KEY):
            scopes = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]
            creds = Credentials.from_service_account_file(JSON_KEY, scopes=scopes)
            return gspread.authorize(creds)
    except Exception as e:
        st.error(f"GSpread Auth Error: {e}")
    return None

def get_gsheet_connection():
    """Fallback for reading using st.connection"""
    try:
        if os.path.exists(JSON_KEY):
            return st.connection("gsheets", type=GSheetsConnection, service_account=JSON_KEY)
        return st.connection("gsheets", type=GSheetsConnection)
    except Exception:
        return None

def get_data_local():
    """Load local CSV fallback"""
    if os.path.exists(CSV_PATH):
        try:
            df = pd.read_csv(CSV_PATH)
            # Remove empty rows (rows where all values are NaN or empty)
            df = df.dropna(how='all')
            # Remove rows where reg76_id is empty/NaN
            if 'reg76_id' in df.columns:
                df = df[df['reg76_id'].notna()]
                df = df[df['reg76_id'].astype(str).str.strip() != '']
            return df
        except Exception as e:
            st.error(f"Error reading CSV: {e}")
            return pd.DataFrame(columns=COLUMNS)
    return pd.DataFrame(columns=COLUMNS)

def get_data():
    """Load data - prioritized from Local CSV for speed, sync handled separately"""
    # For this app, we trust local CSV as the source of truth, 
    # and use GSheet as a replica/backup.
    return get_data_local()

def save_record(data_dict):
    """Save record to local CSV first, then attempt push using gspread"""
    df_local = get_data_local()
    
    # ID Generation
    if "reg76_id" not in data_dict or not data_dict["reg76_id"]:
        prefix = "R76-"
        count = len(df_local) + 1
        data_dict["reg76_id"] = f"{prefix}{datetime.now().strftime('%Y%m')}{count:03d}"
    
    data_dict["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 1. Update Local CSV (Always)
    new_row = pd.DataFrame([data_dict])
    df_local = pd.concat([df_local, new_row], ignore_index=True)
    df_local.to_csv(CSV_PATH, index=False)
    
    # 2. Attempt Sync and show result
    sync_success = sync_to_gsheet(df_local)
    
    if sync_success:
        st.success("✅ Record saved locally AND synced to Google Sheets!")
    else:
        st.warning("⚠️ Record saved locally. Google Sheets sync failed - use manual sync button.")
            
    return data_dict["reg76_id"]

def delete_record(reg76_id):
    """Delete a record from both local CSV and Google Sheets"""
    try:
        # 1. Delete from local CSV
        df_local = get_data_local()
        
        if df_local.empty:
            return False, "No records found in local storage"
        
        # Check if record exists
        if reg76_id not in df_local['reg76_id'].values:
            return False, f"Record {reg76_id} not found"
        
        # Remove the record
        df_local = df_local[df_local['reg76_id'] != reg76_id]
        
        # Save back to CSV
        df_local.to_csv(CSV_PATH, index=False)
        
        # 2. Sync to Google Sheets
        sync_success = sync_to_gsheet(df_local)
        
        if sync_success:
            return True, "✅ Record deleted from both local storage and Google Sheets"
        else:
            return True, "⚠️ Record deleted locally, but Google Sheets sync failed"
            
    except Exception as e:
        return False, f"Error deleting record: {str(e)}"

def clear_all_data():
    """Clear all data from both CSV and Google Sheets - USE WITH CAUTION"""
    try:
        # Create empty dataframe with columns
        empty_df = pd.DataFrame(columns=COLUMNS)
        
        # Save empty CSV
        empty_df.to_csv(CSV_PATH, index=False)
        
        # Sync to Google Sheets
        sync_success = sync_to_gsheet(empty_df)
        
        if sync_success:
            return True, "✅ All data cleared from both local storage and Google Sheets"
        else:
            return True, "⚠️ Local data cleared, but Google Sheets sync failed"
            
    except Exception as e:
        return False, f"Error clearing data: {str(e)}"

def sync_to_gsheet(df):
    """Sync a dataframe to the Google Sheet using direct gspread"""
    client = get_google_client()
    if client:
        try:
            sh = client.open_by_url(SPREADSHEET_URL)
            worksheet = sh.get_worksheet(0) # Get first sheet
            
            # AGGRESSIVE NaN cleaning - convert entire dataframe to strings first
            df_str = df.astype(str)
            df_str = df_str.replace('nan', '')
            df_str = df_str.replace('NaN', '')
            df_str = df_str.replace('inf', '')
            df_str = df_str.replace('-inf', '')
            
            # Convert to list format
            cleaned_data = [df_str.columns.values.tolist()] + df_str.values.tolist()
            
            # Clear the sheet first
            worksheet.clear()
            
            # Update sheet
            worksheet.update('A1', cleaned_data, value_input_option='USER_ENTERED')
            st.toast("✅ Synchronized with Google Sheets")
            return True
        except Exception as e:
            st.sidebar.error(f"Sync failed: {e}")
            return False
    else:
        st.sidebar.warning("GSheet Sync Offline: No credentials found.")
        return False

def filter_records(date_from=None, tanker_no=None):
    df = get_data()
    if df is None or df.empty:
        return pd.DataFrame(columns=COLUMNS)
    
    if date_from:
        if 'created_at' in df.columns:
            df['created_at_dt'] = pd.to_datetime(df['created_at']).dt.date
            df = df[df['created_at_dt'] == date_from]
    
    if tanker_no:
        if 'vehicle_no' in df.columns:
            df = df[df['vehicle_no'].str.contains(tanker_no, case=False, na=False)]
            
    return df
