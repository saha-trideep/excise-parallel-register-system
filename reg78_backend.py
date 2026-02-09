import os
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from reg78_schema import REG78_COLUMNS, PRODUCTION_FEES_RATE_PER_BL, ALL_VATS, SST_VATS, BRT_VATS
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import desktop_storage
from reg78_sqlite_schema import CREATE_REG78_TABLE, CREATE_REG78_INDEXES

CSV_PATH = "backup_data/reg78_data.csv"
DB_PATH = "excise_registers.db"
JSON_KEY = "the-program-482110-e4-7ef9d425d794.json"
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1Ecmrq9JUhCerhq4mebO1Jtpw8sD_tTo-79_x3Jabr68"
WORKSHEET_NAME = "Reg78"  # Daily synopsis worksheet

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
        cursor.executescript(CREATE_REG78_TABLE)
        cursor.executescript(CREATE_REG78_INDEXES)
        conn.commit()
        conn.close()
    except Exception as e:
        st.error(f"SQLite initialization error: {e}")

def get_data_from_sqlite():
    """Load data from SQLite database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM reg78_synopsis ORDER BY synopsis_date DESC", conn)
        conn.close()
        return df
    except Exception as e:
        st.warning(f"SQLite read error: {e}")
        return pd.DataFrame(columns=REG78_COLUMNS)

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
        query = f"INSERT OR REPLACE INTO reg78_synopsis ({column_names}) VALUES ({placeholders})"
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
            return pd.DataFrame(columns=REG78_COLUMNS)
    return pd.DataFrame(columns=REG78_COLUMNS)

def get_data():
    """Load data - prioritized from SQLite database"""
    init_sqlite_db()
    return get_data_from_sqlite()

def save_record(data_dict):
    """Save record to SQLite (primary), Desktop Excel (presentation), CSV (backup), and Google Sheets (sync)"""
    
    # ID Generation and Timestamps
    if "reg78_id" not in data_dict or not data_dict["reg78_id"]:
        prefix = "R78-"
        count = len(get_data()) + 1
        data_dict["reg78_id"] = f"{prefix}{datetime.now().strftime('%Y%m')}{count:04d}"
    
    data_dict["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_dict["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_dict["status"] = data_dict.get("status", "draft")
    record_id = data_dict["reg78_id"]

    # 1. Save to SQLite (PRIMARY STORAGE)
    init_sqlite_db()
    success_sqlite = save_to_sqlite(data_dict)
    
    if not success_sqlite:
        st.error("❌ Failed to save to SQLite database!")
        return None

    # 2. Save to Desktop Excel (PRESENTATION LAYER)
    try:
        success_excel, message_excel, _ = desktop_storage.add_reg78_record_to_excel(data_dict)
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
    
    # 4. Attempt Sync
    sync_success = False
    try:
        df_sqlite = get_data_from_sqlite()
        sync_success = sync_to_gsheet(df_sqlite)
    except Exception as e:
        st.warning(f"⚠️ Google Sheets sync failed: {e}")
    
    if sync_success:
        st.success(f"✅ Daily Synopsis saved to SQLite AND synced to Google Sheets!\n📁 SQLite ID: {record_id}")
    else:
        st.success(f"✅ Daily Synopsis saved to SQLite!\n📁 SQLite ID: {record_id}")
        st.info("ℹ️ Google Sheets sync failed - use manual sync button if needed.")
            
    return record_id

def sync_to_gsheet(df):
    """Sync a dataframe to the Google Sheet using direct gspread"""
    client = get_google_client()
    if client:
        try:
            sh = client.open_by_url(SPREADSHEET_URL)
            
            # Try to get Reg78 worksheet, create if doesn't exist
            try:
                worksheet = sh.worksheet(WORKSHEET_NAME)
            except gspread.exceptions.WorksheetNotFound:
                worksheet = sh.add_worksheet(title=WORKSHEET_NAME, rows=1000, cols=len(REG78_COLUMNS))
            
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
            st.toast("✅ Synchronized with Google Sheets (Reg-78)")
            return True
        except Exception as e:
            st.sidebar.error(f"Sync failed: {e}")
            return False
    else:
        st.sidebar.warning("GSheet Sync Offline: No credentials found.")
        return False

def get_previous_day_closing(target_date):
    """Get closing balance from previous day's Reg-78"""
    df = get_data()
    if df.empty:
        return {"bl": 0.0, "al": 0.0}
    
    # Convert target_date to datetime for comparison
    target_dt = pd.to_datetime(target_date)
    previous_date = (target_dt - timedelta(days=1)).date()
    
    # Filter for previous date
    if 'synopsis_date' in df.columns:
        df['synopsis_date_dt'] = pd.to_datetime(df['synopsis_date']).dt.date
        prev_records = df[df['synopsis_date_dt'] == previous_date]
        
        if not prev_records.empty:
            latest = prev_records.iloc[-1]
            return {
                "bl": float(latest.get('closing_balance_bl', 0) or 0),
                "al": float(latest.get('closing_balance_al', 0) or 0)
            }
    
    return {"bl": 0.0, "al": 0.0}

