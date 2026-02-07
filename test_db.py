import sqlite3
from datetime import date

conn = sqlite3.connect('excise_registers.db')
cursor = conn.cursor()

# Check all dates in database
cursor.execute('SELECT date, instruments, time_spent_hours FROM maintenance_activities ORDER BY date DESC LIMIT 10')
results = cursor.fetchall()

print(f"Total records found: {len(results)}")
print("\nRecent entries:")
for r in results:
    print(f"  Date: {r[0]}, Instruments: {r[1][:50]}..., Hours: {r[2]}")

# Check with date range
cursor.execute('SELECT COUNT(*) FROM maintenance_activities WHERE date >= ? AND date <= ?', ('2025-12-04', '2026-01-01'))
count = cursor.fetchone()[0]
print(f"\nRecords between 2025-12-04 and 2026-01-01: {count}")

conn.close()
