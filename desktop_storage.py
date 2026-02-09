import os
import pandas as pd
from datetime import datetime
from pathlib import Path
import socket

# Define storage location - always on Desktop for easy access
EXCISE_FOLDER = Path(os.path.expanduser("~/Desktop/Excise_Register_Data"))
EXCISE_FOLDER.mkdir(parents=True, exist_ok=True)

# Register File Paths
REG76_EXCEL_FILE = EXCISE_FOLDER / "Reg76_Data.xlsx"
REG74_EXCEL_FILE = EXCISE_FOLDER / "Reg74_Data.xlsx"
REGA_EXCEL_FILE = EXCISE_FOLDER / "RegA_Data.xlsx"
REGB_EXCEL_FILE = EXCISE_FOLDER / "RegB_Data.xlsx"
REG78_EXCEL_FILE = EXCISE_FOLDER / "Reg78_Data.xlsx"
EXCISE_DUTY_EXCEL_FILE = EXCISE_FOLDER / "Excise_Duty_Data.xlsx"

# Helper for registration logic
def ensure_folder_exists():
    """Ensure the storage folder exists on Desktop"""
    EXCISE_FOLDER.mkdir(parents=True, exist_ok=True)
    return EXCISE_FOLDER

# --- REG-76 STORAGE ---
def ensure_reg76_excel_exists():
    if not REG76_EXCEL_FILE.exists():
        from schema import COLUMNS
        df = pd.DataFrame(columns=COLUMNS)
        df.to_excel(REG76_EXCEL_FILE, index=False, sheet_name='Reg-76 Data')
    return REG76_EXCEL_FILE

def get_data_from_excel():
    ensure_reg76_excel_exists()
    try:
        df = pd.read_excel(REG76_EXCEL_FILE, sheet_name='Reg-76 Data')
        return df.dropna(how='all')
    except Exception:
        from schema import COLUMNS
        return pd.DataFrame(columns=COLUMNS)

def save_to_excel(df):
    try:
        ensure_reg76_excel_exists()
        df.to_excel(REG76_EXCEL_FILE, index=False, sheet_name='Reg-76 Data')
        return True, "✅ Data saved to Desktop Excel"
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

def add_record_to_excel(data_dict):
    df = get_data_from_excel()
    # Remove existing if ID exists
    if "reg76_id" in data_dict and data_dict["reg76_id"]:
        df = df[df['reg76_id'].astype(str) != str(data_dict["reg76_id"])]
    
    new_row = pd.DataFrame([data_dict])
    df = pd.concat([df, new_row], ignore_index=True)
    success, msg = save_to_excel(df)
    return success, msg, data_dict.get("reg76_id")

def delete_record_from_excel(reg76_id):
    df = get_data_from_excel()
    if reg76_id in df['reg76_id'].astype(str).values:
        df = df[df['reg76_id'].astype(str) != str(reg76_id)]
        return save_to_excel(df)
    return False, "Record not found"

def clear_all_excel_data():
    from schema import COLUMNS
    df = pd.DataFrame(columns=COLUMNS)
    return save_to_excel(df)

# --- REG-74 STORAGE ---
def ensure_reg74_excel_exists():
    if not REG74_EXCEL_FILE.exists():
        try:
            from reg74_schema import REG74_COLUMNS
            df = pd.DataFrame(columns=REG74_COLUMNS)
            df.to_excel(REG74_EXCEL_FILE, index=False, sheet_name='Reg-74 Data')
        except ImportError:
            df = pd.DataFrame()
            df.to_excel(REG74_EXCEL_FILE, index=False, sheet_name='Reg-74 Data')
    return REG74_EXCEL_FILE

def get_reg74_data_from_excel():
    ensure_reg74_excel_exists()
    try:
        return pd.read_excel(REG74_EXCEL_FILE, sheet_name='Reg-74 Data').dropna(how='all')
    except Exception:
        return pd.DataFrame()

def save_reg74_to_excel(df):
    try:
        df.to_excel(REG74_EXCEL_FILE, index=False, sheet_name='Reg-74 Data')
        return True, "✅ Data saved to Reg-74 Excel"
    except Exception as e:
        return False, str(e)

def add_reg74_record_to_excel(data_dict):
    df = get_reg74_data_from_excel()
    if "reg74_id" in data_dict and data_dict["reg74_id"]:
        df = df[df['reg74_id'].astype(str) != str(data_dict["reg74_id"])]
    new_row = pd.DataFrame([data_dict])
    df = pd.concat([df, new_row], ignore_index=True)
    success, msg = save_reg74_to_excel(df)
    return success, msg, data_dict.get("reg74_id")

# --- REG-A STORAGE ---
def ensure_rega_excel_exists():
    if not REGA_EXCEL_FILE.exists():
        try:
            from rega_schema import REGA_COLUMNS
            df = pd.DataFrame(columns=REGA_COLUMNS)
            df.to_excel(REGA_EXCEL_FILE, index=False, sheet_name='Reg-A Data')
        except ImportError:
            df = pd.DataFrame()
            df.to_excel(REGA_EXCEL_FILE, index=False, sheet_name='Reg-A Data')
    return REGA_EXCEL_FILE