def get_reg76_daily_summary(target_date):
    """Get all Reg-76 receipts for a specific date from SQLite"""
    try:
        conn = sqlite3.connect("excise_registers.db")
        # Filter by date in SQL for efficiency
        query = "SELECT * FROM reg76_receipts WHERE date_receipt = ?"
        daily_records = pd.read_sql_query(query, conn, params=(str(target_date),))
        conn.close()
        
        if daily_records.empty:
            return {
                "count": 0,
                "pass_numbers": "",
                "total_bl": 0.0,
                "total_al": 0.0,
                "mfm1_bl": 0.0,
                "mfm1_al": 0.0
            }
        
        # Aggregate data
        pass_numbers = ", ".join(daily_records['permit_no'].dropna().astype(str).tolist())
        total_bl = daily_records['rec_bl'].sum()
        total_al = daily_records['rec_al'].sum()
        # Note: If mfm1_bl/al are not in schema, fallback to rec_bl/al
        mfm1_bl = total_bl # Adjust if mfm1 columns are added to SQLite later
        mfm1_al = total_al
        
        return {
            "count": len(daily_records),
            "pass_numbers": pass_numbers,
            "total_bl": float(total_bl),
            "total_al": float(total_al),
            "mfm1_bl": float(mfm1_bl),
            "mfm1_al": float(mfm1_al)
        }
    except Exception as e:
        print(f"Error reading Reg-76 SQLite: {e}")
        return {
            "count": 0,
            "pass_numbers": "",
            "total_bl": 0.0,
            "total_al": 0.0,
            "mfm1_bl": 0.0,
            "mfm1_al": 0.0
        }

def get_reg74_daily_summary(target_date):
    """Get all Reg-74 operations for a specific date from SQLite"""
    try:
        conn = sqlite3.connect("excise_registers.db")
        # Get daily records for wastage
        query_daily = "SELECT * FROM reg74_operations WHERE operation_date = ?"
        daily_records = pd.read_sql_query(query_daily, conn, params=(str(target_date),))
        
        # Get all records to find latest closing for each VAT
        query_all = "SELECT * FROM reg74_operations ORDER BY operation_date DESC"
        reg74_df = pd.read_sql_query(query_all, conn)
        conn.close()
        
        if daily_records.empty and reg74_df.empty:
            return {
                "operational_wastage_bl": 0.0,
                "operational_wastage_al": 0.0,
                "vat_balances": {vat: {"bl": 0.0, "al": 0.0} for vat in ALL_VATS}
            }
        
        # Get storage wastage
        wastage_bl = daily_records['storage_wastage_bl'].sum() if 'storage_wastage_bl' in daily_records.columns else 0.0
        wastage_al = daily_records['storage_wastage_al'].sum() if 'storage_wastage_al' in daily_records.columns else 0.0
        
        # Get latest closing balance for each VAT
        vat_balances = {}
        for vat in ALL_VATS:
            vat_records = reg74_df[
                (reg74_df['source_vat'] == vat) | 
                (reg74_df['destination_vat'] == vat)
            ]
            
            if not vat_records.empty:
                latest = vat_records.iloc[0] # Already sorted by date DESC
                vat_balances[vat] = {
                    "bl": float(latest.get('closing_bl', 0) or 0),
                    "al": float(latest.get('closing_al', 0) or 0)
                }
            else:
                vat_balances[vat] = {"bl": 0.0, "al": 0.0}
        
        return {
            "operational_wastage_bl": float(wastage_bl),
            "operational_wastage_al": float(wastage_al),
            "vat_balances": vat_balances
        }
    except Exception as e:
        print(f"Error reading Reg-74 SQLite: {e}")
        return {
            "operational_wastage_bl": 0.0,
            "operational_wastage_al": 0.0,
            "vat_balances": {vat: {"bl": 0.0, "al": 0.0} for vat in ALL_VATS}
        }

