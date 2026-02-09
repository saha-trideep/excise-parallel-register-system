import os
import sqlite3
import pandas as pd
from datetime import datetime
from schema import COLUMNS
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import gspread
from google.oauth2.service_account import Credentials
import desktop_storage  # New desktop storage module
from reg76_sqlite_schema import CREATE_REG76_TABLE, CREATE_REG76_INDEXES

CSV_PATH = "backup_data/reg76_data.csv"
DB_PATH = "excise_registers.db"
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

def init_sqlite_db():
    """Initialize SQLite database and tables if they don't exist"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.executescript(CREATE_REG76_TABLE)
        cursor.executescript(CREATE_REG76_INDEXES)
        conn.commit()
        conn.close()
    except Exception as e:
        st.error(f"SQLite initialization error: {e}")

def get_data_from_sqlite():
    """Load data from SQLite database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM reg76_receipts ORDER BY date_receipt DESC", conn)
        conn.close()
        return df
    except Exception as e:
        st.warning(f"SQLite read error: {e}")
        return pd.DataFrame(columns=COLUMNS)

def save_to_sqlite(data_dict):
    """Save record to SQLite database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Prepare column names and values
        columns = list(data_dict.keys())
        placeholders = ', '.join(['?' for _ in columns])
        column_names = ', '.join(columns)
        values = [data_dict[col] for col in columns]
        
        # Insert or replace record
        query = f"INSERT OR REPLACE INTO reg76_receipts ({column_names}) VALUES ({placeholders})"
        cursor.execute(query, values)
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"SQLite save error: {e}")
        return False

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
    """Load data - prioritized from SQLite database"""
    # SQLite is now the primary source of truth
    init_sqlite_db()  # Ensure tables exist
    return get_data_from_sqlite()

def save_record(data_dict):
    """Save record to SQLite (primary), Desktop Excel (presentation), CSV (backup), and Google Sheets (sync)"""
    
    # Generate ID if not present
    if "reg76_id" not in data_dict or not data_dict["reg76_id"]:
        prefix = "R76-"
        count = len(get_data()) + 1
        data_dict["reg76_id"] = f"{prefix}{datetime.now().strftime('%Y%m')}{count:04d}"
    
    # Add timestamps
    data_dict["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_dict["status"] = data_dict.get("status", "draft")
    record_id = data_dict["reg76_id"]
    
    # 1. Save to SQLite (PRIMARY STORAGE)
    init_sqlite_db()  # Ensure tables exist
    success_sqlite = save_to_sqlite(data_dict)
    
    if not success_sqlite:
        st.error("❌ Failed to save to SQLite database!")
        return None
    
    # 2. Save to Desktop Excel (PRESENTATION LAYER)
    try:
        success_excel, message_excel, _ = desktop_storage.add_record_to_excel(data_dict)
        if not success_excel:
            st.warning(f"⚠️ Desktop Excel save failed: {message_excel}")
    except Exception as e:
        st.warning(f"⚠️ Desktop Excel save failed: {e}")
    
    # 3. Save to Local CSV (BACKUP)
    try:
        df_local = get_data_local()
        new_row = pd.DataFrame([data_dict])
        df_local = pd.concat([df_local, new_row], ignore_index=True)
        df_local.to_csv(CSV_PATH, index=False)
    except Exception as e:
        st.warning(f"⚠️ CSV backup failed: {e}")
    
    # 4. Sync to Google Sheets (OPTIONAL SYNC)
    try:
        df_sqlite = get_data_from_sqlite()
        sync_success = sync_to_gsheet(df_sqlite)
    except Exception as e:
        sync_success = False
        st.warning(f"⚠️ Google Sheets sync failed: {e}")
    
    # --- AUTOMATION HOOKS ---
    try:
        # Auto-generate Reg-78 Daily Synopsis
        import reg78_backend
        from datetime import datetime as dt
        target_date = dt.strptime(data_dict["date_receipt"], "%Y-%m-%d").date()
        synopsis_data = reg78_backend.generate_daily_synopsis(target_date)
        if synopsis_data:
            synopsis_data["synopsis_date"] = str(target_date)
            reg78_backend.save_record(synopsis_data)
            st.info("📊 Reg-78 Daily Synopsis auto-updated!")
        
        # 2. Auto-generate Daily Handbook PDF
        try:
            from handbook_generator_v2 import EnhancedHandbookGenerator
            EnhancedHandbookGenerator(target_date).generate_handbook()
            st.info("📑 Daily Handbook auto-generated!")
        except Exception as e:
            st.warning(f"⚠️ Handbook generation failed: {e}")
    except Exception as e:
        st.warning(f"⚠️ Automation hooks failed: {e}")
    # -------------------------
    
    # Success message
    if sync_success:
        st.success(f"✅ Record saved to SQLite AND synced to Google Sheets!\n📁 SQLite ID: {record_id}")
    else:
        st.success(f"✅ Record saved to SQLite!\n📁 SQLite ID: {record_id}")
        st.info("ℹ️ Google Sheets sync failed - use manual sync button if needed.")
            
    return record_id

def delete_record(reg76_id):
    """Delete a record from Desktop Excel, CSV, and Google Sheets"""
    try:
        # 1. Delete from Desktop Excel (PRIMARY)
        success_excel, message_excel = desktop_storage.delete_record_from_excel(reg76_id)
        
        if not success_excel:
            return False, message_excel
        
        # 2. Delete from local CSV (BACKUP)
        try:
            df_local = get_data_local()
            if not df_local.empty and reg76_id in df_local['reg76_id'].values:
                df_local = df_local[df_local['reg76_id'] != reg76_id]
                df_local.to_csv(CSV_PATH, index=False)
        except Exception as e:
            pass  # CSV is backup, don't fail if it errors
        
        # 3. Sync to Google Sheets
        df_excel = desktop_storage.get_data_from_excel()
        sync_success = sync_to_gsheet(df_excel)
        
        if sync_success:
            return True, f"✅ Record deleted from Desktop Excel and synced to Google Sheets"
        else:
            return True, f"⚠️ Record deleted from Desktop Excel, but Google Sheets sync failed"
            
    except Exception as e:
        return False, f"Error deleting record: {str(e)}"

def clear_all_data():
    """Clear all data from Desktop Excel, CSV, and Google Sheets - USE WITH CAUTION"""
    try:
        # 1. Clear Desktop Excel (PRIMARY)
        success_excel, message_excel = desktop_storage.clear_all_excel_data()
        
        if not success_excel:
            return False, message_excel
        
        # 2. Clear CSV (BACKUP)
        try:
            empty_df = pd.DataFrame(columns=COLUMNS)
            empty_df.to_csv(CSV_PATH, index=False)
        except Exception as e:
            pass  # CSV is backup
        
        # 3. Sync to Google Sheets
        empty_df = pd.DataFrame(columns=COLUMNS)
        sync_success = sync_to_gsheet(empty_df)
        
        if sync_success:
            return True, "✅ All data cleared from Desktop Excel and Google Sheets"
        else:
            return True, "⚠️ Desktop Excel cleared, but Google Sheets sync failed"
            
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
