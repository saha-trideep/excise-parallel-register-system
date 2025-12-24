# Reg-B Implementation Plan
## Register for Issue of Country Liquor in Bottles

---

## 📋 **OVERVIEW**

**Purpose:** Track finished bottle inventory and production fees for bottled country liquor ready for issue/sale

**Key Features:**
- Dual tracking: Production Fees Account + Bottle Stock Inventory
- Multi-strength, multi-size bottle management
- Auto-integration with Reg-A (production data)
- E-Challan management for production fees
- Wastage/breakage tracking
- Issue on payment of duty

---

## 🗂️ **DATA STRUCTURE**

### **Master Tables**

#### 1. `regb_production_fees` (Financial Account)
```sql
- regb_fees_id (PK)
- date
- opening_balance (₹)
- deposit_amount (₹)
- echallan_no
- echallan_date
- total_credited (₹) [auto: opening + deposit]
- total_bottles_produced (from Reg-A)
- iml_bottles_qty (from Reg-A)
- fee_per_bottle (₹3.00)
- total_fees_debited (₹) [auto: bottles × fee]
- closing_balance (₹) [auto: credited - debited]
- remarks
- excise_officer_name
- excise_officer_signature
- status (draft/submitted)
- created_at
- updated_at
```

#### 2. `regb_bottle_stock` (Inventory Account)
```sql
- regb_stock_id (PK)
- date
- product_name (e.g., "Country Liquor 22.81%")
- strength (22.81%, etc.)
- bottle_size_ml (750, 375, 180, 90)
- opening_balance_bottles
- quantity_received_bottles (from Reg-A)
- total_accounted_bottles [auto: opening + received]
- wastage_breakage_bottles
- issue_on_duty_bottles (manual entry)
- closing_balance_bottles [auto: accounted - wastage - issue]
- opening_balance_bl
- opening_balance_al
- received_bl (from Reg-A)
- received_al (from Reg-A)
- total_bl
- total_al
- wastage_bl
- wastage_al
- issue_bl
- issue_al
- closing_bl
- closing_al
- status
- created_at
- updated_at
```

#### 3. `regb_daily_summary` (Consolidated View)
```sql
- regb_summary_id (PK)
- date
- total_opening_bottles (all sizes/strengths)
- total_received_bottles
- total_accounted_bottles
- total_wastage_bottles
- total_issued_bottles
- total_closing_bottles
- total_opening_bl
- total_opening_al
- total_received_bl
- total_received_al
- total_wastage_bl
- total_wastage_al
- total_issued_bl
- total_issued_al
- total_closing_bl
- total_closing_al
- production_fees_opening
- production_fees_deposit
- production_fees_credited
- production_fees_debited
- production_fees_closing
- status
- created_at
- updated_at
```

---

## 🔄 **DATA FLOW & AUTO-INTEGRATION**

### **From Reg-A (Production) → Reg-B (Issue)**

```
Reg-A Daily Production
├── Bottles Produced by Size/Strength
│   ├── 750ml @ 22.81% → 1,000 bottles
│   ├── 375ml @ 22.81% → 800 bottles
│   ├── 180ml @ 22.81% → 500 bottles
│   └── 90ml @ 22.81% → 500 bottles
│
├── BL/AL Calculations
│   ├── Each bottle size → BL content
│   └── BL × Strength → AL content
│
└── Production Fees
    └── Total Bottles × ₹3/- → Fees Debited
```

### **Auto-Fill Logic**

1. **Select Date** → Fetch Reg-A production for that date
2. **Auto-populate:**
   - Quantity Received of Bottles (from Reg-A)
   - IML Bottles Production Quantity (from Reg-A)
   - Bottles Production (from Reg-A)
   - Fee for Bottling Debited (bottles × ₹3)
   - Received BL/AL (from Reg-A calculations)

3. **Fetch Previous Day Closing:**
   - Opening Balance (₹) = Previous day closing balance
   - Opening Balance Bottles = Previous day closing bottles
   - Opening BL/AL = Previous day closing BL/AL

---

## 🎨 **UI/UX DESIGN**

### **Page Layout**

