import os
import pandas as pd
from datetime import datetime, timedelta
from reg78_schema import REG78_COLUMNS, PRODUCTION_FEES_RATE_PER_BL, ALL_VATS, SST_VATS, BRT_VATS
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

CSV_PATH = "reg78_data.csv"
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

def get_data_local():
    """Load local CSV fallback"""
    if os.path.exists(CSV_PATH):
        try:
            return pd.read_csv(CSV_PATH)
        except Exception:
            return pd.DataFrame(columns=REG78_COLUMNS)
    return pd.DataFrame(columns=REG78_COLUMNS)

def get_data():
    """Load data - prioritized from Local CSV for speed"""
    return get_data_local()

def save_record(data_dict):
    """Save record to local CSV first, then attempt push using gspread"""
    df_local = get_data_local()
    
    # ID Generation
    if "reg78_id" not in data_dict or not data_dict["reg78_id"]:
        prefix = "R78-"
        count = len(df_local) + 1
        data_dict["reg78_id"] = f"{prefix}{datetime.now().strftime('%Y%m')}{count:04d}"
    
    data_dict["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_dict["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 1. Update Local CSV (Always)
    new_row = pd.DataFrame([data_dict])
    df_local = pd.concat([df_local, new_row], ignore_index=True)
    df_local.to_csv(CSV_PATH, index=False)
    
    # 2. Attempt Sync
    sync_success = sync_to_gsheet(df_local)
    
    if sync_success:
        st.success("✅ Daily Synopsis saved and synced to Google Sheets!")
    else:
        st.warning("⚠️ Synopsis saved locally. Google Sheets sync failed - use manual sync button.")
            
    return data_dict["reg78_id"]

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
    """Get all Reg-76 receipts for a specific date"""
    try:
        reg76_df = pd.read_csv("reg76_data.csv")
        
        if reg76_df.empty:
            return {
                "count": 0,
                "pass_numbers": "",
                "total_bl": 0.0,
                "total_al": 0.0,
                "mfm1_bl": 0.0,
                "mfm1_al": 0.0
            }
        
        # Filter by date
        reg76_df['receipt_date_dt'] = pd.to_datetime(reg76_df['receipt_date']).dt.date
        daily_records = reg76_df[reg76_df['receipt_date_dt'] == target_date]
        
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
        total_bl = daily_records['receipt_bl'].sum()
        total_al = daily_records['receipt_al'].sum()
        mfm1_bl = daily_records['mfm1_bl'].sum() if 'mfm1_bl' in daily_records.columns else total_bl
        mfm1_al = daily_records['mfm1_al'].sum() if 'mfm1_al' in daily_records.columns else total_al
        
        return {
            "count": len(daily_records),
            "pass_numbers": pass_numbers,
            "total_bl": float(total_bl),
            "total_al": float(total_al),
            "mfm1_bl": float(mfm1_bl),
            "mfm1_al": float(mfm1_al)
        }
    except Exception:
        return {
            "count": 0,
            "pass_numbers": "",
            "total_bl": 0.0,
            "total_al": 0.0,
            "mfm1_bl": 0.0,
            "mfm1_al": 0.0
        }

def get_reg74_daily_summary(target_date):
    """Get all Reg-74 operations for a specific date"""
    try:
        reg74_df = pd.read_csv("reg74_data.csv")
        
        if reg74_df.empty:
            return {
                "operational_wastage_bl": 0.0,
                "operational_wastage_al": 0.0,
                "vat_balances": {}
            }
        
        # Filter by date
        reg74_df['operation_date_dt'] = pd.to_datetime(reg74_df['operation_date']).dt.date
        daily_records = reg74_df[reg74_df['operation_date_dt'] == target_date]
        
        # Get storage wastage
        wastage_bl = daily_records['storage_wastage_bl'].sum() if 'storage_wastage_bl' in daily_records.columns else 0.0
        wastage_al = daily_records['storage_wastage_al'].sum() if 'storage_wastage_al' in daily_records.columns else 0.0
        
        # Get latest closing balance for each VAT
        vat_balances = {}
        for vat in ALL_VATS:
            vat_records = reg74_df[
                (reg74_df['source_vat'] == vat) | 
                (reg74_df['destination_vat'] == vat)
            ].sort_values('operation_date', ascending=False)
            
            if not vat_records.empty:
                latest = vat_records.iloc[0]
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
    except Exception:
        return {
            "operational_wastage_bl": 0.0,
            "operational_wastage_al": 0.0,
            "vat_balances": {vat: {"bl": 0.0, "al": 0.0} for vat in ALL_VATS}
        }

def get_rega_daily_summary(target_date):
    """Get all Reg-A production for a specific date"""
    try:
        rega_df = pd.read_csv("rega_data.csv")
        
        if rega_df.empty:
            return {
                "total_bottles": 0,
                "total_bl_produced": 0.0,
                "total_al_produced": 0.0,
                "total_al_in_bottles": 0.0,
                "production_wastage_bl": 0.0,
                "production_wastage_al": 0.0,
                "production_fees": 0.0
            }
        
        # Filter by date
        rega_df['production_date_dt'] = pd.to_datetime(rega_df['production_date']).dt.date
        daily_records = rega_df[rega_df['production_date_dt'] == target_date]
        
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
        mfm2_total_bl = daily_records['mfm2_reading_bl'].sum()  # BL from MFM2
        mfm2_total_al = daily_records['mfm2_reading_al'].sum()
        production_wastage_bl = daily_records['wastage_bl'].sum()
        production_wastage_al = daily_records['wastage_al'].sum()
        
        # Calculate production fees: ₹3/- per BL produced (MFM2 BL reading)
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
    except Exception:
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
