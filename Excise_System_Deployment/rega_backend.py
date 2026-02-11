import os
import sqlite3
import pandas as pd
from datetime import datetime
from rega_schema import REGA_COLUMNS
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import desktop_storage
from rega_sqlite_schema import CREATE_REGA_TABLE, CREATE_REGA_INDEXES

CSV_PATH = "backup_data/rega_data.csv"
DB_PATH = "excise_registers.db"
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

def init_sqlite_db():
    """Initialize SQLite database and tables if they don't exist"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.executescript(CREATE_REGA_TABLE)
        cursor.executescript(CREATE_REGA_INDEXES)
        conn.commit()
        conn.close()
    except Exception as e:
        st.error(f"SQLite initialization error: {e}")

def get_data_from_sqlite():
    """Load data from SQLite database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM rega_production ORDER BY production_date DESC", conn)
        conn.close()
        return df
    except Exception as e:
        st.warning(f"SQLite read error: {e}")
        return pd.DataFrame(columns=REGA_COLUMNS)

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
        query = f"INSERT OR REPLACE INTO rega_production ({column_names}) VALUES ({placeholders})"
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
            return pd.DataFrame(columns=REGA_COLUMNS)
    return pd.DataFrame(columns=REGA_COLUMNS)

def get_data():
    """Load data - prioritized from SQLite database"""
    init_sqlite_db()
    return get_data_from_sqlite()

def save_record(data_dict):
    """Save record to SQLite (primary), Desktop Excel (presentation), CSV (backup), and Google Sheets (sync)"""
    
    # ID Generation and Timestamps
    if "rega_id" not in data_dict or not data_dict["rega_id"]:
        prefix = "RA-"
        count = len(get_data()) + 1
        data_dict["rega_id"] = f"{prefix}{datetime.now().strftime('%Y%m')}{count:04d}"
    
    data_dict["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_dict["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_dict["status"] = data_dict.get("status", "draft")
    record_id = data_dict["rega_id"]

    # 1. Save to SQLite (PRIMARY STORAGE)
    init_sqlite_db()
    success_sqlite = save_to_sqlite(data_dict)
    
    if not success_sqlite:
        st.error("❌ Failed to save to SQLite database!")
        return None

    # 2. Save to Desktop Excel (PRESENTATION LAYER)
    try:
        success_excel, message_excel, _ = desktop_storage.add_rega_record_to_excel(data_dict)
        if not success_excel:
            st.warning(f"⚠️ Desktop Excel save failed: {message_excel}")
    except Exception as e:
        st.warning(f"⚠️ Desktop Excel save failed: {e}")

    # 3. Update Local CSV (BACKUP)
    try:
        df_local = get_data_local()
        new_row = pd.DataFrame([data_dict])
        df_local = pd.concat([df_local, new_row], ignore_index=True)
        df_local.to_csv(CSV_PATH, index=False)
    except Exception as e:
        st.warning(f"⚠️ CSV backup failed: {e}")
    
    # --- AUTOMATION HOOKS ---
    try:
        # 1. Trigger Reg-78 Auto-Synopsis Update
        import reg78_backend
        target_date = datetime.strptime(data_dict["production_date"], "%Y-%m-%d").date()
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
        st.warning(f"Automation Hook Warning: {e}")
    # -------------------------

    # 4. Attempt Sync
    sync_success = False
    try:
        df_sqlite = get_data_from_sqlite()
        sync_success = sync_to_gsheet(df_sqlite)
    except Exception as e:
        st.warning(f"⚠️ Google Sheets sync failed: {e}")
    
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
    """Get batches from Reg-74 that are ready for production from SQLite"""
    try:
        conn = sqlite3.connect(DB_PATH) # excise_registers.db
        reg74_df = pd.read_sql_query("SELECT * FROM reg74_operations", conn)
        conn.close()
        
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
    except Exception as e:
        print(f"Error fetching available batches from SQLite: {e}")
        return pd.DataFrame()

def get_brt_current_stock(brt_vat):
    """Get current stock for a specific BRT from Reg-74 SQLite"""
    try:
        conn = sqlite3.connect(DB_PATH)
        query = "SELECT * FROM reg74_operations WHERE source_vat = ? OR destination_vat = ? ORDER BY operation_date DESC"
        brt_records = pd.read_sql_query(query, conn, params=(brt_vat, brt_vat))
        conn.close()
        
        if brt_records.empty:
            return {"bl": 0.0, "al": 0.0, "strength": 0.0}
        
        latest = brt_records.iloc[0]
        
        return {
            "bl": float(latest.get('closing_bl', 0) or 0),
            "al": float(latest.get('closing_al', 0) or 0),
            "strength": float(latest.get('closing_strength', 0) or 0)
        }
    except Exception as e:
        print(f"Error fetching BRT stock from SQLite: {e}")
        return {"bl": 0.0, "al": 0.0, "strength": 0.0}

def get_batch_details(batch_no):
    """Get batch details from Reg-74 SQLite"""
    try:
        conn = sqlite3.connect(DB_PATH)
        query = "SELECT * FROM reg74_operations WHERE batch_no = ? ORDER BY operation_date DESC"
        batch_records = pd.read_sql_query(query, conn, params=(batch_no,))
        conn.close()
        
        if batch_records.empty:
            return None
        
        latest = batch_records.iloc[0]
        
        return {
            "batch_no": batch_no,
            "brt_vat": latest.get('destination_vat', ''),
            "bl": float(latest.get('closing_bl', 0) or 0),
            "al": float(latest.get('closing_al', 0) or 0),
            "strength": float(latest.get('closing_strength', 0) or 0),
            "operation_date": latest.get('operation_date', ''),
            "reg74_id": latest.get('reg74_id', '')
        }
    except Exception as e:
        print(f"Error fetching batch details from SQLite: {e}")
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
