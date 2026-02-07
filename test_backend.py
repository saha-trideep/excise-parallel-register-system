from datetime import date
from maintenance_backend import get_maintenance_activities

# Test the function
start = date(2025, 12, 4)
end = date(2026, 1, 1)

print(f"Testing get_maintenance_activities({start}, {end})")
df = get_maintenance_activities(start, end)

print(f"\nDataFrame shape: {df.shape}")
print(f"Is empty: {df.empty}")
print(f"\nFirst few rows:")
if not df.empty:
    print(df[['date', 'instruments', 'time_spent_hours']].head())
else:
    print("DataFrame is empty!")
