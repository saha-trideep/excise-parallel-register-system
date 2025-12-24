from pdf_generator import generate_reg76_pdf
import pandas as pd

# Create sample data
sample_data = {
    'reg76_id': ['R76-202512001', 'R76-202512002'],
    'permit_no': ['PAL-3663', 'PAL-3664'],
    'vehicle_no': ['NLOK-12', 'NLOK-13'],
    'distillery': ['Globus Spirits', 'Globus Spirits'],
    'spirit_nature': ['ENA', 'ENA'],
    'date_dispatch': ['2025-12-22', '2025-12-22'],
    'date_receipt': ['2025-12-23', '2025-12-23'],
    'adv_al': [23930.56, 24500.00],
    'rec_al': [24972.37, 25100.00],
    'transit_wastage_al': [0.0, 0.0],
    'storage_vat_no': ['SST-5', 'SST-6'],
    'status': ['Submitted', 'Submitted']
}

df = pd.DataFrame(sample_data)

# Generate PDF
try:
    filename = generate_reg76_pdf(df, "test_reg76.pdf")
    print(f"✅ PDF generated successfully: {filename}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