def get_rega_data_from_excel():
    ensure_rega_excel_exists()
    try:
        return pd.read_excel(REGA_EXCEL_FILE, sheet_name='Reg-A Data').dropna(how='all')
    except Exception:
        return pd.DataFrame()

def save_rega_to_excel(df):
    try:
        df.to_excel(REGA_EXCEL_FILE, index=False, sheet_name='Reg-A Data')
        return True, "✅ Data saved to Reg-A Excel"
    except Exception as e:
        return False, str(e)

def add_rega_record_to_excel(data_dict):
    df = get_rega_data_from_excel()
    if "rega_id" in data_dict and data_dict["rega_id"]:
        df = df[df['rega_id'].astype(str) != str(data_dict["rega_id"])]
    new_row = pd.DataFrame([data_dict])
    df = pd.concat([df, new_row], ignore_index=True)
    success, msg = save_rega_to_excel(df)
    return success, msg, data_dict.get("rega_id")

# --- REG-78 STORAGE ---
def ensure_reg78_excel_exists():
    if not REG78_EXCEL_FILE.exists():
        try:
            from reg78_schema import REG78_COLUMNS
            df = pd.DataFrame(columns=REG78_COLUMNS)
            df.to_excel(REG78_EXCEL_FILE, index=False, sheet_name='Reg-78 Data')
        except ImportError:
            df = pd.DataFrame()
            df.to_excel(REG78_EXCEL_FILE, index=False, sheet_name='Reg-78 Data')
    return REG78_EXCEL_FILE

def get_reg78_data_from_excel():
    ensure_reg78_excel_exists()
    try:
        return pd.read_excel(REG78_EXCEL_FILE, sheet_name='Reg-78 Data').dropna(how='all')
    except Exception:
        return pd.DataFrame()

def save_reg78_to_excel(df):
    try:
        df.to_excel(REG78_EXCEL_FILE, index=False, sheet_name='Reg-78 Data')
        return True, "✅ Data saved to Reg-78 Excel"
    except Exception as e:
        return False, str(e)

def add_reg78_record_to_excel(data_dict):
    df = get_reg78_data_from_excel()
    # For Reg-78, we often use date as uniqueness
    synopsis_date = str(data_dict.get("synopsis_date") or "")
    if synopsis_date and "synopsis_date" in df.columns:
        df = df[df["synopsis_date"].astype(str) != synopsis_date]
    new_row = pd.DataFrame([data_dict])
    df = pd.concat([df, new_row], ignore_index=True)
    success, msg = save_reg78_to_excel(df)
    return success, msg, data_dict.get("reg78_id")

# --- REG-B STORAGE ---
REGB_FEES_SHEET = "Production Fees"
REGB_STOCK_SHEET = "Bottle Stock"

REGB_FEES_COLUMNS = ["regb_fees_id","date","opening_balance","deposit_amount","echallan_no","echallan_date","total_credited","iml_bottles_qty","total_bottles_produced","fee_per_bottle","total_fees_debited","closing_balance","remarks","excise_officer_name","excise_officer_signature","status","created_at","updated_at"]
REGB_STOCK_COLUMNS = ["regb_stock_id","date","product_name","strength","bottle_size_ml","opening_balance_bottles","quantity_received_bottles","total_accounted_bottles","wastage_breakage_bottles","issue_on_duty_bottles","closing_balance_bottles","opening_balance_bl","received_bl","total_bl","wastage_bl","issue_bl","closing_bl","opening_balance_al","received_al","total_al","wastage_al","issue_al","closing_al","status","created_at","updated_at"]

def ensure_regb_excel_exists():
    if not REGB_EXCEL_FILE.exists():
        with pd.ExcelWriter(REGB_EXCEL_FILE, engine="openpyxl") as writer:
            pd.DataFrame(columns=REGB_FEES_COLUMNS).to_excel(writer, index=False, sheet_name=REGB_FEES_SHEET)
            pd.DataFrame(columns=REGB_STOCK_COLUMNS).to_excel(writer, index=False, sheet_name=REGB_STOCK_SHEET)
    return REGB_EXCEL_FILE

def save_regb_fees_to_excel(data_dict):
    ensure_regb_excel_exists()
    try:
        fees_df = pd.read_excel(REGB_EXCEL_FILE, sheet_name=REGB_FEES_SHEET)
        stock_df = pd.read_excel(REGB_EXCEL_FILE, sheet_name=REGB_STOCK_SHEET)
        
        # Deduplication by date
        key_date = str(data_dict.get("date") or "")
        if key_date and "date" in fees_df.columns:
            fees_df = fees_df[fees_df["date"].astype(str) != key_date]
        
        fees_df = pd.concat([fees_df, pd.DataFrame([data_dict])], ignore_index=True)
        
        with pd.ExcelWriter(REGB_EXCEL_FILE, engine="openpyxl") as writer:
            fees_df.to_excel(writer, index=False, sheet_name=REGB_FEES_SHEET)
            stock_df.to_excel(writer, index=False, sheet_name=REGB_STOCK_SHEET)
        return True, "✅ Reg-B Fees saved"
    except Exception as e:
        return False, str(e)