```
┌─────────────────────────────────────────────────────────────┐
│  🍾 REG-B - ISSUE OF COUNTRY LIQUOR IN BOTTLES             │
│  Register for Finished Goods & Production Fees              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  📅 DATE SELECTION & AUTO-FILL                              │
│  ┌──────────────┐  ┌────────────────────────────────────┐  │
│  │ Select Date  │  │ 🔄 Fetch Reg-A Production Data     │  │
│  └──────────────┘  └────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  💰 SECTION 1: PRODUCTION FEES ACCOUNT                      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Opening Balance (₹): [Auto from previous day]       │   │
│  │ Deposit Amount (₹): [Manual entry]                  │   │
│  │ E-Challan No: [Manual] | Date: [Manual]             │   │
│  │ Total Amount Credited: [Auto: opening + deposit]    │   │
│  │                                                      │   │
│  │ IML Bottles Qty: [Auto from Reg-A]                  │   │
│  │ Bottles Production: [Auto from Reg-A]               │   │
│  │ Fee per Bottle: ₹3.00                               │   │
│  │ Total Fees Debited: [Auto: bottles × ₹3]            │   │
│  │                                                      │   │
│  │ Closing Balance: [Auto: credited - debited]         │   │
│  │ Remarks: [Manual]                                   │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  📦 SECTION 2: BOTTLE STOCK INVENTORY                       │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │ Product: Country Liquor 22.81%                      │    │
│  │ Bottle Size: [750ml ▼] [375ml ▼] [180ml ▼] [90ml ▼]│    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  📊 STOCK MOVEMENT TABLE (Multi-Size View)                  │
│  ┌──────┬────────┬────────┬────────┬────────┬────────┐    │
│  │ Size │ Open.  │ Recv'd │ Total  │ Waste  │ Issue  │    │
│  │      │ Bal.   │        │ Acct.  │ Break  │ on Duty│    │
│  ├──────┼────────┼────────┼────────┼────────┼────────┤    │
│  │750ml │  500   │ 1,000  │ 1,500  │   10   │  800   │    │
│  │375ml │  300   │  800   │ 1,100  │    5   │  600   │    │
│  │180ml │  200   │  500   │  700   │    3   │  400   │    │
│  │90ml  │  100   │  500   │  600   │    2   │  300   │    │
│  └──────┴────────┴────────┴────────┴────────┴────────┘    │
│                                                              │
│  📊 BL/AL SUMMARY                                            │
│  ┌────────────────────────────────────────────────────┐    │
│  │ Total Opening: 1,100 bottles | 650.5 BL | 148.4 AL │    │
│  │ Total Received: 2,800 bottles | 2,108.5 BL | 480.9 AL│   │
│  │ Total Accounted: 3,900 bottles | 2,759.0 BL | 629.3 AL│  │
│  │ Total Wastage: 20 bottles | 15.0 BL | 3.4 AL        │    │
│  │ Total Issued: 2,100 bottles | 1,575.0 BL | 359.3 AL │    │
│  │ Total Closing: 1,780 bottles | 1,169.0 BL | 266.6 AL│    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  ✍️ VERIFICATION & SUBMISSION                               │
│  ┌────────────────────────────────────────────────────┐    │
│  │ Excise Officer: [Dropdown]                         │    │
│  │ Digital Signature: [Upload/Draw]                   │    │
│  │                                                     │    │
│  │ [💾 Save Draft] [✅ Submit Reg-B] [📄 Print PDF]   │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 **KEY FEATURES**

### **1. Smart Auto-Fill**
- ✅ Fetch Reg-A production data by date
- ✅ Auto-populate bottles received by size/strength
- ✅ Auto-calculate BL/AL for each bottle size
- ✅ Auto-calculate production fees (₹3 per bottle)
- ✅ Fetch previous day closing as today's opening

### **2. Multi-Size/Strength Management**
- ✅ Support 750ml, 375ml, 180ml, 90ml bottles
- ✅ Support multiple strengths (22.81%, etc.)
- ✅ Dynamic table for different product variants
- ✅ Individual tracking per size/strength combination

### **3. Production Fees Integration**
- ✅ Track production fees account balance
- ✅ E-Challan entry for deposits
- ✅ Auto-calculate fees debited (bottles × ₹3)
- ✅ Running balance (credited - debited)

### **4. Wastage/Breakage Tracking**
- ✅ Manual entry for wastage per bottle size
- ✅ Auto-calculate wastage BL/AL
- ✅ Deduct from closing balance

### **5. Issue on Payment of Duty**
- ✅ Manual entry for bottles issued
- ✅ Auto-calculate issue BL/AL
- ✅ Track what's sold/issued from warehouse

### **6. Validation & Checks**
- ✅ Closing balance must be ≥ 0
- ✅ Total accounted = opening + received
- ✅ Closing = accounted - wastage - issue
- ✅ Production fees balance must be sufficient
- ✅ E-Challan validation

### **7. Reports & Export**
- ✅ Daily summary report
- ✅ Stock movement report by size/strength
- ✅ Production fees ledger
- ✅ PDF export with officer signature

---

## 📊 **CALCULATIONS**

### **Bottle Content Calculations**

```python
# For each bottle size
bottle_bl = (bottle_size_ml / 1000) × quantity
bottle_al = bottle_bl × (strength / 100)

