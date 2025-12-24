import os
import pandas as pd
from datetime import datetime
from rega_schema import REGA_COLUMNS
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

CSV_PATH = "rega_data.csv"
JSON_KEY = "the-program-482110-e4-7ef9d425d794.json"
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1Ecmrq9JUhCerhq4mebO1Jtpw8sD_tTo-79_x3Jabr68"
WORKSHEET_NAME = "RegA"  # Production register worksheet

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

def get_data_local():
    """Load local CSV fallback"""
    if os.path.exists(CSV_PATH):
        try:
            return pd.read_csv(CSV_PATH)
        except Exception:
            return pd.DataFrame(columns=REGA_COLUMNS)
    return pd.DataFrame(columns=REGA_COLUMNS)

def get_data():
    """Load data - prioritized from Local CSV for speed"""
    return get_data_local()

def save_record(data_dict):
    """Save record to local CSV first, then attempt push using gspread"""
    df_local = get_data_local()
    
    # ID Generation
    if "rega_id" not in data_dict or not data_dict["rega_id"]:
        prefix = "RA-"
        count = len(df_local) + 1
        data_dict["rega_id"] = f"{prefix}{datetime.now().strftime('%Y%m')}{count:04d}"
    
    data_dict["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_dict["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 1. Update Local CSV (Always)
    new_row = pd.DataFrame([data_dict])
    df_local = pd.concat([df_local, new_row], ignore_index=True)
    df_local.to_csv(CSV_PATH, index=False)
    
    # 2. Attempt Sync
    sync_success = sync_to_gsheet(df_local)
    
    if sync_success:
        st.success("✅ Record saved locally AND synced to Google Sheets!")
    else:
        st.warning("⚠️ Record saved locally. Google Sheets sync failed - use manual sync button.")
            
    return data_dict["rega_id"]

def sync_to_gsheet(df):
    """Sync a dataframe to the Google Sheet using direct gspread"""
    client = get_google_client()
    if client:
        try:
            sh = client.open_by_url(SPREADSHEET_URL)
            
            # Try to get RegA worksheet, create if doesn't exist
            try:
                worksheet = sh.worksheet(WORKSHEET_NAME)
            except gspread.exceptions.WorksheetNotFound:
                worksheet = sh.add_worksheet(title=WORKSHEET_NAME, rows=1000, cols=len(REGA_COLUMNS))
            
            # Clean data
            df_str = df.astype(str)
            df_str = df_str.replace('nan', '')
            df_str = df_str.replace('NaN', '')
            df_str = df_str.replace('inf', '')
            df_str = df_str.replace('-inf', '')
            
            # Convert to list format
            cleaned_data = [df_str.columns.values.tolist()] + df_str.values.tolist()
            
            # Update sheet
            worksheet.clear()
            worksheet.update('A1', cleaned_data, value_input_option='USER_ENTERED')
            st.toast("✅ Synchronized with Google Sheets (Reg-A)")
            return True
        except Exception as e:
            st.sidebar.error(f"Sync failed: {e}")
            return False
    else:
        st.sidebar.warning("GSheet Sync Offline: No credentials found.")
        return False

def filter_records(date_from=None, batch_no=None, shift=None):
    """Filter records by various criteria"""
    df = get_data()
    if df is None or df.empty:
        return pd.DataFrame(columns=REGA_COLUMNS)
    
    if date_from:
        if 'production_date' in df.columns:
            df['production_date_dt'] = pd.to_datetime(df['production_date']).dt.date
            df = df[df['production_date_dt'] == date_from]
    
    if batch_no and batch_no != "All":
        if 'batch_no' in df.columns:
            df = df[df['batch_no'] == batch_no]
    
    if shift and shift != "All":
        if 'production_shift' in df.columns:
            df = df[df['production_shift'] == shift]
            
    return df

def get_available_batches():
    """Get batches from Reg-74 that are ready for production"""
    try:
        reg74_df = pd.read_csv("reg74_data.csv")
        
        if reg74_df.empty:
            return pd.DataFrame()
        
        # Filter for reduction/blending operations with available stock
        available = reg74_df[
            (reg74_df['operation_type'] == 'Reduction/Blending') |
            (reg74_df['operation_type'] == 'Transfer SST to BRT')
        ].copy()
        
        # Filter out batches with zero closing balance
        if 'closing_bl' in available.columns:
            available = available[available['closing_bl'] > 0]
        
        return available
    except Exception:
        return pd.DataFrame()

def get_brt_current_stock(brt_vat):
    """Get current stock for a specific BRT from Reg-74"""
    try:
        reg74_df = pd.read_csv("reg74_data.csv")
        
        if reg74_df.empty:
            return {"bl": 0.0, "al": 0.0, "strength": 0.0}
        
        # Filter records for this BRT
        brt_records = reg74_df[
            (reg74_df['source_vat'] == brt_vat) | 
            (reg74_df['destination_vat'] == brt_vat)
        ].sort_values('operation_date', ascending=False)
        
        if brt_records.empty:
            return {"bl": 0.0, "al": 0.0, "strength": 0.0}
        
        latest = brt_records.iloc[0]
        
        return {
            "bl": float(latest.get('closing_bl', 0) or 0),
            "al": float(latest.get('closing_al', 0) or 0),
            "strength": float(latest.get('closing_strength', 0) or 0)
        }
    except Exception:
        return {"bl": 0.0, "al": 0.0, "strength": 0.0}

def get_batch_details(batch_no):
    """Get batch details from Reg-74"""
    try:
        reg74_df = pd.read_csv("reg74_data.csv")
        
        if reg74_df.empty:
            return None
        
        # Find the batch
        batch_records = reg74_df[reg74_df['batch_no'] == batch_no]
        
        if batch_records.empty:
            return None
        
        # Get the latest record for this batch
        latest = batch_records.sort_values('operation_date', ascending=False).iloc[0]
        
        return {
            "batch_no": batch_no,
            "brt_vat": latest.get('destination_vat', ''),
            "bl": float(latest.get('closing_bl', 0) or 0),
            "al": float(latest.get('closing_al', 0) or 0),
            "strength": float(latest.get('closing_strength', 0) or 0),
            "operation_date": latest.get('operation_date', ''),
            "reg74_id": latest.get('reg74_id', '')
        }
    except Exception:
        return None

def calculate_production_wastage(mfm2_bl, mfm2_al, bottles_bl, bottles_al):
    """Calculate production wastage based on MFM2 vs Bottles"""
    wastage_bl = mfm2_bl - bottles_bl
    wastage_al = mfm2_al - bottles_al
    wastage_percentage = (wastage_al / mfm2_al * 100) if mfm2_al > 0 else 0
    
    allowable_limit = 0.1  # 0.1% of MFM2 AL
    
    return {
        "wastage_bl": wastage_bl,
        "wastage_al": wastage_al,
        "wastage_percentage": wastage_percentage,
        "within_limit": wastage_percentage <= allowable_limit,
        "critical": wastage_percentage > 1.0
    }

def get_batch_production_history(batch_no):
    """Get all production sessions for a batch"""
    df = get_data()
    if df.empty:
        return pd.DataFrame()
    
    return df[df['batch_no'] == batch_no].sort_values('production_date')

def get_next_session_number(batch_no):
    """Get the next session number for a batch"""
    history = get_batch_production_history(batch_no)
    if history.empty:
        return 1
    
    max_session = history['session_number'].max()
    return int(max_session) + 1 if pd.notna(max_session) else 1