def save_regb_bottle_stock_to_excel(data_dict):
    ensure_regb_excel_exists()
    try:
        fees_df = pd.read_excel(REGB_EXCEL_FILE, sheet_name=REGB_FEES_SHEET)
        stock_df = pd.read_excel(REGB_EXCEL_FILE, sheet_name=REGB_STOCK_SHEET)
        
        # Deduplication by date, product, size
        match = (
            (stock_df["date"].astype(str) == str(data_dict.get("date"))) & 
            (stock_df["product_name"] == data_dict.get("product_name")) & 
            (stock_df["bottle_size_ml"].astype(str) == str(data_dict.get("bottle_size_ml")))
        )
        stock_df = stock_df[~match]
        
        stock_df = pd.concat([stock_df, pd.DataFrame([data_dict])], ignore_index=True)
        
        with pd.ExcelWriter(REGB_EXCEL_FILE, engine="openpyxl") as writer:
            fees_df.to_excel(writer, index=False, sheet_name=REGB_FEES_SHEET)
            stock_df.to_excel(writer, index=False, sheet_name=REGB_STOCK_SHEET)
        return True, "✅ Reg-B Stock saved"
    except Exception as e:
        return False, str(e)

# --- EXCISE DUTY STORAGE ---
EXCISE_LEDGER_SHEET = "Duty Ledger"
EXCISE_BOTTLES_SHEET = "Issued Bottles"

def ensure_excise_excel_exists():
    if not EXCISE_DUTY_EXCEL_FILE.exists():
        with pd.ExcelWriter(EXCISE_DUTY_EXCEL_FILE, engine="openpyxl") as writer:
            pd.DataFrame().to_excel(writer, index=False, sheet_name=EXCISE_LEDGER_SHEET)
            pd.DataFrame().to_excel(writer, index=False, sheet_name=EXCISE_BOTTLES_SHEET)
    return EXCISE_DUTY_EXCEL_FILE

def save_excise_ledger_to_excel(data_dict):
    ensure_excise_excel_exists()
    try:
        ledger_df = pd.read_excel(EXCISE_DUTY_EXCEL_FILE, sheet_name=EXCISE_LEDGER_SHEET)
        bottles_df = pd.read_excel(EXCISE_DUTY_EXCEL_FILE, sheet_name=EXCISE_BOTTLES_SHEET)
        
        key_date = str(data_dict.get("date") or "")
        if key_date and "date" in ledger_df.columns:
            ledger_df = ledger_df[ledger_df["date"].astype(str) != key_date]
            
        ledger_df = pd.concat([ledger_df, pd.DataFrame([data_dict])], ignore_index=True)
        
        with pd.ExcelWriter(EXCISE_DUTY_EXCEL_FILE, engine="openpyxl") as writer:
            ledger_df.to_excel(writer, index=False, sheet_name=EXCISE_LEDGER_SHEET)
            bottles_df.to_excel(writer, index=False, sheet_name=EXCISE_BOTTLES_SHEET)
        return True, "✅ Excise Duty Ledger saved"
    except Exception as e:
        return False, str(e)

def save_excise_bottle_to_excel(data_dict):
    ensure_excise_excel_exists()
    try:
        ledger_df = pd.read_excel(EXCISE_DUTY_EXCEL_FILE, sheet_name=EXCISE_LEDGER_SHEET)
        bottles_df = pd.read_excel(EXCISE_DUTY_EXCEL_FILE, sheet_name=EXCISE_BOTTLES_SHEET)
        
        match = (
            (bottles_df["date"].astype(str) == str(data_dict.get("date"))) & 
            (bottles_df["product_name"] == data_dict.get("product_name")) & 
            (bottles_df["bottle_size_ml"].astype(str) == str(data_dict.get("bottle_size_ml")))
        )
        bottles_df = bottles_df[~match]
        
        bottles_df = pd.concat([bottles_df, pd.DataFrame([data_dict])], ignore_index=True)
        
        with pd.ExcelWriter(EXCISE_DUTY_EXCEL_FILE, engine="openpyxl") as writer:
            ledger_df.to_excel(writer, index=False, sheet_name=EXCISE_LEDGER_SHEET)
            bottles_df.to_excel(writer, index=False, sheet_name=EXCISE_BOTTLES_SHEET)
        return True, "✅ Excise Duty Bottles saved"
    except Exception as e:
        return False, str(e)

# Initialize
print(f"📁 Excise Register Data Folder: {EXCISE_FOLDER}")
print(f"📊 Reg-76 Excel File: {REG76_EXCEL_FILE}")
print(f"📊 Reg-74 Excel File: {REG74_EXCEL_FILE}")
print(f"📊 Reg-A Excel File: {REGA_EXCEL_FILE}")
print(f"📊 Reg-B Excel File: {REGB_EXCEL_FILE}")
print(f"📊 Excise Duty Excel File: {EXCISE_DUTY_EXCEL_FILE}")
print(f"📊 Reg-78 Excel File: {REG78_EXCEL_FILE}")