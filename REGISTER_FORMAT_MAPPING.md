# Register Format Mapping Guide

This document maps the official **Register Format.xlsx** workbook to the current data model
used by the Streamlit application. It focuses on the registers that are actively used in
manual entry (Reg‑76, Reg‑74, Reg‑A, Reg‑B, Excise Duty) and the automated daily synopsis
(Reg‑78).

> **Note:** The workbook uses multi‑row and merged headers. The mapping below treats each
> *logical* column/section as a field group rather than relying on a single header row.

---

## 1) REG‑76 (Sheet: **REG 76**)

### Header / Identity Fields
| Excel label | App field (schema.py) | Notes |
| --- | --- | --- |
| Import Permit No./Transport Pass No. | `permit_no` | Primary pass number in system. |
| Name of Exporting/Transporting Distillery | `distillery` | Source distillery name. |
| Vechile No./Tanker No. | `vehicle_no` | Vehicle/tanker identifier. |
| Date of Arrival | `date_arrival` | Date tanker arrives. |
| Date of Receipt & date of Examination | `date_receipt` | Receipt/exam date. |
| Export/import Order No. & Date | `export_order_no`, `export_order_date` / `import_order_no`, `import_order_date` | Template combines order no + date; store both if available. |
| Export/Import Pass No. & Date | `export_pass_no`, `export_pass_date` / `import_pass_no`, `import_pass_date` | Template combines pass no + date. |
| Nature of Spirit | `spirit_nature` | Spirit type. |
| No. of drum or Tanker | `num_tankers` | Count of drums/tankers. |
| Capacity of each Drum/Tanker | `tanker_capacity` | Capacity per tanker/drum. |
| Weight of Empty Drum/Tanker | `empty_tanker_weight_kg` | Already in schema. |
| weight of spirit in Advice (in Kg) | `adv_weight_kg` | Advised mass. |
| Average density of Spirit (gm/cc) | `adv_avg_density` | Advised average density. |
| Average Temperature of Spirit | `adv_temp` | Advised temp. |

### Advised / Received Quantity Grid (multi‑column section)
The sheet has a **“Details of Advised Quantity”** and **“Details of Advised and Received Quantity”** block with
columns like mass, volume, strength, temperature, etc. Map the grid values to:

| Excel label | App field | Notes |
| --- | --- | --- |
| Mass (in kg.) | `adv_weight_kg` / `rec_mass_kg` | Use advised vs received rows. |
| Volume in BL at given temperature | `adv_bl` / `rec_bl` | Bulk liters at given temp. |
| Volume in BL at 20°C | `adv_bl_20c` / `rec_bl_20c` | Normalized to 20°C. |
| Temperature | `adv_temp` / `rec_unload_temp` | Advised vs received. |
| Indication | `indication` | In schema (advised section). |
| Strength (in % v/v) | `adv_strength` / `rec_strength` | Advised vs received. |
| Mass (in kg) (received) | `rec_mass_kg` | For unloading section. |
| Density at 20°C | `rec_density_20c` | Received density. |
| Density at unloading temperature | `rec_density_at_temp` | Received density. |

### Weighbridge / Transit Differences
| Excel label | App field | Notes |
| --- | --- | --- |
| Laden weight (Consignee) | `wb_laden_consignee` | If available in template. |
| Unladen weight (Consignee) | `wb_unladen_consignee` |  |
| Laden weight (Pass) | `wb_laden_pass` |  |
| Unladen weight (Pass) | `wb_unladen_pass` |  |
| Difference / Transit Wastage | `diff_advised_al`, `transit_wastage_al`, `transit_increase_al` | From advised vs received. |
| Allowable / Chargeable Wastage | `allowable_wastage_al`, `chargeable_wastage_al` |  |

---

## 2) Reg‑74 (Sheet: **Reg-74**)
The Reg‑74 sheet is a wide matrix of *opening balance*, *receipts*, *issues/transfer*, and *closing balance*.
The app stores Reg‑74 in **long‑form rows**, so each operation record should be mapped by context.

### Core Identity
| Excel label | App field (reg74_schema.py) | Notes |
| --- | --- | --- |
| Date & Hours | `operation_date` | Combine date + time if available. |
| Nature of operations to be noted in this column | `operation_type` | Also store in `operation_remarks` if needed. |
| Remarks | `wastage_remarks` / `operation_remarks` | Depends on usage. |

### Opening Balance (RLT/Alcoholmeter)
| Excel label | App field | Notes |
| --- | --- | --- |
| Dip in CM | `opening_dip_cm` | From RLT. |
| Temperature in Deg.C | `opening_temp` |  |
| Indication in Alcoholmeter | `opening_indication` |  |
| Strength in % v/v | `source_opening_strength` | Opening strength. |
| Volume in Bulk Litre | `source_opening_bl` | Opening BL. |
| Volume in Alcoholic Litre | `source_opening_al` | Opening AL. |
| From Which Receiver | `source_vat` | SST/BRT VAT. |

