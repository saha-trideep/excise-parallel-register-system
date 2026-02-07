# 🐛 BUG REPORT & CORRECTION REQUIREMENTS
## Excise Parallel Register System - Reg-76 to Reg-78 to Handbook Flow

**Date**: February 7, 2026  
**Reported By**: Junior Developer Testing Team  
**Priority**: HIGH  
**Affected Modules**: Reg-76 (5_Reg_76.py), Reg-78 (6_Reg_78.py), Handbook Generator (handbook_generator.py)

---

## 🚨 CRITICAL ISSUES FOUND

### **ISSUE #1: Missing Required Fields in Reg-76**
**Severity**: HIGH  
**Status**: ❌ BLOCKING

#### Missing Fields:
1. **"Weight of Empty Drum/Tanker"** (in kg)
   - **Excel Location**: Row 15 in REG 76 sheet
   - **Required For**: Net weight verification and regulatory compliance
   - **Recommended Location**: Section 4 (Weigh Bridge Data)
   - **Field Type**: Number input, step=0.1, format="%.1f"
   - **Database Field**: `empty_tanker_weight_kg`

2. **"Date of Dispatch"** 
   - **Excel Location**: Implied in transit calculation section
   - **Required For**: Accurate transit days calculation
   - **Current Issue**: Code references `date_dispatch` but field may not exist properly
   - **Recommended Location**: Section 2 (Date & Movement) - FIRST field before Date of Arrival
   - **Field Type**: Date input
   - **Database Field**: `date_dispatch`
   - **Impact**: Transit days calculation is currently incorrect

3. **"Indication"**
   - **Excel Location**: Row 23, Column E (in Advised Quantity section)
   - **Required For**: Qualitative observations during measurement (e.g., "Clear", "Cloudy", "Sediment present")
   - **Recommended Location**: Section 3 (Advised Quantity) - after Strength field
   - **Field Type**: Text input or Selectbox with options: ["Clear", "Cloudy", "Sediment", "Normal", "Other"]
   - **Database Field**: `indication`

#### **Code Changes Required**:

**File**: `pages/5_Reg_76.py`

**Location 1** - Add Empty Tanker Weight in Section 4:
```python
# SECTION 4: WEIGH BRIDGE
st.markdown('<div class="section-container">', unsafe_allow_html=True)
st.markdown('<div class="section-header">SECTION 4 – WEIGH BRIDGE DATA</div>', unsafe_allow_html=True)

# ADD THIS FIELD FIRST
empty_tanker_weight = st.number_input(
    "Weight of Empty Drum/Tanker (kg)*", 
    min_value=0.0, 
    step=0.1, 
    format="%.1f",
    help="Standard empty weight of the tanker"
)

w1, w2 = st.columns(2)
# ... rest of weigh bridge section
```

**Location 2** - Fix Date of Dispatch in Section 2:
```python
# SECTION 2: DATE & MOVEMENT
st.markdown('<div class="section-container">', unsafe_allow_html=True)
st.markdown('<div class="section-header">SECTION 2 – DATE & MOVEMENT</div>', unsafe_allow_html=True)
c4, c5, c6 = st.columns(3)
with c4:
    # MAKE SURE THIS EXISTS AND IS PROPERLY NAMED
    date_dispatch = st.date_input("Date of Dispatch*", key="dispatch_date")
with c5:
    date_arrival = st.date_input("Date of Arrival")
with c6:
    date_receipt = st.date_input("Date of Receipt & Examination")
```

**Location 3** - Add Indication in Section 3:
```python
# SECTION 3: ADVISED QUANTITY
with c9:
    adv_s = st.number_input("Strength (% v/v)", min_value=0.0, max_value=100.0, step=0.01)
    # ADD THIS FIELD AFTER STRENGTH
    indication = st.selectbox(
        "Indication*",
        ["Clear", "Cloudy", "Sediment Present", "Normal", "Other"],
        help="Visual observation of spirit quality"
    )
    if indication == "Other":
        indication_other = st.text_input("Specify Indication")
        indication = indication_other if indication_other else "Other"
```

**Location 4** - Update payload in submission:
```python
payload = {
    # ... existing fields ...
    "empty_tanker_weight_kg": empty_tanker_weight,  # ADD THIS
    "indication": indication,  # ADD THIS
    # ... rest of fields ...
}
```

---

