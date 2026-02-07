# Reg-A Format Comparison & Updates

## Official Excel Format Analysis
The official Reg-A format is the "Production Register" which tracks the conversion of bulk spirit into finished bottles.
Key columns identified in `REG-A` sheet:
1.  **Input**: From VAT No, Strength, Volume (BL/AL).
2.  **Process**: Batch No, Production Date, MFM-II Readings (Density, Temp, Strength, Volume).
3.  **Output (Bottles)**: Detailed columns for bottle counts: `750`, `600`, `500`, `375`, `300`, `180`.
4.  **Wastage/Increase**: `Production Increase`, `Production Wastage`, `Allowable Wastage`, `Chargeable Wastage`.

## Implementation Status
Our `RegA` implementation tracks "Bottling Operations".

### Gaps Identified & Fixed
| Official Column | Field Name | Status | Action Taken |
| :--- | :--- | :--- | :--- |
| 23, 24, 26 | Bottle Counts (600ml, 500ml, 300ml) | ❌ Missing | **Added** to Schema |
| 31 | Production Increase | ❌ Missing | **Added** `production_increase_al` to Schema |
| 34 | Chargeable Wastage | ❌ Missing | **Added** `chargeable_wastage_al` to Schema |

### Backend Updates
1.  **Schema**: Updated `rega_schema.py` to include:
    -   `bottles_300ml`, `bottles_500ml`, `bottles_600ml` (and corresponding BL/Case fields).
    -   `production_increase_al`.
    -   `chargeable_wastage_al`.

## Next Steps
-   Update `rega.py` UI to show these new bottle size inputs.
-   Ensure backend logic calculates `chargeable_wastage` (Wastage - Allowable).