### Receipts (MFM‑I / VAT / Cask)
| Excel label | App field | Notes |
| --- | --- | --- |
| Qty Received through Mass flow meter‑I | `receipt_bl` | Volume received in BL. |
| Average Strength recorded by MFM‑I | `receipt_strength` |  |
| Quantity received in A.L | `receipt_al` |  |
| From which VAT | `source_vat` | If applicable. |
| total No. of Cask or Drum | `num_tankers` (if stored elsewhere) | Not yet modeled in Reg‑74 schema. |

### Increase / Audit
| Excel label | App field | Notes |
| --- | --- | --- |
| Operational Increase | `storage_wastage_bl` (positive) | If increase captured, store in `storage_wastage` with sign. |
| Increase found during stock Audit | `storage_wastage_note` | Or dedicated audit fields if added. |

### Issues / Transfers (MFM‑II)
| Excel label | App field | Notes |
| --- | --- | --- |
| Destination or VAT No | `destination_vat` |  |
| Qty Transferred in BL | `issue_bl` |  |
| Strength recorded by MFM‑II | `issue_strength` |  |
| Quantity transferred in AL | `issue_al` |  |

### Closing Balance
| Excel label | App field | Notes |
| --- | --- | --- |
| Final dip in CM | `dip_reading_cm` |  |
| Final Volumn of spirit in bulk litre | `closing_bl` |  |
| Strength in % v/v | `closing_strength` |  |
| Qty in Alcoholic Litre | `closing_al` |  |
| Sprit left in the VAT after production as dead stock in AL | `closing_al` | Same target field. |

---

## 3) REG‑A (Sheet: **REG-A**)
The Reg‑A sheet is structured by **batch** with a **bottling size grid**. The app stores this in one
row per batch with dedicated bottle count columns.

### Core Batch / Transfer Info
| Excel label | App field (rega_schema.py) | Notes |
| --- | --- | --- |
| BASE BATCH No. | `batch_no` | App uses `batch_no` + `session_number`. |
| BATCH START DATE | `production_date` | If distinct, store in `production_date`. |
| BRAND NAME | `brand_name` |  |
| ALLOTED VAT No. | `source_brt_vat` | BRT vat. |
| FROM VAT No. | `source_brt_vat` | Use same if only one field. |
| STR IN % v/v | `brt_opening_strength` |  |
| VOLUME IN BL | `brt_opening_bl` |  |
| VOLUME IN AL | `brt_opening_al` |  |
| TO VAT No. | `destination_vat` | Not in schema; store in `warehouse_location` if needed. |

### MFM‑II Transfer
| Excel label | App field | Notes |
| --- | --- | --- |
| AVG DENSITY IN gm/cc | `mfm2_density` |  |
| AVG TEMP IN deg C | `mfm2_temperature` |  |
| AVG STR IN % v/v | `mfm2_strength` |  |
| TOTAL VOLUME TRANSFER IN BL | `mfm2_total_passed` / `mfm2_reading_bl` | Use one, prefer `mfm2_total_passed`. |
| TOTAL VOLUME TRANSFER IN AL | `mfm2_reading_al` |  |

### Bottling Counts (Bottle Counter)
| Excel label | App field | Notes |
| --- | --- | --- |
| 750 | `bottles_750ml` | Bottle counts. |
| 600 | `bottles_600ml` |  |
| 500 | `bottles_500ml` |  |
| 375 | `bottles_375ml` |  |
| 300 | `bottles_300ml` |  |
| 180 | `bottles_180ml` |  |
| SPIRIT BOTTLED IN BL | `bottles_total_bl` |  |
| SPIRIT BOTTLED IN AL | `bottles_total_al` |  |

### Wastage / Increase
| Excel label | App field | Notes |
| --- | --- | --- |
| PRODUCTION INCREASE | `production_increase_al` |  |
| PRODUCTION WASTAGE | `wastage_al` |  |
| ALLOWABLE WASTAGE | `allowable_limit` |  |
| CHARGEABLE WASTAGE | `chargeable_wastage_al` |  |

---

## 4) REG‑78 (Sheet: **REG-78**)
This sheet is the **daily synopsis** (auto‑generated). It is organized as a 15‑column summary.
The app schema stores BL and AL separately.

