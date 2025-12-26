"""
Add a dummy test record to Reg-76 for testing delete functionality
This script adds a realistic test record that you can delete later.
"""

import pandas as pd
from datetime import datetime
import os

CSV_PATH = "reg76_data.csv"

def add_test_record():
    """Add a dummy test record to reg76_data.csv"""
    
    print("=" * 60)
    print("Adding Test Record to Reg-76")
    print("=" * 60)
    print()
    
    # Check if CSV exists
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        # Clean empty rows
        df = df.dropna(how='all')
        if 'reg76_id' in df.columns:
            df = df[df['reg76_id'].notna()]
            df = df[df['reg76_id'].astype(str).str.strip() != '']
        print(f"Current records: {len(df)}")
    else:
        print("CSV file not found. Creating new one...")
        from schema import COLUMNS
        df = pd.DataFrame(columns=COLUMNS)
    
    # Create test record
    test_record = {
        "reg76_id": f"R76-TEST-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "permit_no": "TEST-PERMIT-12345",
        "distillery": "Globus Spirits",
        "spirit_nature": "ENA",
        "vehicle_no": "WB-23-TEST-9999",
        "num_tankers": 1,
        "tanker_capacity": "Full",
        "tanker_make_model": "Test Tanker Model",
        "invoice_no": "INV-TEST-001",
        "invoice_date": datetime.now().strftime("%Y-%m-%d"),
        "export_order_no": "EXP-TEST-001",
        "export_order_date": datetime.now().strftime("%Y-%m-%d"),
        "import_order_no": "IMP-TEST-001",
        "import_order_date": datetime.now().strftime("%Y-%m-%d"),
        "export_pass_no": "PASS-TEST-001",
        "export_pass_date": datetime.now().strftime("%Y-%m-%d"),
        "import_pass_no": "",
        "import_pass_date": "",
        "date_dispatch": datetime.now().strftime("%Y-%m-%d"),
        "date_arrival": datetime.now().strftime("%Y-%m-%d"),
        "date_receipt": datetime.now().strftime("%Y-%m-%d"),
        "days_in_transit": 0,
        "adv_weight_kg": 10000.500,
        "adv_avg_density": 0.8100,
        "adv_strength": 96.50,
        "adv_temp": 20.0,
        "adv_bl": 12346.914,
        "adv_al": 11914.772,
        "adv_bl_20c": 12346.914,
        "wb_laden_consignee": 25000.0,
        "wb_unladen_consignee": 15000.0,
        "wb_laden_pass": 25000.0,
        "wb_unladen_pass": 15000.0,
        "rec_mass_kg": 10000.000,
        "rec_unload_temp": 20.0,
        "rec_density_at_temp": 0.8100,
        "rec_density_20c": 0.8100,
        "rec_strength": 96.50,
        "rec_bl": 12345.679,
        "rec_al": 11913.580,
        "diff_advised_al": -1.192,
        "transit_wastage_al": 1.192,
        "transit_increase_al": 0.0,
        "allowable_wastage_al": 0.0,
        "chargeable_wastage_al": 1.192,
        "storage_vat_no": "SST-5",
        "evc_generated_date": datetime.now().strftime("%Y-%m-%d"),
        "excise_remarks": "TEST RECORD - Safe to delete",
        "officer_sig_date": datetime.now().strftime("%Y-%m-%d"),
        "status": "Submitted",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Add to dataframe
    new_row = pd.DataFrame([test_record])
    df = pd.concat([df, new_row], ignore_index=True)
    
    # Save to CSV
    df.to_csv(CSV_PATH, index=False)
    
    print()
    print("SUCCESS! Test record added:")
    print(f"  ID: {test_record['reg76_id']}")
    print(f"  Vehicle: {test_record['vehicle_no']}")
    print(f"  Permit: {test_record['permit_no']}")
    print(f"  VAT: {test_record['storage_vat_no']}")
    print()
    print(f"Total records now: {len(df)}")
    print()
    print("=" * 60)
    print("Next Steps:")
    print("  1. Restart your Streamlit app (Ctrl+C, then 'streamlit run Home.py')")
    print("  2. Login with password: admin089")
    print("  3. Go to Reg-76 > Administrative View tab")
    print("  4. You should now see the DELETE options!")
    print("  5. Use the delete feature to remove this test record")
    print("=" * 60)

if __name__ == "__main__":
    try:
        add_test_record()
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
