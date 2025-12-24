import pandas as pd
import json

CSV_PATH = "reg76_data.csv"
df = pd.read_csv(CSV_PATH)
df_clean = df.fillna("")
data = [df_clean.columns.values.tolist()] + df_clean.values.tolist()

try:
    json.dumps(data)
    print("JSON check passed")
except Exception as e:
    print(f"JSON check failed: {e}")
    # Deep check
    for i, row in enumerate(data):
        for j, val in enumerate(row):
            try:
                json.dumps(val)
            except:
                print(f"Non-compliant value at row {i}, col {j}: {val} (type: {type(val)})")
