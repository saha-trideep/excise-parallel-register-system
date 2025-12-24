# Excise Duty Register - Implementation Plan

## 📋 Overview

**Register Name:** Register of Personal Ledger Account of Excise Duty for IML  
**Purpose:** Track excise duty payments for issued bottles from Reg-B  
**Integration:** Auto-fills from Reg-B "Issue on Payment of Duty"

---

## 🎯 Key Requirements

### Duty Structure (Per BL):
- **50° U.P. (28.5% v/v)** → ₹50/- per BL
- **60° U.P. (22.8% v/v)** → ₹50/- per BL
- **70° U.P. (17.1% v/v)** → ₹20/- per BL
- **80° U.P. (11.4% v/v)** → ₹17/- per BL

### Bottle Measurements:
750ml, 600ml, 500ml, 375ml, 300ml, 180ml

---

## 📊 Register Structure (From Image)

### Main Columns:

1. **Date**
2. **Opening Balance**
   - Deposit Amount
   - E-Challan No. & Date
3. **Amount Credited**
4. **Name of Issue**
5. **Ware House No.**
6. **Transport Permit No.**

7. **Issued of Bottle/Quantity** (Multi-size columns)
   - 750 ml (Qty, BL, AL)
   - 500 ml (Qty, BL, AL)
   - 375 ml (Qty, BL, AL)
   - 180 ml (Qty, BL, AL)
   - 90 ml (Qty, BL, AL)
   - 60 ml (Qty, BL, AL)

8. **Amount of Duty**
   - Issued
   - Debited for the Issue

9. **Balance**
10. **Remarks**

---

## 🗄️ Database Schema

### Table: `excise_duty_ledger`

```sql
CREATE TABLE excise_duty_ledger (
    duty_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    
    -- Financial Account
    opening_balance REAL NOT NULL DEFAULT 0.00,
    deposit_amount REAL NOT NULL DEFAULT 0.00,
    echallan_no TEXT,
    echallan_date TEXT,
    amount_credited REAL NOT NULL DEFAULT 0.00,
    
    -- Issue Details
    name_of_issue TEXT,
    warehouse_no TEXT,
    transport_permit_no TEXT,
    
    -- Duty Calculation
    total_duty_amount REAL NOT NULL DEFAULT 0.00,
    duty_debited REAL NOT NULL DEFAULT 0.00,
    closing_balance REAL NOT NULL DEFAULT 0.00,
    
    -- Administrative
    remarks TEXT,
    excise_officer_name TEXT,
    status TEXT NOT NULL DEFAULT 'draft',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
```

### Table: `excise_duty_bottles`

```sql
CREATE TABLE excise_duty_bottles (
    duty_bottle_id INTEGER PRIMARY KEY AUTOINCREMENT,
    duty_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    
    -- Product Details
    product_name TEXT NOT NULL,
    strength REAL NOT NULL,
    bottle_size_ml INTEGER NOT NULL,
    
    -- Quantities
    qty_issued INTEGER NOT NULL DEFAULT 0,
    bl_issued REAL NOT NULL DEFAULT 0.000,
    al_issued REAL NOT NULL DEFAULT 0.000,
    
    -- Duty Calculation
    duty_rate_per_bl REAL NOT NULL,
    duty_amount REAL NOT NULL DEFAULT 0.00,
    
    FOREIGN KEY (duty_id) REFERENCES excise_duty_ledger(duty_id)
);
```

---

## 🔄 Integration with Reg-B

### Auto-Fill Logic:

When user issues bottles in Reg-B:
1. **Capture Issue Data:**
   - Product name, strength, bottle size
   - Quantity issued
   - BL and AL issued
   
2. **Calculate Duty:**
   ```python
   duty_rate = get_duty_rate_for_strength(strength)
   duty_amount = bl_issued × duty_rate
   ```

3. **Create Duty Entry:**
   - Auto-populate bottle details
   - Calculate total duty
   - Debit from balance

---

## 💰 Duty Rate Mapping

```python
DUTY_RATES = {
    Decimal("28.5"): Decimal("50.00"),  # 50° U.P. → ₹50/BL
    Decimal("22.8"): Decimal("50.00"),  # 60° U.P. → ₹50/BL
    Decimal("17.1"): Decimal("20.00"),  # 70° U.P. → ₹20/BL
    Decimal("11.4"): Decimal("17.00")   # 80° U.P. → ₹17/BL
}
```

---

## 🧮 Key Calculations

### 1. Duty Amount per Product:
```
Duty Amount = BL Issued × Duty Rate per BL
```

**Example (60° U.P., 750ml, 100 bottles):**
- BL = (100 × 750) / 1000 = 75.000 BL
- Duty Rate = ₹50/BL
- Duty Amount = 75.000 × ₹50 = ₹3,750.00

### 2. Total Duty for All Products:
```
Total Duty = Σ (Duty Amount for each product variant)
```

### 3. Balance Calculation:
```
Amount Credited = Opening Balance + Deposit Amount
Closing Balance = Amount Credited - Duty Debited
```