# Example: 750ml @ 22.81%
750ml bottle:
  BL = 0.750 L
  AL = 0.750 × 0.2281 = 0.171 L

1,000 bottles of 750ml @ 22.81%:
  Total BL = 1,000 × 0.750 = 750.0 BL
  Total AL = 1,000 × 0.171 = 171.0 AL
```

### **Production Fees Calculation**

```python
total_bottles_produced = sum(all bottle sizes from Reg-A)
fee_per_bottle = 3.00  # ₹3 per bottle
total_fees_debited = total_bottles_produced × fee_per_bottle

# Example:
2,800 bottles produced
Fees = 2,800 × ₹3 = ₹8,400
```

### **Balance Calculations**

```python
# Production Fees Account
total_credited = opening_balance + deposit_amount
closing_balance = total_credited - total_fees_debited

# Bottle Stock
total_accounted = opening_balance + quantity_received
closing_balance = total_accounted - wastage - issue_on_duty
```

---

## 🗄️ **DATABASE SCHEMA**

### **File Structure**
```
regb_schema.py          # Pydantic models & constants
regb_backend.py         # Business logic & database operations
regb.py                 # Streamlit frontend
regb_utils.py           # Helper functions (BL/AL calculations)
```

### **Key Constants**
```python
FEE_PER_BOTTLE = 3.00  # ₹3 per bottle
BOTTLE_SIZES = [750, 375, 180, 90]  # ml
STRENGTH_OPTIONS = [22.81, 25.0, 30.0]  # % v/v
```

---

## 🔄 **WORKFLOW**

### **Daily Entry Process**

1. **Select Date** → System checks if Reg-A exists for that date
2. **Auto-Fill Production Data:**
   - Fetch bottles produced from Reg-A
   - Calculate BL/AL for each size
   - Calculate production fees
3. **Fetch Previous Closing:**
   - Opening balance (₹) from previous Reg-B
   - Opening bottles from previous Reg-B
4. **Manual Entries:**
   - Deposit amount
   - E-Challan details
   - Wastage/breakage quantities
   - Issue on duty quantities
   - Remarks
5. **Auto-Calculate:**
   - Total credited
   - Total fees debited
   - Closing balance (₹)
   - Closing bottles
   - Closing BL/AL
6. **Verification:**
   - Select excise officer
   - Add signature
7. **Submit** → Lock the record

---

## 🎯 **INTEGRATION POINTS**

### **From Reg-A:**
- ✅ Bottles produced by size/strength
- ✅ IML bottles quantity
- ✅ BL/AL content per bottle type
- ✅ Production date

### **To Reg-78:**
- ✅ Issues on payment of duty (BL/AL)
- ✅ Bottle stock closing balance
- ✅ Production fees paid/pending

### **To Future Registers:**
- ✅ Issue details for sales tracking
- ✅ Wastage for reconciliation
- ✅ Stock levels for inventory management

---

## 📱 **RESPONSIVE DESIGN**

- ✅ Mobile-friendly tables
- ✅ Collapsible sections
- ✅ Touch-friendly inputs
- ✅ Swipeable multi-size views
- ✅ Quick summary cards

---

## 🔐 **SECURITY & AUDIT**

- ✅ User authentication
- ✅ Role-based access (entry vs. view)
- ✅ Audit trail (who, when, what)
- ✅ Digital signature verification
- ✅ E-Challan document upload
- ✅ Immutable records after submission

---

## 📈 **ANALYTICS & INSIGHTS**

- ✅ Daily production fees trend
- ✅ Wastage analysis by bottle size
- ✅ Issue patterns
- ✅ Stock turnover rate
- ✅ Fees collection efficiency

---

## ✅ **NEXT STEPS**

1. Create `regb_schema.py` with Pydantic models
2. Create `regb_backend.py` with database operations
3. Create `regb_utils.py` with calculation helpers
4. Create `regb.py` with Streamlit UI
5. Test integration with Reg-A
6. Test multi-size/strength scenarios
7. Add PDF export functionality
8. Add digital signature support

---

**Ready to build the most robust Reg-B system! 🚀**
