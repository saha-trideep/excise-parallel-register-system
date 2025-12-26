"""
Debug script to check what's happening with Reg-76 data
"""

import pandas as pd
import os

CSV_PATH = "reg76_data.csv"

print("=" * 70)
print("REG-76 DEBUG INFORMATION")
print("=" * 70)
print()

# Check if file exists
if not os.path.exists(CSV_PATH):
    print("ERROR: reg76_data.csv NOT FOUND!")
    exit(1)

print(f"File exists: {CSV_PATH}")
print(f"File size: {os.path.getsize(CSV_PATH)} bytes")
print()

# Read the CSV
df = pd.read_csv(CSV_PATH)
print(f"Total rows in CSV (including empty): {len(df)}")
print()

# Show raw data
print("Raw CSV content (first 3 rows):")
print(df.head(3))
print()

# Clean empty rows
df_clean = df.dropna(how='all')
print(f"After removing completely empty rows: {len(df_clean)}")
print()

# Check reg76_id column
if 'reg76_id' in df_clean.columns:
    print("reg76_id column exists")
    print(f"Non-null reg76_id count: {df_clean['reg76_id'].notna().sum()}")
    print()
    
    # Filter valid IDs
    df_valid = df_clean[df_clean['reg76_id'].notna()]
    df_valid = df_valid[df_valid['reg76_id'].astype(str).str.strip() != '']
    
    print(f"After filtering valid reg76_id: {len(df_valid)}")
    print()
    
    if len(df_valid) > 0:
        print("VALID RECORDS FOUND:")
        print("-" * 70)
        for idx, row in df_valid.iterrows():
            print(f"  ID: {row['reg76_id']}")
            print(f"  Vehicle: {row['vehicle_no']}")
            print(f"  Created: {row['created_at']}")
            print()
    else:
        print("NO VALID RECORDS FOUND!")
        print()
else:
    print("ERROR: reg76_id column NOT FOUND in CSV!")
    print()

# Check what filter_records would return
print("=" * 70)
print("SIMULATING filter_records() function:")
print("=" * 70)

# Simulate the backend function
if 'reg76_id' in df_clean.columns:
    df_filtered = df_clean[df_clean['reg76_id'].notna()]
    df_filtered = df_filtered[df_filtered['reg76_id'].astype(str).str.strip() != '']
    
    print(f"Records that would be returned: {len(df_filtered)}")
    print(f"Is empty? {df_filtered.empty}")
    print()
    
    if not df_filtered.empty:
        print("✓ DELETE SECTION SHOULD BE VISIBLE!")
        print()
        print("Available record IDs for deletion:")
        for rid in df_filtered['reg76_id'].tolist():
            print(f"  - {rid}")
    else:
        print("✗ DELETE SECTION WILL BE HIDDEN (no records)")
else:
    print("✗ Cannot simulate - reg76_id column missing")

print()
print("=" * 70)
print("DIAGNOSIS:")
print("=" * 70)

if len(df_valid) > 0:
    print("✓ You HAVE records in the CSV")
    print("✓ The delete section SHOULD be visible")
    print()
    print("POSSIBLE ISSUES:")
    print("  1. Streamlit app not restarted after code changes")
    print("  2. Browser cache showing old version")
    print("  3. Looking at wrong tab (should be ADMINISTRATIVE VIEW)")
    print("  4. VAT filter hiding the records")
    print("  5. Streamlit running from different directory")
else:
    print("✗ NO valid records in CSV")
    print("✗ Delete section will NOT show until you add a record")

print()
print("=" * 70)
