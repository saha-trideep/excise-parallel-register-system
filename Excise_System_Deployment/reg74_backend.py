import os
import sqlite3
import pandas as pd
from datetime import datetime
from reg74_schema import REG74_COLUMNS
import streamlit as st
try:
    from streamlit_gsheets import GSheetsConnection
    GSHEETS_AVAILABLE = True
except ImportError:
    GSHEETS_AVAILABLE = False
    
try:
    import gspread
    from google.oauth2.service_account import Credentials
    GSPREAD_AVAILABLE = True
except ImportError:
    GSPREAD_AVAILABLE = False

import desktop_storage  # New desktop storage module
from reg74_sqlite_schema import CREATE_REG74_TABLE, CREATE_REG74_INDEXES

CSV_PATH = "backup_data/reg74_data.csv"
DB_PATH = "excise_registers.db"
JSON_KEY = "the-program-482110-e4-7ef9d425d794.json"
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1Ecmrq9JUhCerhq4mebO1Jtpw8sD_tTo-79_x3Jabr68"
WORKSHEET_NAME = "Reg74"  # Different worksheet for Reg-74

def get_google_client():
    """Returns a direct gspread client using service account"""
    if not GSPREAD_AVAILABLE:
        return None
        
    try:
        # Try Streamlit secrets first (for Streamlit Cloud)
        if "gsheets_credentials" in st.secrets:
            scopes = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]
            creds = Credentials.from_service_account_info(
                st.secrets["gsheets_credentials"],
                scopes=scopes
            )
            return gspread.authorize(creds)
        # Fallback to local JSON file
        elif os.path.exists(JSON_KEY):
            scopes = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]
            creds = Credentials.from_service_account_file(JSON_KEY, scopes=scopes)
            return gspread.authorize(creds)
    except Exception as e:
        st.warning(f"Google Sheets not available: {e}. Using local CSV.")
    return None

def init_sqlite_db():
    """Initialize SQLite database and tables if they don't exist"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.executescript(CREATE_REG74_TABLE)
        cursor.executescript(CREATE_REG74_INDEXES)
        conn.commit()
        conn.close()
    except Exception as e:
        st.error(f"SQLite initialization error: {e}")

def get_data_from_sqlite():
    """Load data from SQLite database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM reg74_operations ORDER BY operation_date DESC", conn)
        conn.close()
        return df
    except Exception as e:
        st.warning(f"SQLite read error: {e}")
        return pd.DataFrame(columns=REG74_COLUMNS)

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
        query = f"INSERT OR REPLACE INTO reg74_operations ({column_names}) VALUES ({placeholders})"
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
            return pd.read_csv(CSV_PATH)
        except Exception:
            return pd.DataFrame(columns=REG74_COLUMNS)
    return pd.DataFrame(columns=REG74_COLUMNS)

def get_data():
    """Load data - prioritized from SQLite database"""
    # SQLite is now the primary source of truth
    init_sqlite_db()  # Ensure tables exist
    return get_data_from_sqlite()