| Excel column | Excel label (row 9) | App field (reg78_schema.py) | Notes |
| --- | --- | --- | --- |
| 1 | Date Hour | `synopsis_date`, `synopsis_hour` | Split date/time. |
| 2 | Balance in hand | `opening_balance_al` | Sheet is in AL. |
| 3 | Consignment of strong spirit received through Pass Number | `consignment_pass_numbers` | Also store count in `consignment_count`. |
| 4 | Quantity of spirit received through Mass Flow Meter‑I | `mfm1_total_al` |  |
| 5 | Operational Increase | `operational_increase_al` |  |
| 6 | Production Increase | `production_increase_al` |  |
| 7 | Increase during stock Audit | `audit_increase_al` |  |
| 8 | Total balance in hand (sum of col. 2 to 7) | `total_credit_al` |  |
| 9 | Issues on payment of duty | `issues_on_duty_al` |  |
| 10 | Sample drawn | `sample_drawn_al` |  |
| 11 | Operational wastage | `operational_wastage_al` |  |
| 12 | Production wastage | `production_wastage_al` |  |
| 13 | Wastage during stock Audit | `audit_wastage_al` |  |
| 14 | Total debit (sum of col. 9 to 13) | `total_debit_al` |  |
| 15 | Spirit left in vats | `closing_balance_al` |  |

> **Automation scope:** Reg‑78 should aggregate from **Reg‑76 receipts**, **Reg‑74 operations**,
> and **Reg‑A production**. The app already has helper functions for Reg‑76 and Reg‑74; those
> should be used together with Reg‑A totals.

---

## 5) REG‑B (Sheet: **REG-B**)
Reg‑B is a *matrix register* by **product strength** and **bottle size**. The app stores this in a
**long‑form table** (`regb_bottle_stock`) so each product/size is a row.

### Mapping Strategy (long‑form rows)
| Excel group | App fields (regb_schema.py) | Notes |
| --- | --- | --- |
| Product header (e.g., 500 UP 28.5% v/v) | `product_name`, `strength` | Product name & strength for row. |
| Bottle size (750/600/500/375/300/180) | `bottle_size_ml` | One row per size. |
| Opening Balance in hand | `opening_balance_bottles` | Section header row 4. |
| Quantity Received of Bottle | `quantity_received_bottles` |  |
| Total Bottle to be Accounted | `total_accounted_bottles` |  |
| Wastage/Breakage of Bottle | `wastage_breakage_bottles` |  |
| Issue on Payment of Duty | `issue_on_duty_bottles` |  |
| Closing in Hand of Bottle | `closing_balance_bottles` |  |
| AL Liters column (per section) | `opening_balance_al` / `received_al` / `total_al` / `wastage_al` / `issue_al` / `closing_al` | Map to AL equivalents. |

> **Tip:** This sheet can be exported by **pivoting** the long‑form table into the matrix
> layout so the official format is preserved.

---

## 6) Excise Duty (Sheet: **Excise Duty**)
Excise Duty includes both **ledger‑level** totals and **issued bottle details**. The app uses
`excise_duty_ledger` for ledger totals and `excise_duty_bottles` for per‑size details.

### Ledger Mapping
| Excel label | App field (excise_duty_schema.py) | Notes |
| --- | --- | --- |
| Date | `date` | Ledger date. |
| Opening Balance | `opening_balance` |  |
| Deposit Amount | `deposit_amount` |  |
| E Challan No. & Date | `echallan_no`, `echallan_date` | Split number/date. |
| Total Amount Credited | `amount_credited` |  |
| Date of Issue | `date` | Use in ledger, and per issue rows. |
| Name of the Warehouse/Depot | `name_of_issue` |  |
| Transport Pass No. | `transport_permit_no` |  |
| Bottles Issued (AL) | `total_duty_amount` | Sum of AL and duty. |
| Amount of duty Debited | `duty_debited` |  |
| Closing Balance | `closing_balance` |  |
| Remarks | `remarks` |  |
| Signature of the Excise Officer | `excise_officer_signature` |  |

### Issued Bottle Detail Mapping
| Excel label | App field (excise_duty_bottles table) | Notes |
| --- | --- | --- |
| Product group (500/600/700/800 UP) | `product_name`, `strength` | Based on section headers. |
| Bottle size (750/600/500/375/300/180) | `bottle_size_ml` | One row per size. |
| Issued bottle quantity | `qty_issued` |  |
| BL issued | `bl_issued` |  |
| AL issued | `al_issued` |  |
| Duty rate per BL | `duty_rate_per_bl` |  |
| Duty amount | `duty_amount` |  |

---

## Recommended Next Steps
1. **Confirm any ambiguous columns** (e.g., combined “Order No & Date” fields) and decide
   whether to split values or store raw text.
2. **Add a sheet export layer** so the app can save data directly into the official template
   layout (pivoting for Reg‑B and Excise Duty).
3. **Wire Reg‑78 aggregation** to combine Reg‑76 + Reg‑74 + Reg‑A (already partially present).

