# Reg-76 Excel Format Comparison Analysis

## Date: 2026-02-05

## 📋 Official Excel Format (Spirit Transaction Sheet)

The "Spirit Transaction" sheet in `Register Format.xlsx` contains the following columns:

1. **Date**
2. **Strong Spirit Opening Balance**
3. **Strong Spirit Received / Unloaded (through MFM-I)**
4. **In-transit / Unloading Increase**
5. **In-transit / Unloading Wastage**
6. **Strong Spirit Transferred to Blending VATs (through MFM-II)**
7. **Operational Increase in Strong Spirit VATs**
8. **Strong Spirit Closing Balance (must tally with physical VATs)**
9. **Blended / Finished Spirit Opening Balance**
10. **Blended Spirit Received from Strong Spirit**
11. **Operational Increase in Blending/Finished VATs**
12. **Operational Wastage in Blending/Finished VATs**
13. **Sample Drawn**
14. **Spirit Actually Passed to Bottling Lines (through MFM-II)**
15. **Blended / Finished Spirit Closing Balance**
16. **Production Increase**
17. **Production Wastage**
18. **Total Bottles Produced (All sizes combined)**
19. **Total Cases Produced**
20. **Spirit Accounted in Bottled Production (Bottle Qty. × size × strength)**
21. **Net Difference of the Day**
22. **Total Allowable Wastage of the Day**
23. **Chargeable Excess Wastage (if any)**

---

## 🔍 Current Implementation (Our Project)

Our current `reg76.py` implementation captures the following fields:

### Section 1: Basic Consignment Details
- `permit_no` - Import Permit / Transport Pass No.
- `distillery` - Exporting Distillery
- `spirit_nature` - Nature of Spirit (ENA, GENA, RS, Ethanol)
- `vehicle_no` - Vehicle / Tanker No.
- `num_tankers` - Number of Tankers
- `tanker_capacity` - Capacity of Tanker (Full/Partial)
- `tanker_make_model` - Make & Model of Tanker
- `invoice_no` - Invoice No.
- `invoice_date` - Invoice Date
- `export_pass_no` - Export / Import Pass No.
- `export_pass_date` - Pass Date
- `export_order_no` - Export Order No.
- `export_order_date` - Export Order Date
- `import_order_no` - Import Order No.
- `import_order_date` - Import Order Date

### Section 2: Date & Movement
- `date_dispatch` - Date of Dispatch
- `date_arrival` - Date of Arrival
- `date_receipt` - Date of Receipt & Examination
- `days_in_transit` - Transit Duration (calculated)

### Section 3: Advised Quantity
- `adv_weight_kg` - Weight in Advice (kg)
- `adv_avg_density` - Avg Density (gm/cc)
- `adv_strength` - Strength (% v/v)
- `adv_temp` - Temperature (°C)
- `adv_bl` - Advised BL (calculated)
- `adv_al` - Advised AL (calculated)
- `adv_bl_20c` - Advised BL at 20°C (calculated)

### Section 4: Weigh Bridge Data
- `wb_laden_consignee` - Laden at Consignee (kg)
- `wb_unladen_consignee` - Unladen at Consignee (kg)
- `wb_laden_pass` - Laden as per Pass (kg)
- `wb_unladen_pass` - Unladen as per Pass (kg)

### Section 5: Received Quantity (MFM-1)
- `rec_mass_kg` - Mass received (kg) - MFM
- `rec_unload_temp` - Avg Unloading Temp
- `rec_density_at_temp` - Density @ Temp
- `rec_density_20c` - Density @ 20°C
- `rec_strength` - Strength % v/v (MFM)
- `rec_bl` - Received BL (calculated)
- `rec_al` - Received AL (calculated)
- `diff_advised_al` - Variance vs Advice (calculated)

### Section 6: Transit Wastage/Increase
- `transit_wastage_al` - Transit Wastage (AL)
- `transit_increase_al` - Transit Increase (AL)
- `allowable_wastage_al` - Allowable (AL)
- `chargeable_wastage_al` - Chargeable (AL)

### Section 7 & 8: Destination & Remarks
- `storage_vat_no` - Storage VAT No.
- `evc_generated_date` - Online EVC Date
- `excise_remarks` - Official Remarks
- `officer_sig_date` - Officer Name / Signature Tag

### System Fields
- `reg76_id` - Unique Record ID
- `status` - Record Status
- `created_at` - Timestamp

---

## ⚠️ CRITICAL FINDING: Format Mismatch!

### **The Excel format is NOT for Reg-76!**

The "Spirit Transaction" sheet appears to be a **DAILY SUMMARY REGISTER** that combines:
- **Reg-76** (Spirit Receipt)
- **Reg-74** (Spirit Storage/VAT Operations)
- **Reg-A/B** (Production/Bottling)

This is a **consolidated daily report**, NOT the individual Reg-76 receipt form!

### What This Means:
1. **Our Reg-76 implementation is CORRECT** - it captures individual spirit receipt transactions
2. **The Excel sheet is a different register** - likely a daily handbook or summary register
3. **We need to identify the actual Reg-76 format** in the Excel file

---

## 🔎 Next Steps

1. **Check other sheets** in `Register Format.xlsx` to find the actual Reg-76 format
2. **Verify** if there's a separate sheet for individual receipt entries
3. **Confirm** with user which specific format they want for Reg-76

---

## ✅ Current Implementation Status

Our Reg-76 form is comprehensive and captures:
- ✅ All consignment details
- ✅ Movement tracking
- ✅ Advised quantities with calculations
- ✅ Weigh bridge verification
- ✅ Received quantities (MFM-1)
- ✅ Transit wastage/increase calculations
- ✅ Storage destination
- ✅ Official remarks and signatures

**The implementation follows standard excise register practices for spirit receipt documentation.**

---

## 📊 Data Storage

Currently, data is saved to:
- **Local CSV**: `reg76_data.csv` (in project directory)
- **Google Sheets**: Synced automatically

### Requested Change:
- Save Excel files to **Desktop folder**
- Create separate Excel sheets for each register
- Organize in a dedicated folder on Desktop