### **ISSUE #2: BL at 20°C Should Be Manual Entry Field**
**Severity**: MEDIUM  
**Status**: ❌ INCORRECT IMPLEMENTATION

#### Current Problem:
```python
# Current code (WRONG):
adv_bl_20c = adv_bl  # Just copies the value without temperature correction
```

#### What Should Happen:
The operator needs to **MANUALLY ENTER** the "BL at 20°C" value as measured, NOT auto-calculate it.

#### **Code Changes Required**:

**File**: `pages/5_Reg_76.py`

**Section 3 - Advised Quantity**:
```python
c7, c8, c9, c10 = st.columns(4)
with c7:
    adv_w = st.number_input("Weight in Advice (kg)", min_value=0.0, step=0.001, format="%.3f")
with c8:
    adv_d = st.number_input("Avg Density (gm/cc)", min_value=0.0, step=0.0001, format="%.4f")
with c9:
    adv_s = st.number_input("Strength (% v/v)", min_value=0.0, max_value=100.0, step=0.01)
with c10:
    adv_t = st.number_input("Temperature (°C)", value=20.0, step=0.1)

# Calculate BL at given temperature
adv_bl = calculate_bl(adv_w, adv_d)
adv_al = calculate_al(adv_bl, adv_s)

# ADD MANUAL ENTRY FIELD FOR BL AT 20°C
col_bl20_adv, col_al_result = st.columns(2)
with col_bl20_adv:
    adv_bl_20c = st.number_input(
        "Volume in BL at 20°C (Manual Entry)*", 
        min_value=0.0, 
        step=0.01,
        format="%.2f",
        help="Enter the BL value corrected to 20°C as per measurement"
    )

m1, m2, m3 = st.columns(3)
with m1: display_calc_result("Advised BL", adv_bl, "L")
with m2: display_calc_result("Advised AL", adv_al, "L")
with m3: display_calc_result("Advised BL at 20°C", adv_bl_20c, "L")  # Now shows manual entry
```

**Section 5 - Received Quantity**:
```python
# ADD SIMILAR MANUAL ENTRY FOR RECEIVED BL AT 20°C
r1, r2, r3 = st.columns(3)
with r1:
    rec_m = st.number_input("Mass received (kg) - MFM", step=0.001, format="%.3f")
    rec_t = st.number_input("Avg Unloading Temp", value=20.0, step=0.1)
with r2:
    rec_d_t = st.number_input("Density @ Temp", step=0.0001, format="%.4f")
    rec_d_20 = st.number_input("Density @ 20°C", step=0.0001, format="%.4f")
with r3:
    rec_s = st.number_input("Strength % v/v (MFM)", step=0.01)
    
rec_bl = calculate_bl(rec_m, rec_d_t)
rec_al = calculate_al(rec_bl, rec_s)

# ADD MANUAL ENTRY FIELD FOR RECEIVED BL AT 20°C
rec_bl_20c = st.number_input(
    "Volume in BL at 20°C (Manual Entry)*", 
    min_value=0.0, 
    step=0.01,
    format="%.2f",
    help="Enter the BL value corrected to 20°C as per MFM reading",
    key="rec_bl_20c"
)

m4, m5, m6 = st.columns(3)
with m4: display_calc_result("Received BL", rec_bl, "L")
with m5: display_calc_result("Received AL", rec_al, "L")
with m6: display_calc_result("Received BL at 20°C", rec_bl_20c, "L")  # Shows manual entry
```

**Update payload**:
```python
payload = {
    # ... existing fields ...
    "adv_bl_20c": adv_bl_20c,  # Now manual entry
    "rec_bl_20c": rec_bl_20c,  # ADD THIS - manual entry for received
    # ... rest of fields ...
}
```

---

### **ISSUE #3: CRITICAL - Handbook SST/BRT Vat Update Logic is WRONG**
**Severity**: CRITICAL 🚨  
**Status**: ❌ SYSTEM LOGIC ERROR

#### Current Understanding (INCORRECT):
```
Reg-76 rec_al → Reg-78 Column 4 → Handbook "Received (A.L.)" (generic)
```

#### What SHOULD Happen:
```
Reg-76 Entry:
├─ rec_al: 28,725.77 AL
├─ storage_vat_no: "SST-5"
└─ date: 2025-11-14

↓↓↓ MUST UPDATE ↓↓↓

Handbook "SST & BRT Detail" Section:
├─ Row for "SST-5"
│   └─ Column "Received (A.L.)" = 28,725.77
├─ Row for "SST-6" 
│   └─ Column "Received (A.L.)" = 0 (no receipt)
└─ ... (SST-7 to BRT-17)
```