---

## 🎨 UI Design (Streamlit)

### Section 1: Financial Account
- Opening Balance (auto from previous day)
- Deposit Amount
- E-Challan No. & Date
- Amount Credited (auto-calculated)

### Section 2: Issue Details
- Name of Issue (customer/distributor)
- Warehouse No.
- Transport Permit No.

### Section 3: Bottle Issues (Multi-Product Table)
Dynamic table with columns:
- Product Name
- Strength (U.P.)
- Bottle Size
- Qty Issued (auto from Reg-B)
- BL Issued (auto-calculated)
- AL Issued (auto-calculated)
- Duty Rate (auto from strength)
- Duty Amount (auto-calculated)

### Section 4: Duty Summary
- Total Duty Amount
- Duty Debited
- Closing Balance

---

## 📋 Data Flow

### Daily Workflow:

1. **User Issues Bottles in Reg-B**
   - Enters "Issue on Payment of Duty" quantity
   - Saves Reg-B entry

2. **Navigate to Excise Duty Register**
   - Select same date
   - System auto-fills issued bottles from Reg-B

3. **Enter Financial Details**
   - Opening balance (auto from previous day)
   - Deposit amount (if any)
   - E-Challan details

4. **Enter Issue Details**
   - Name of issue
   - Warehouse number
   - Transport permit number

5. **Review Auto-Calculated Duty**
   - System shows duty for each product
   - Total duty calculated
   - Balance computed

6. **Save Entry**
   - Validates balance
   - Saves to database

---

## 🔍 Validation Rules

1. **Balance Check:**
   ```
   Amount Credited ≥ Duty Debited
   ```

2. **Closing Balance:**
   ```
   Closing Balance = Amount Credited - Duty Debited
   ```

3. **Duty Calculation:**
   ```
   Duty Amount = BL × Duty Rate (must match)
   ```

4. **Issue Quantity:**
   ```
   Qty in Duty Register ≤ Qty Issued in Reg-B
   ```

---

## 📊 Reports & Views

### 1. Daily Entry View
- Single date entry with all details

### 2. Summary View
- Total duty collected
- Total bottles issued (by size/strength)
- Balance summary

### 3. Administrative View
- Multi-date reports
- Duty collection trends
- Product-wise duty breakdown
- PDF export

---

## 🔗 Integration Points

### From Reg-B:
- Fetch issued bottles (by date, product, size, strength)
- Get BL and AL values
- Auto-populate duty register

### To Reports:
- Daily duty collection
- Monthly duty summary
- Product-wise duty analysis

---

## 📝 Example Entry

### Date: 2025-01-24

**Financial:**
- Opening Balance: ₹10,000.00
- Deposit: ₹5,000.00
- E-Challan: ECH/2025/001235
- Amount Credited: ₹15,000.00

**Issue Details:**
- Name: ABC Distributors
- Warehouse: WH-001
- Transport Permit: TP/2025/0456

**Bottles Issued:**

| Product | Strength | Size | Qty | BL | AL | Rate | Duty |
|---------|----------|------|-----|----|----|------|------|
| Country Liquor | 60° U.P. (22.8%) | 750ml | 100 | 75.000 | 17.100 | ₹50 | ₹3,750.00 |
| Country Liquor | 60° U.P. (22.8%) | 375ml | 200 | 75.000 | 17.100 | ₹50 | ₹3,750.00 |
| Country Liquor | 70° U.P. (17.1%) | 750ml | 50 | 37.500 | 6.413 | ₹20 | ₹750.00 |

**Duty Summary:**
- Total Duty: ₹8,250.00
- Duty Debited: ₹8,250.00
- Closing Balance: ₹6,750.00

---

## 🚀 Implementation Steps

### Phase 1: Schema & Backend
1. Create `excise_duty_schema.py`
2. Create `excise_duty_backend.py`
3. Create `excise_duty_utils.py`

### Phase 2: Integration
4. Add Reg-B integration functions
5. Implement duty calculation logic
6. Add validation rules

### Phase 3: UI
7. Create `excise_duty_register.py` (Streamlit)
8. Implement financial account section
9. Implement issue details section
10. Implement bottle issues table
11. Implement duty summary

### Phase 4: Testing & Polish
12. Test with sample data
13. Verify calculations
14. Add PDF export
15. Add reports

---

## 🎯 Success Criteria

✅ Auto-fills issued bottles from Reg-B  
✅ Correct duty calculation based on strength  
✅ Multi-size bottle tracking  
✅ Balance validation  
✅ E-Challan tracking  
✅ Transport permit tracking  
✅ Daily summary generation  
✅ Premium UI with clear duty breakdown  

---

## 📌 Notes

- Duty rates are strength-specific
- All BL calculations must be precise (3 decimals)
- Balance must never go negative
- Integration with Reg-B is critical
- Transport permit is mandatory for issues
- E-Challan required for deposits

---

**Ready to implement!** 🚀