def get_rega_daily_summary(target_date):
    """Get all Reg-A production for a specific date from SQLite"""
    try:
        conn = sqlite3.connect("excise_registers.db")
        query = "SELECT * FROM rega_production WHERE production_date = ?"
        daily_records = pd.read_sql_query(query, conn, params=(str(target_date),))
        conn.close()
        
        if daily_records.empty:
            return {
                "total_bottles": 0,
                "total_bl_produced": 0.0,
                "total_al_produced": 0.0,
                "total_al_in_bottles": 0.0,
                "production_wastage_bl": 0.0,
                "production_wastage_al": 0.0,
                "production_fees": 0.0
            }
        
        # Aggregate production data
        total_bottles = daily_records['total_bottles'].sum()
        total_al_in_bottles = daily_records['bottles_total_al'].sum()
        mfm2_total_bl = daily_records['mfm2_reading_bl'].sum()
        mfm2_total_al = daily_records['mfm2_reading_al'].sum()
        production_wastage_bl = daily_records['wastage_bl'].sum()
        production_wastage_al = daily_records['wastage_al'].sum()
        
        # Calculate production fees: ₹3/- per BL produced
        production_fees = mfm2_total_bl * PRODUCTION_FEES_RATE_PER_BL
        
        return {
            "total_bottles": int(total_bottles),
            "total_bl_produced": float(mfm2_total_bl),
            "total_al_produced": float(mfm2_total_al),
            "total_al_in_bottles": float(total_al_in_bottles),
            "production_wastage_bl": float(production_wastage_bl),
            "production_wastage_al": float(production_wastage_al),
            "production_fees": float(production_fees)
        }
    except Exception as e:
        print(f"Error reading Reg-A SQLite: {e}")
        return {
            "total_bottles": 0,
            "total_bl_produced": 0.0,
            "total_al_produced": 0.0,
            "total_al_in_bottles": 0.0,
            "production_wastage_bl": 0.0,
            "production_wastage_al": 0.0,
            "production_fees": 0.0
        }

def generate_daily_synopsis(target_date):
    """
    GENIUS AUTO-FILL: Generate complete daily synopsis from all registers
    """
    # Get previous day closing
    opening = get_previous_day_closing(target_date)
    
    # Get Reg-76 summary (Receipts)
    reg76 = get_reg76_daily_summary(target_date)
    
    # Get Reg-74 summary (Operations & VAT balances)
    reg74 = get_reg74_daily_summary(target_date)
    
    # Get Reg-A summary (Production)
    rega = get_rega_daily_summary(target_date)
    
    # Calculate totals
    total_credit_bl = (opening['bl'] + reg76['total_bl'])
    total_credit_al = (opening['al'] + reg76['total_al'])
    
    total_debit_bl = (rega['total_al_produced'] + reg74['operational_wastage_bl'] + 
                     rega['production_wastage_bl'])
    total_debit_al = (rega['total_al_produced'] + reg74['operational_wastage_al'] + 
                     rega['production_wastage_al'])
    
    closing_bl = total_credit_bl - total_debit_bl
    closing_al = total_credit_al - total_debit_al
    
    # Build synopsis data
    synopsis = {
        "opening_balance_bl": opening['bl'],
        "opening_balance_al": opening['al'],
        
        "consignment_count": reg76['count'],
        "consignment_pass_numbers": reg76['pass_numbers'],
        "consignment_received_bl": reg76['total_bl'],
        "consignment_received_al": reg76['total_al'],
        
        "mfm1_total_bl": reg76['mfm1_bl'],
        "mfm1_total_al": reg76['mfm1_al'],
        
        "total_credit_bl": total_credit_bl,
        "total_credit_al": total_credit_al,
        
        "production_total_bl": rega['total_bl_produced'],
        "production_total_al": rega['total_al_produced'],
        "production_fees_rate": PRODUCTION_FEES_RATE_PER_BL,
        "total_production_fees": rega['production_fees'],
        "issues_on_duty_bl": rega['total_bl_produced'],
        "issues_on_duty_al": rega['total_al_produced'],
        
        "operational_wastage_bl": reg74['operational_wastage_bl'],
        "operational_wastage_al": reg74['operational_wastage_al'],
        
        "production_wastage_bl": rega['production_wastage_bl'],
        "production_wastage_al": rega['production_wastage_al'],
        
        "total_debit_bl": total_debit_bl,
        "total_debit_al": total_debit_al,
        
        "closing_balance_bl": closing_bl,
        "closing_balance_al": closing_al,
        
        "total_bottles_produced": rega['total_bottles'],
        "total_al_in_bottles": rega['total_al_in_bottles'],
        "production_fees_payable": rega['production_fees'],
        
        "vat_balances": reg74['vat_balances']
    }
    
    return synopsis

def filter_records(date_from=None, date_to=None):
    """Filter records by date range"""
    df = get_data()
    if df is None or df.empty:
        return pd.DataFrame(columns=REG78_COLUMNS)
    
    if date_from:
        if 'synopsis_date' in df.columns:
            df['synopsis_date_dt'] = pd.to_datetime(df['synopsis_date']).dt.date
            df = df[df['synopsis_date_dt'] >= date_from]
    
    if date_to:
        if 'synopsis_date' in df.columns:
            df['synopsis_date_dt'] = pd.to_datetime(df['synopsis_date']).dt.date
            df = df[df['synopsis_date_dt'] <= date_to]
            
    return df
