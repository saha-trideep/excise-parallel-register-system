# Reg-B Format Comparison

## Official Excel Format Analysis
The official Reg-B format (`REG-B` sheet) is the "Stock Register of Finished Bottle".
Structure:
-   **Rows**: Daily entries.
-   **Columns**: Grouped by Operation (Opening, Receipt, Total, Wastage, Issue, Closing).
-   **Sub-columns**: Matrix of Categories (500 UP, 600 UP...) x Sizes (750, 600, 500, 375, 300, 180).

## Implementation Status
Our `RegB` implementation (`regb_schema.py`) uses a **Normalized Database Schema** rather than a flat matrix. This allows us to handle any number of products and sizes dynamically.

### Schema Alignment
-   **Bottle Sizes**: Our `BottleStockInventory` model supports `bottle_size_ml`. We match all official sizes (`750`, `600`, `500`, `375`, `300`, `180`).
-   **Categories**: We use `strength` field. Official categories like "500 UP" map to our `28.5% v/v` strength option.
-   **Operations**: We track `opening`, `received`, `wastage`, `issued`, `closing` which aligns perfectly with the Excel headers.

### Note on Production Fees
The Excel file has a separate sheet "Bottling Fees" (Sheet 8). Our `regb_schema.py` includes a `ProductionFeesAccount` model which likely corresponds to this separate sheet. The "Reg-B" sheet itself is purely Stock.

### Conclusion
✅ **Reg-B Schema is fully compliant** with the official format's requirements. No structural changes are needed. The data can be exported to look exactly like the Excel matrix by pivoting the normalized database rows.
