import pandas as pd
import sqlite3
from datetime import datetime
import sys

print("=" * 60)
print("IMPORTING DECEMBER DATA TO MAINTENANCE DATABASE")
print("=" * 60)

# Read CSV
csv_path = r"C:\Users\Lenovo\Desktop\Daily Activity Database - Activity.csv"
print(f"\n1. Reading CSV from: {csv_path}")

try:
    df = pd.read_csv(csv_path)
    print(f"   ✓ Found {len(df)} total rows")
    print(f"\n   Columns: {list(df.columns)}")
except Exception as e:
    print(f"   ✗ Error reading CSV: {e}")
    input("\nPress Enter to exit...")
    sys.exit(1)

# Clean data
print("\n2. Cleaning data...")
df = df.dropna(subset=['Date'])
df = df[df['Date'].str.strip() != '']
print(f"   ✓ {len(df)} rows after removing empty dates")

# Convert dates
print("\n3. Converting dates...")
df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y', errors='coerce')
df = df.dropna(subset=['Date'])
print(f"   ✓ {len(df)} rows with valid dates")

# Filter for December 4-30, 2025
print("\n4. Filtering for Dec 4-30, 2025...")
df = df[(df['Date'] >= '2025-12-04') & (df['Date'] <= '2025-12-30')]
print(f"   ✓ {len(df)} activities in date range")

if len(df) == 0:
    print("\n   ✗ No data found in the date range!")
    input("\nPress Enter to exit...")
    sys.exit(1)

# Connect to database
db_path = 'excise_registers.db'
print(f"\n5. Connecting to database: {db_path}")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check if table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='maintenance_activities'")
if not cursor.fetchone():
    print("   ✗ Table doesn't exist! Creating it...")
    cursor.execute("""
        CREATE TABLE maintenance_activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            instruments TEXT NOT NULL,
            serial_numbers TEXT NOT NULL,
            activity_description TEXT NOT NULL,
            detailed_steps TEXT NOT NULL,
            time_spent_hours REAL NOT NULL,
            technician TEXT NOT NULL,
            issues_found TEXT,
            resolution TEXT,
            billing_category TEXT NOT NULL,
            billing_section TEXT NOT NULL,
            notes TEXT,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    print("   ✓ Table created")

# Clear existing December data to avoid duplicates
print("\n6. Clearing existing December data (if any)...")
cursor.execute("DELETE FROM maintenance_activities WHERE date >= '2025-12-04' AND date <= '2025-12-30'")
deleted = cursor.rowcount
conn.commit()
print(f"   ✓ Deleted {deleted} existing records")

# Import records
print("\n7. Importing activities...")
imported = 0
errors = 0

for idx, row in df.iterrows():
    try:
        # Handle missing values and get correct column names
        time_spent = float(row['Time Spend (Hours)']) if pd.notna(row['Time Spend (Hours)']) else 1.0
        technician = row['Technician Name'] if pd.notna(row['Technician Name']) else "E+H Residential Engineer"
        issues = row['Issues Identified'] if pd.notna(row['Issues Identified']) else "None"
        resolution = row['Resolution Applied'] if pd.notna(row['Resolution Applied']) else "No action needed"
        
        # Try to get billing category - handle the special character
        billing_cat = "c"  # default
        for col in df.columns:
            if 'Billing Category' in col:
                val = row[col]
                if pd.notna(val):
                    billing_cat = str(val).lower().strip()
                    # Ensure it's a single letter a-d
                    if billing_cat not in ['a', 'b', 'c', 'd']:
                        billing_cat = 'c'
                break
        
        notes = row['Notes/Attached'] if pd.notna(row['Notes/Attached']) else ""
        
        cursor.execute("""
            INSERT INTO maintenance_activities 
            (date, instruments, serial_numbers, activity_description, detailed_steps,
             time_spent_hours, technician, issues_found, resolution, billing_category,
             billing_section, notes, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row['Date'].date().isoformat(),
            row['Instrument/Group'],
            row['Serial Number'],
            row['Activity Description'],
            row['Detailed Steps performed'],
            time_spent,
            technician,
            issues,
            resolution,
            billing_cat,
            'Confidential/Internal',
            notes,
            datetime.now().isoformat()
        ))
        imported += 1
        
        if imported % 10 == 0:
            print(f"   ... {imported} activities imported")
            
    except Exception as e:
        errors += 1
        print(f"   ✗ Error on row {idx}: {str(e)}")
        continue

conn.commit()
conn.close()

print("\n" + "=" * 60)
print(f"✓✓✓ IMPORT COMPLETE! ✓✓✓")
print(f"✓ Successfully imported: {imported} activities")
if errors > 0:
    print(f"✗ Errors: {errors}")
print("=" * 60)

print("\n📊 SUMMARY:")
print(f"   Date Range: Dec 4-30, 2025")
print(f"   Activities: {imported}")
print(f"   Database: excise_registers.db")

print("\n🎯 NEXT STEPS:")
print("   1. Go to your Streamlit app: http://localhost:8501")
print("   2. Press F5 to refresh the page")
print("   3. Click '🔧 Maintenance Log' in sidebar")
print("   4. Click '📄 Monthly Report' tab")
print("   5. Set dates: 2025-12-04 to 2025-12-30")
print("   6. You should see preview metrics now!")
print("   7. Click 'Generate PDF Report'")
print("\n✓✓✓ Ready to generate your report! ✓✓✓")

input("\nPress Enter to close...")
