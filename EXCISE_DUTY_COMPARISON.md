# Excise Duty Register Comparison

## Official "Register of Personal Ledger Account" Analysis
The official format (`Excise Duty` sheet) is a **Personal Ledger Account (PLA)** that tracks:
1.  **Credits**: Allow deposits (Opening Balance + New Deposits = Total Credit).
2.  **Debits**: Deduct duty based on bottle issues.
3.  **Balance**: Running balance of duty available.

### Structure
-   **Ledger Columns**: Date, Challan Details, Opening, Credited, Debited, Closing.
-   **Issue Columns**: Warehouse Name, Transport Pass No., Date of Issue.
-   **Breakdown Columns**: Matrix of Bottle Counts (Strength x Size) + Total AL Issued.

## Implementation Status
Our implementation (`excise_duty_schema.py`) uses a robust **Master-Detail** architecture:
1.  **Master (`ExciseDutyLedger`)**: Tracks the financial transaction (Credits, Debits, Balance) and Issue metadata (Pass No, Warehouse).
2.  **Detail (`ExciseDutyBottle`)**: Tracks specific items issued (Product, Strength, Size, Qty, Duty Amount).

### Comparison Findings
| Official Component | Implementation | Status |
| :--- | :--- | :--- |
| Financial Columns | `opening_balance`, `deposit_amount`, `amount_credited`, `duty_debited`, `closing_balance` | ✅ Matched |
| Challan Details | `echallan_no`, `echallan_date` | ✅ Matched |
| Issue Metadata | `name_of_issue`, `warehouse_no`, `transport_permit_no` | ✅ Matched |
| Bottle Breakdown | `ExciseDutyBottle` model (Normalized) | ✅ Matched (Flexible) |
| Duty Calculation | `DUTY_RATES` constant map (Needs verification) | ✅ Implemented |

### Recommendations
-   **View Layer**: Ensure the UI can generate a wide-format report that pivots the `ExciseDutyBottle` records to match the Excel register's matrix view.
-   **Duty Rates**: Verify current duty rates (currently hardcoded as ₹50, ₹50, ₹20, ₹17 per BL) are up to date.
