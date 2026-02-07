import os
import pandas as pd
from datetime import datetime
from pathlib import Path

# Desktop path configuration
DESKTOP_PATH = Path.home() / "Desktop"
EXCISE_FOLDER = DESKTOP_PATH / "Excise_Register_Data"
REG76_EXCEL_FILE = EXCISE_FOLDER / "Reg76_Data.xlsx"

# Ensure folder exists
EXCISE_FOLDER.mkdir(parents=True, exist_ok=True)

def get_excel_path():
    """Returns the path to the Reg-76 Excel file on Desktop"""
    return REG76_EXCEL_FILE

def ensure_excel_file_exists():
    """Create the Excel file if it doesn't exist"""
    if not REG76_EXCEL_FILE.exists():
        # Create empty DataFrame with all columns
        from schema import COLUMNS
        df = pd.DataFrame(columns=COLUMNS)
        df.to_excel(REG76_EXCEL_FILE, index=False, sheet_name='Reg-76 Data')
        print(f"✅ Created new Excel file: {REG76_EXCEL_FILE}")
    return REG76_EXCEL_FILE

def get_data_from_excel():
    """Load data from Desktop Excel file"""
    ensure_excel_file_exists()
    try:
        df = pd.read_excel(REG76_EXCEL_FILE, sheet_name='Reg-76 Data')
        # Clean data
        df = df.dropna(how='all')
        if 'reg76_id' in df.columns:
            df = df[df['reg76_id'].notna()]
            df = df[df['reg76_id'].astype(str).str.strip() != '']
        return df
    except Exception as e:
        print(f"Error reading Excel: {e}")
        from schema import COLUMNS
        return pd.DataFrame(columns=COLUMNS)

def save_to_excel(df):
    """Save DataFrame to Desktop Excel file"""
    try:
        ensure_excel_file_exists()
        df.to_excel(REG76_EXCEL_FILE, index=False, sheet_name='Reg-76 Data')
        return True, f"✅ Data saved to: {REG76_EXCEL_FILE}"
    except Exception as e:
        return False, f"❌ Error saving to Excel: {str(e)}"

def add_record_to_excel(data_dict):
    """Add a new record to the Excel file"""
    df = get_data_from_excel()
    
    # Generate ID if not present
    if "reg76_id" not in data_dict or not data_dict["reg76_id"]:
        prefix = "R76-"
        count = len(df) + 1
        data_dict["reg76_id"] = f"{prefix}{datetime.now().strftime('%Y%m')}{count:03d}"
    
    data_dict["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Add new row
    new_row = pd.DataFrame([data_dict])
    df = pd.concat([df, new_row], ignore_index=True)
    
    # Save to Excel
    success, message = save_to_excel(df)
    return success, message, data_dict["reg76_id"]

def delete_record_from_excel(reg76_id):
    """Delete a record from Excel file"""
    try:
        df = get_data_from_excel()
        
        if df.empty:
            return False, "No records found"
        
        if reg76_id not in df['reg76_id'].values:
            return False, f"Record {reg76_id} not found"
        
        # Remove record
        df = df[df['reg76_id'] != reg76_id]
        
        # Save
        success, message = save_to_excel(df)
        if success:
            return True, f"✅ Record {reg76_id} deleted"
        else:
            return False, message
            
    except Exception as e:
        return False, f"Error: {str(e)}"

def clear_all_excel_data():
    """Clear all data from Excel file"""
    try:
        from schema import COLUMNS
        empty_df = pd.DataFrame(columns=COLUMNS)
        success, message = save_to_excel(empty_df)
        return success, message
    except Exception as e:
        return False, f"Error: {str(e)}"

def export_to_csv(df, filename=None):
    """Export data to CSV on Desktop"""
    if filename is None:
        filename = f"Reg76_Export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    csv_path = EXCISE_FOLDER / filename
    try:
        df.to_csv(csv_path, index=False)
        return True, f"✅ Exported to: {csv_path}"
    except Exception as e:
        return False, f"Error: {str(e)}"

# --- REG-74 STORAGE FUNCTIONS ---

REG74_EXCEL_FILE = EXCISE_FOLDER / "Reg74_Data.xlsx"

def ensure_reg74_excel_exists():
    """Create the Reg-74 Excel file if it doesn't exist"""
    if not REG74_EXCEL_FILE.exists():
        # Create empty DataFrame with all columns
        try:
            from reg74_schema import REG74_COLUMNS
            df = pd.DataFrame(columns=REG74_COLUMNS)
            df.to_excel(REG74_EXCEL_FILE, index=False, sheet_name='Reg-74 Data')
            print(f"✅ Created new Excel file: {REG74_EXCEL_FILE}")
        except ImportError:
            print("⚠️ reg74_schema not found, creating generic empty file")
            df = pd.DataFrame()
            df.to_excel(REG74_EXCEL_FILE, index=False, sheet_name='Reg-74 Data')
    return REG74_EXCEL_FILE

def get_reg74_data_from_excel():
    """Load data from Reg-74 Desktop Excel file"""
    ensure_reg74_excel_exists()
    try:
        df = pd.read_excel(REG74_EXCEL_FILE, sheet_name='Reg-74 Data')
        # Clean data
        df = df.dropna(how='all')
        if 'reg74_id' in df.columns:
            df = df[df['reg74_id'].notna()]
            df = df[df['reg74_id'].astype(str).str.strip() != '']
        return df
    except Exception as e:
        print(f"Error reading Reg-74 Excel: {e}")
        try:
            from reg74_schema import REG74_COLUMNS
            return pd.DataFrame(columns=REG74_COLUMNS)
        except:
            return pd.DataFrame()

def save_reg74_to_excel(df):
    """Save Reg-74 DataFrame to Desktop Excel file"""
    try:
        ensure_reg74_excel_exists()
        df.to_excel(REG74_EXCEL_FILE, index=False, sheet_name='Reg-74 Data')
        return True, f"✅ Data saved to: {REG74_EXCEL_FILE}"
    except Exception as e:
        return False, f"❌ Error saving to Reg-74 Excel: {str(e)}"

def add_reg74_record_to_excel(data_dict):
    """Add a new record to the Reg-74 Excel file"""
    df = get_reg74_data_from_excel()
    
    # Generate ID if not present
    if "reg74_id" not in data_dict or not data_dict["reg74_id"]:
        prefix = "R74-"
        count = len(df) + 1
        data_dict["reg74_id"] = f"{prefix}{datetime.now().strftime('%Y%m')}{count:03d}"
    
    data_dict["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Add new row
    new_row = pd.DataFrame([data_dict])
    df = pd.concat([df, new_row], ignore_index=True)
    
    # Save to Excel
    success, message = save_reg74_to_excel(df)
    return success, message, data_dict["reg74_id"]

# Print initialization message
print(f"📁 Excise Register Data Folder: {EXCISE_FOLDER}")
print(f"📊 Reg-76 Excel File: {REG76_EXCEL_FILE}")
print(f"📊 Reg-74 Excel File: {REG74_EXCEL_FILE}")