#### The Problem:
When a tanker unloads into **SST-5**, the Handbook should show:
- ✅ SST-5: Received (A.L.) = 28,725.77
- ❌ NOT just a generic "total received" column

Each SST/BRT vat (SST-5, SST-6, SST-7, SST-8, SST-9, SST-10, BRT-11, BRT-12, BRT-13, BRT-14, BRT-15, BRT-16, BRT-17) has its own row in the Handbook, and the "Received (A.L.)" column should show ONLY what was received into THAT SPECIFIC VAT.

#### **Code Changes Required**:

**File**: `handbook_generator.py`

**Current Logic** (needs verification and likely correction):
```python
def fetch_reg76_data(self):
    """Fetch Reg-76 receipts for the handbook date"""
    query = """
        SELECT * FROM reg76_data 
        WHERE date(receipt_date) = date(?)
        ORDER BY receipt_date DESC
    """
    # This likely returns all receipts but doesn't properly aggregate by vat
```

**CORRECT Logic Should Be**:
```python
def fetch_reg76_data_by_vat(self):
    """
    Fetch Reg-76 receipts grouped by storage vat for the handbook date.
    Returns a dictionary: {vat_no: total_received_al}
    """
    query = """
        SELECT 
            storage_vat_no,
            SUM(rec_al) as total_received_al
        FROM reg76_data 
        WHERE date(date_receipt) = date(?)
        GROUP BY storage_vat_no
    """
    conn = self.get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, (self.handbook_date,))
    results = cursor.fetchall()
    conn.close()
    
    # Convert to dictionary for easy lookup
    vat_receipts = {}
    for row in results:
        vat_no = row[0]  # e.g., "SST-5"
        received_al = row[1]
        vat_receipts[vat_no] = received_al
    
    return vat_receipts

def create_sst_brt_section(self):
    """Create SST & BRT Detail table with per-vat received amounts"""
    # Get receipts grouped by vat
    vat_receipts = self.fetch_reg76_data_by_vat()
    
    # Get stock levels from Reg-74
    stock_data = self.fetch_reg74_data()
    
    # Create table with ALL vats (SST-5 to BRT-17)
    all_vats = [f"SST-{i}" for i in range(5, 11)] + [f"BRT-{i}" for i in range(11, 18)]
    
    for vat_no in all_vats:
        # Get received amount for THIS SPECIFIC VAT (0 if no receipt)
        received_al = vat_receipts.get(vat_no, 0.0)
        
        # Get stock data for this vat
        stock = stock_data.get(vat_no, {})
        dip = stock.get('dip_cm', 0.0)
        bl = stock.get('bl', 0.0)
        strength = stock.get('strength', 0.0)
        al = stock.get('al', 0.0)
        
        # Add row to table
        table_data.append([
            vat_no,           # Vats column
            dip,              # Dip (cm)
            bl,               # B.L.
            strength,         # %v/v
            al,               # A.L.
            received_al       # Received (A.L.) - SPECIFIC TO THIS VAT
        ])
```

#### Example Output in Handbook:
```
SST & BRT Detail (Date: 14.11.2025)
┌──────────┬────────┬──────────┬───────┬──────────┬────────────────┐
│ Vats     │ Dip(cm)│   B.L.   │ %v/v  │   A.L.   │ Received (A.L.)│
├──────────┼────────┼──────────┼───────┼──────────┼────────────────┤
│ SST-5    │  145.2 │ 12500.00 │  96.1 │ 12012.50 │   28725.77    │ ← Receipt went here
│ SST-6    │  120.5 │  9800.50 │  96.1 │  9416.08 │       0.00    │ ← No receipt
│ SST-7    │   98.3 │  7200.00 │  96.1 │  6919.20 │       0.00    │
│ SST-8    │  210.8 │ 18500.00 │  96.1 │ 17778.50 │       0.00    │
│ SST-9    │  156.4 │ 13200.00 │  96.1 │ 12685.20 │       0.00    │
│ SST-10   │  189.7 │ 16100.00 │  96.1 │ 15472.10 │       0.00    │
├──────────┼────────┼──────────┼───────┼──────────┼────────────────┤
│ BRT-11   │  134.5 │  2108.50 │  22.8 │   480.95 │       0.00    │
│ BRT-12   │  112.8 │  1850.00 │  22.8 │   421.80 │       0.00    │
│ ...      │   ...  │    ...   │  ...  │    ...   │      ...      │
└──────────┴────────┴──────────┴───────┴──────────┴────────────────┘
Total SST:                              │ 74283.58 │   28725.77    │
Total BRT:                              │  5840.25 │       0.00    │
Grand Total:                            │ 80123.83 │   28725.77    │
```

