# Reg-74 Format Comparison & Updates

## Official Excel Format Analysis
The official Reg-74 format ("Register Format.xlsx") is a comprehensive spirit store register with 41 columns, tracking:
1.  **Opening Balance**: Dip, Temp, Indication, Strength, BL, AL.
2.  **Receipts**: Source, MFM details, Vat/Cask details.
3.  **Increases**: Operational & Audit.
4.  **Closing (Verification)**: Dip, RLT Reading, Strength, AL.
5.  **Wastage**: Operational & Audit.
6.  **Issues/Transfers**: Destination, RLT Reading, Strength, AL.
7.  **Production Issues**: To Reg-A, BL, Density, Strength, AL.
8.  **Final Closing**: Dip, BL, Strength, AL.

## Implementation Status
Our implementation (`reg74.py`) uses an **Operation-Based Approach** (Unloading, Transfer, Reduction, Issue), which is more user-friendly than a giant 41-column table. However, we ensure all necessary data points are captured to generate the official report.

### Gaps Identified & Fixed
We compared our form against the 41 columns and found the following missing fields, which have now been added:

| Official Column | Field Name | Status | Action Taken |
| :--- | :--- | :--- | :--- |
| 2 | Dip in CM (Opening) | ❌ Missing | **Added** to Wastage Verification Section |
| 3 | Temperature (Opening) | ❌ Missing | **Added** to Wastage Verification Section |
| 4 | Indication (Opening) | ❌ Missing | **Added** to Wastage Verification Section |
| 35 | Final dip in CM (Closing) | ✅ Present | Existing `dip_reading` field mapped |
| (Derived) | Closing Indication | ❌ Missing | **Added** `closing_indication` to Section 3 |

### Backend Updates
1.  **Schema**: Updated `reg74_schema.py` to include `opening_dip_cm`, `opening_temp`, `opening_indication`, `closing_indication`.
2.  **Storage**: Updated `reg74_backend.py` and `desktop_storage.py` to save Reg-74 data to:
    -   `C:\Users\Lenovo\Desktop\Excise_Register_Data\Reg74_Data.xlsx`

## How to Use
1.  **Select Operation**: Choose Unloading, Transfer, etc.
2.  **Verify Opening Stock**: Enter the physical Dip, Temp, and Indication to verify against book stock.
3.  **Enter Transaction**: Fill in the BL/AL quantities.
4.  **Verify Closing**: Enter the final Dip and Indication.
5.  **Submit**: Data is saved to the Desktop Excel file.
