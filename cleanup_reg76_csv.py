"""
Quick cleanup script for reg76_data.csv
This script removes empty rows and invalid records from the CSV file.
"""

import pandas as pd
import os

CSV_PATH = "reg76_data.csv"

def cleanup_csv():
    """Clean up the CSV file by removing empty rows and invalid records"""
    
    if not os.path.exists(CSV_PATH):
        print(f"ERROR: File not found: {CSV_PATH}")
        return
    
    print(f"Reading {CSV_PATH}...")
    
    try:
        # Read the CSV
        df = pd.read_csv(CSV_PATH)
        original_count = len(df)
        
        print(f"Original record count: {original_count}")
        
        # Remove completely empty rows
        df = df.dropna(how='all')
        after_empty_removal = len(df)
        
        # Remove rows where reg76_id is empty/NaN
        if 'reg76_id' in df.columns:
            df = df[df['reg76_id'].notna()]
            df = df[df['reg76_id'].astype(str).str.strip() != '']
        
        final_count = len(df)
        
        # Save cleaned CSV
        df.to_csv(CSV_PATH, index=False)
        
        print(f"\nCleanup Complete!")
        print(f"   - Removed {original_count - after_empty_removal} completely empty rows")
        print(f"   - Removed {after_empty_removal - final_count} rows with invalid IDs")
        print(f"   - Final record count: {final_count}")
        
        if final_count > 0:
            print(f"\nRemaining records:")
            print(df[['reg76_id', 'vehicle_no', 'created_at']].to_string(index=False))
        else:
            print(f"\nCSV is now clean with only headers!")
            
    except Exception as e:
        print(f"ERROR during cleanup: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("Reg-76 CSV Cleanup Utility")
    print("=" * 60)
    print()
    
    cleanup_csv()
    
    print()
    print("=" * 60)
    print("Next Steps:")
    print("   1. Run the Streamlit app")
    print("   2. Go to Administrative View tab")
    print("   3. Click 'Sync with GSheet' to update Google Sheets")
    print("=" * 60)