def save_record(data_dict):
    """Save record to SQLite (primary), Desktop Excel (presentation), CSV (backup), and Google Sheets (sync)"""
    
    # 1. Generate ID and set timestamps if missing
    if "reg74_id" not in data_dict or not data_dict["reg74_id"]:
        prefix = "R74-"
        count = len(get_data()) + 1
        data_dict["reg74_id"] = f"{prefix}{datetime.now().strftime('%Y%m')}{count:04d}"
        
    data_dict["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_dict["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_dict["status"] = data_dict.get("status", "draft")
    record_id = data_dict["reg74_id"]
    
    # 2. Save to SQLite (PRIMARY STORAGE)
    init_sqlite_db()
    success_sqlite = save_to_sqlite(data_dict)
    
    if not success_sqlite:
        st.error("❌ Failed to save to SQLite database!")
        return None

    # 3. Save to Desktop Excel (PRESENTATION LAYER)
    try:
        success_excel, message_excel, _ = desktop_storage.add_reg74_record_to_excel(data_dict)
        if not success_excel:
            st.warning(f"⚠️ Desktop Excel save failed: {message_excel}")
    except Exception as e:
        st.warning(f"⚠️ Desktop Excel save failed: {e}")
        
    # 4. Save to Local CSV (BACKUP)
    try:
        df_local = get_data_local()
        new_row = pd.DataFrame([data_dict])
        df_local = pd.concat([df_local, new_row], ignore_index=True)
        df_local.to_csv(CSV_PATH, index=False)
    except Exception as e:
        st.warning(f"⚠️ CSV backup failed: {e}")
    
    # 5. Sync to Google Sheets (OPTIONAL SYNC)
    sync_success = False
    try:
        df_sqlite = get_data_from_sqlite()
        sync_success = sync_to_gsheet(df_sqlite)
    except Exception as e:
        st.warning(f"⚠️ Google Sheets sync failed: {e}")
        
    # --- AUTOMATION HOOKS ---
    try:
        # Auto-generate Reg-78 Daily Synopsis
        import reg78_backend
        from datetime import datetime as dt
        target_date = dt.strptime(data_dict["operation_date"], "%Y-%m-%d").date()
        synopsis_data = reg78_backend.generate_daily_synopsis(target_date)
        if synopsis_data:
            synopsis_data["synopsis_date"] = str(target_date)
            reg78_backend.save_record(synopsis_data)
            st.info("📊 Reg-78 Daily Synopsis auto-updated!")

        # Auto-update Spirit Transaction daily summary
        try:
            import spirit_transaction_backend
            spirit_transaction_backend.refresh_for_date(target_date)
            st.info("📈 Spirit Transaction auto-updated!")
        except Exception as e:
            st.warning(f"⚠️ Spirit Transaction update failed: {e}")
        
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

    if sync_success:
        st.success(f"✅ Record saved to SQLite AND synced to Google Sheets!\n📁 SQLite ID: {record_id}")
    else:
        st.success(f"✅ Record saved to SQLite!\n📁 SQLite ID: {record_id}")
        st.info("ℹ️ Google Sheets sync failed - use manual sync button if needed.")
            
    return record_id

def sync_to_gsheet(df):
    """Sync a dataframe to the Google Sheet using direct gspread"""
    client = get_google_client()
    if client:
        try:
            sh = client.open_by_url(SPREADSHEET_URL)
            
            # Try to get Reg74 worksheet, create if doesn't exist
            try:
                worksheet = sh.worksheet(WORKSHEET_NAME)
            except gspread.exceptions.WorksheetNotFound:
                worksheet = sh.add_worksheet(title=WORKSHEET_NAME, rows=1000, cols=len(REG74_COLUMNS))
            
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
            st.toast("✅ Synchronized with Google Sheets (Reg-74)")
            return True
        except Exception as e:
            st.sidebar.error(f"Sync failed: {e}")
            return False
    else:
        st.sidebar.warning("GSheet Sync Offline: No credentials found.")
        return False

def filter_records(date_from=None, operation_type=None, vat_no=None):
    """Filter records by various criteria"""
    df = get_data()
    if df is None or df.empty:
        return pd.DataFrame(columns=REG74_COLUMNS)
    
    if date_from:
        if 'operation_date' in df.columns:
            df['operation_date_dt'] = pd.to_datetime(df['operation_date']).dt.date
            df = df[df['operation_date_dt'] == date_from]
    
    if operation_type and operation_type != "All":
        if 'operation_type' in df.columns:
            df = df[df['operation_type'] == operation_type]
    
    if vat_no and vat_no != "All":
        if 'source_vat' in df.columns or 'destination_vat' in df.columns:
            df = df[(df['source_vat'] == vat_no) | (df['destination_vat'] == vat_no)]
            
    return df

def get_vat_current_stock(vat_no):
    """Get current stock for a specific VAT from latest closing balance"""
    df = get_data()
    if df.empty:
        return {"bl": 0.0, "al": 0.0, "strength": 0.0}
    
    # Filter records for this VAT
    vat_records = df[
        (df['source_vat'] == vat_no) | 
        (df['destination_vat'] == vat_no)
    ].sort_values('operation_date', ascending=False)
    
    if vat_records.empty:
        return {"bl": 0.0, "al": 0.0, "strength": 0.0}
    
    latest = vat_records.iloc[0]
    
    return {
        "bl": float(latest.get('closing_bl', 0) or 0),
        "al": float(latest.get('closing_al', 0) or 0),
        "strength": float(latest.get('closing_strength', 0) or 0)
    }

def get_available_reg76_records():
    """Get Reg-76 records that haven't been processed in Reg-74 yet from SQLite"""
    try:
        # Load Reg-76 data from SQLite
        conn = sqlite3.connect(DB_PATH) # excise_registers.db
        reg76_df = pd.read_sql_query("SELECT * FROM reg76_receipts", conn)
        conn.close()
        
        reg74_df = get_data() # Already uses SQLite
        
        if reg76_df.empty:
            return pd.DataFrame()
        
        # Get Reg-76 IDs already processed
        processed_ids = []
        if not reg74_df.empty and 'ref_reg76_id' in reg74_df.columns:
            processed_ids = reg74_df['ref_reg76_id'].dropna().unique().tolist()
        
        # Filter unprocessed records
        available = reg76_df[~reg76_df['reg76_id'].isin(processed_ids)]
        return available
    except Exception as e:
        print(f"Error fetching available Reg-76 from SQLite: {e}")
        return pd.DataFrame()

def get_last_operation_date(vat_no):
    """Get the date of the last operation for a specific VAT"""
    df = get_data()
    if df.empty:
        return None
    
    # Filter records for this VAT
    vat_records = df[
        (df['source_vat'] == vat_no) | 
        (df['destination_vat'] == vat_no)
    ].sort_values('operation_date', ascending=False)
    
    if vat_records.empty:
        return None
    
    latest = vat_records.iloc[0]
    try:
        return pd.to_datetime(latest['operation_date']).date()
    except:
        return None