---

## 🔄 CORRECT DATA FLOW DIAGRAM

```
┌────────────────────────────────────────────────────────────────┐
│                    REG-76 ENTRY                                │
├────────────────────────────────────────────────────────────────┤
│  Permit No: tBSUB/2025-26/00032298/P                          │
│  Received AL: 28,725.77                                        │
│  Storage Vat: SST-5  ◄─────────────┐                          │
│  Date: 14.11.2025                  │                           │
└────────────────────────────────────┼───────────────────────────┘
                                     │
                    STORES VAT INFO  │
                                     │
         ┌───────────────────────────┴───────────────────────┐
         │                                                    │
         ▼                                                    ▼
┌─────────────────────┐                          ┌─────────────────────┐
│      REG-78         │                          │   HANDBOOK PDF      │
├─────────────────────┤                          ├─────────────────────┤
│ Column 4:           │                          │ SST & BRT Detail:   │
│ "Quantity received  │                          │                     │
│  through MFM-I"     │                          │ SST-5 Row:          │
│ = 28,725.77 AL      │                          │ ├─ Dip: (from 74)   │
│                     │                          │ ├─ B.L.: (from 74)  │
│ (Daily Total)       │                          │ ├─ %v/v: (from 74)  │
│                     │                          │ ├─ A.L.: (from 74)  │
│                     │                          │ └─ Received (A.L.): │
│                     │                          │    28,725.77 ◄──────┤
│                     │                          │                     │
│                     │                          │ SST-6 Row:          │
│                     │                          │ └─ Received: 0.00   │
│                     │                          │                     │
│                     │                          │ SST-7 Row:          │
│                     │                          │ └─ Received: 0.00   │
└─────────────────────┘                          └─────────────────────┘
```

---

## 📝 SUMMARY OF REQUIRED CHANGES

### **File: `pages/5_Reg_76.py`**
- [ ] Add field: `empty_tanker_weight_kg` (Section 4)
- [ ] Verify/Fix: `date_dispatch` field (Section 2)
- [ ] Add field: `indication` (Section 3)
- [ ] Change: `adv_bl_20c` from auto-calc to manual input
- [ ] Add field: `rec_bl_20c` as manual input (Section 5)
- [ ] Update: payload to include all new fields

### **File: `handbook_generator.py`**
- [ ] Modify: `fetch_reg76_data()` to return vat-grouped dictionary
- [ ] Fix: `create_sst_brt_section()` to show per-vat received amounts
- [ ] Ensure: Each vat row shows its specific received AL, not total

### **File: `reg76_backend.py` or `reg76_schema.py`**
- [ ] Add database columns: `empty_tanker_weight_kg`, `indication`, `rec_bl_20c`
- [ ] Update: Schema validation for new fields

---

## ⚠️ TESTING REQUIREMENTS

After implementing fixes, verify:

1. **Reg-76 Form**:
   - [ ] All 5 new/fixed fields are visible
   - [ ] BL at 20°C accepts manual input
   - [ ] Form validation works for mandatory fields
   - [ ] Data saves to database correctly

2. **Reg-78 Auto-Update**:
   - [ ] Column 4 updates when Reg-76 entry is added
   - [ ] Daily total matches sum of all receipts

3. **Handbook Generation**:
   - [ ] Generate handbook for date with receipt into SST-5
   - [ ] Verify SST-5 row shows received AL
   - [ ] Verify other vats show 0.00 in received column
   - [ ] Total received matches Reg-76 sum for the day

---

## 📋 PRIORITY ORDER

1. 🔴 **CRITICAL** - Fix Handbook vat-specific received amounts (Issue #3)
2. 🟠 **HIGH** - Add missing required fields (Issue #1)
3. 🟡 **MEDIUM** - Change BL at 20°C to manual entry (Issue #2)

---

**Developer**: Please confirm you understand these requirements before implementing changes.
