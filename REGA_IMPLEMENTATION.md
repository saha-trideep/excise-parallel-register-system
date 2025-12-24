# Reg-A Production Register - Implementation Guide

## 🍾 **Overview**

**Reg-A** is the Production Register that tracks the complete bottling process from **MFM2 (Production Mass Flow Meter)** readings to final bottle production, with strict **0.1% wastage limit** enforcement.

---

## 🔄 **Complete Spirit Flow**

```
┌──────────────────────────────────────────────────────────┐
│ TANKER ARRIVAL                                           │
│ ├─ MFM1 (Unloading Mass Flow Meter)                     │
│ └─ Reg-76: Spirit Receipt                               │
└──────────────────────────────────────────────────────────┘
                        ↓
┌──────────────────────────────────────────────────────────┐
│ STORAGE                                                  │
│ ├─ Reg-74: Unloading to SST (SST-5 to SST-10)          │
│ └─ Storage Wastage Verification                         │
└──────────────────────────────────────────────────────────┘
                        ↓
┌──────────────────────────────────────────────────────────┐
│ BLENDING/REDUCTION                                       │
│ ├─ Reg-74: Transfer SST → BRT (Batch Creation)         │
│ ├─ Reg-74: Reduction/Blending (Water Addition)         │
│ └─ Target Strength: 22.81% or 17.4% v/v                │
└──────────────────────────────────────────────────────────┘
                        ↓
┌──────────────────────────────────────────────────────────┐
│ PRODUCTION                                               │
│ ├─ MFM2 (Production Mass Flow Meter)                    │
│ ├─ Reg-A: Bottle Production                            │
│ ├─ Wastage Calculation (MFM2 vs Bottles)               │
│ └─ Allowable Limit: 0.1% of MFM2 AL                    │
└──────────────────────────────────────────────────────────┘
```

---

## 📊 **Key Features**

### **1. MFM2 Integration** ✅
- **MFM2 Start Reading**: Meter reading at production start
- **MFM2 End Reading**: Meter reading at production end
- **MFM2 Total**: End - Start (spirit passed through meter)
- **MFM2 AL**: MFM2 BL × Strength / 100

### **2. Bottle-Centric Entry** ✅
- Enter **bottle counts** (not cases)
- Support for **4 bottle sizes**: 180ml, 375ml, 750ml, 1000ml
- **Auto-calculation** of BL and AL from bottles
- **Real-time efficiency** tracking

### **3. Production Wastage (0.1% Limit)** ✅
- **Formula**: (MFM2 AL - Bottles AL) / MFM2 AL × 100
- **Allowable Limit**: 0.1% of MFM2 AL
- **Critical Threshold**: 1.0% triggers alert
- **Mandatory Explanation**: If exceeds 0.1%

### **4. Batch Tracking** ✅
- Links to **Reg-74 batches**
- **Multi-session support**: Same batch, multiple production days
- **Session numbering**: Auto-incremented (Session-1, Session-2, etc.)
- **Batch completion tracking**: Flags when BRT is empty

### **5. BRT Integration** ✅
- **Auto-fetch** BRT stock from Reg-74
- **Real-time validation**: MFM2 reading ≤ Available stock
- **Closing balance calculation**: Opening - MFM2 reading
- **Remaining stock display**: For next session

---

## 🎯 **Workflow Example**

### **Scenario: Production Session**

**Step 1: Select Batch**
```
Batch: BATCH-001
Source BRT: BRT-11
Available Stock: 2,108.5 BL / 480.95 AL @ 22.81% v/v
Reg-74 ID: R74-2025120001
```

**Step 2: MFM2 Readings**
```
MFM2 Start Reading: 10,000.000 L
MFM2 End Reading: 12,108.500 L
MFM2 Total BL: 2,108.500 L (auto-calculated)
MFM2 Total AL: 480.950 L (auto-calculated: 2108.5 × 22.81 / 100)
Temperature: 20.0°C
Density: 0.9652 gm/cc
```

**Step 3: Bottle Production**
```
750ml Bottles: 2,800 bottles
Total Bottles: 2,800
Total BL: 2,100.000 L (2800 × 0.750)
Total AL: 479.010 L (2100.0 × 22.81 / 100)
```

**Step 4: Wastage Analysis**
```
MFM2 AL: 480.950 L
Bottles AL: 479.010 L
Wastage AL: 1.940 L
Wastage %: 0.403% (1.940 / 480.950 × 100)
Allowable Limit: 0.1%
Status: ❌ EXCEEDS LIMIT
```

**Step 5: Wastage Explanation (Required)**
```
"Line spillage during bottle changeover. 
Approximately 1.9L lost during cleaning and setup. 
All spillage documented and cleaned as per SOP."
```

**Step 6: Dispatch**
```
Dispatch Type: Warehouse Storage
Location: Warehouse-A, Section-3
Challan No: CH-2025-001
Dispatch Date: 2025-12-24
```

**Step 7: Approval**
```
Production Officer: John Doe (Signed: 2025-12-24)
Excise Officer: Jane Smith (Signed: 2025-12-24)
Status: Approved
```

**Result:**
```
✅ Production Record Saved: RA-2025120001
📊 Remaining in BRT-11: 8.500 BL / 1.940 AL
🎯 Batch BATCH-001 can continue in next session
```

---

## 📋 **Wastage Calculation Details**

### **Formula Breakdown:**

```python
# Step 1: MFM2 AL Calculation
mfm2_al = mfm2_bl × (strength / 100)
# Example: 2108.5 × (22.81 / 100) = 480.95 AL

# Step 2: Bottles AL Calculation
bottles_bl = (bottles_180ml × 0.180) + 
             (bottles_375ml × 0.375) + 
             (bottles_750ml × 0.750) + 
             (bottles_1000ml × 1.000)
bottles_al = bottles_bl × (strength / 100)
# Example: 2100.0 × (22.81 / 100) = 479.01 AL

# Step 3: Wastage Calculation
wastage_bl = mfm2_bl - bottles_bl
wastage_al = mfm2_al - bottles_al
wastage_percentage = (wastage_al / mfm2_al) × 100
# Example: (1.94 / 480.95) × 100 = 0.403%

# Step 4: Validation
if wastage_percentage <= 0.1:
    status = "✅ Within Allowable Limit"
elif wastage_percentage <= 1.0:
    status = "⚠️ Exceeds Limit - Explanation Required"
else:
    status = "🚨 CRITICAL - Immediate Investigation Required"
```

---

## ⚠️ **Validation Rules**

### **1. Batch Validation**
```python
✅ Batch must exist in Reg-74
✅ Batch must have available stock in BRT
✅ BRT closing balance must be > 0
```

### **2. MFM2 Validation**
```python
✅ MFM2 End > MFM2 Start
✅ MFM2 Total BL > 0
✅ MFM2 Total BL ≤ BRT Available Stock
```

### **3. Bottle Validation**
```python
✅ At least one bottle size must have count > 0
✅ Total bottles > 0
✅ Bottles BL ≤ MFM2 BL (cannot bottle more than passed through meter)
```

### **4. Wastage Validation**
```python
✅ If wastage % > 0.1%, explanation is MANDATORY
✅ If wastage % > 1.0%, CRITICAL alert triggered
✅ Negative wastage = ERROR (bottles > MFM2 impossible)
```

### **5. Officer Validation**
```python
✅ Production Officer name is MANDATORY
✅ Excise Officer name is OPTIONAL
✅ Approval date must be ≥ Production date
```

---

## 🎨 **Visual Wastage Display**

### **Within Limit (≤ 0.1%)**
```
┌────────────────────────────────────────────┐
│ ✅ WASTAGE WITHIN ALLOWABLE LIMIT          │
├────────────────────────────────────────────┤
│ Wastage of 0.062% is within allowable     │
│ limit of 0.1%                              │
│ Production efficiency: 99.94%              │
└────────────────────────────────────────────┘
```

### **Exceeds Limit (0.1% - 1.0%)**
```
┌────────────────────────────────────────────┐
│ ⚠️ WASTAGE EXCEEDS ALLOWABLE LIMIT        │
├────────────────────────────────────────────┤
│ Wastage of 0.403% exceeds allowable       │
│ limit of 0.1%                              │
│ Explanation required for excise compliance │
│ Wastage: 1.94 AL out of 480.95 AL         │
└────────────────────────────────────────────┘
```

### **Critical (> 1.0%)**
```
┌────────────────────────────────────────────┐
│ 🚨 CRITICAL WASTAGE ALERT                 │
├────────────────────────────────────────────┤
│ Wastage of 1.25% exceeds critical         │
│ threshold (1.0%)!                          │
│ IMMEDIATE INVESTIGATION REQUIRED!          │
│ Allowable limit: 0.1% of MFM2 AL          │
└────────────────────────────────────────────┘
```

---

## 📊 **Multi-Session Production**

### **Scenario: Large Batch Over Multiple Days**

**Day 1: Session-1**
```
Batch: BATCH-001
BRT-11 Opening: 5,000 BL / 1,140.5 AL @ 22.81%
MFM2 Reading: 2,108.5 BL / 480.95 AL
Bottles Produced: 2,800 × 750ml
BRT-11 Closing: 2,891.5 BL / 659.55 AL
Status: Batch Incomplete
```

**Day 2: Session-2**
```
Batch: BATCH-001 (same batch)
Session: Session-2 (auto-incremented)
BRT-11 Opening: 2,891.5 BL / 659.55 AL @ 22.81%
MFM2 Reading: 2,891.5 BL / 659.55 AL
Bottles Produced: 3,855 × 750ml
BRT-11 Closing: 0.0 BL / 0.0 AL
Status: ✅ Batch Complete
```

---

## 🔍 **Key Differences: Storage vs Production Wastage**

| Aspect | Storage Wastage (Reg-74) | Production Wastage (Reg-A) |
|--------|--------------------------|----------------------------|
| **Measurement** | Expected vs Actual (Dip) | MFM2 vs Bottles |
| **Allowable Limit** | 0.3% | 0.1% |
| **Calculation** | (Expected AL - Actual AL) / Expected AL × 100 | (MFM2 AL - Bottles AL) / MFM2 AL × 100 |
| **When Checked** | Before operation starts | After production completes |
| **Excise Rule** | "No allowable wastage" (but 0.3% tolerance) | 0.1% allowable for production |
| **Note Required** | If wastage > 0.1L | If wastage > 0.1% |

---

## 📁 **Files Created**

1. **`rega_schema.py`** - Schema with 80+ columns
2. **`rega_backend.py`** - Backend with MFM2 calculations
3. **`rega.py`** - Ultra-compact production form

---

## 🚀 **How to Run**

```bash
python -m streamlit run rega.py
```

**Access URLs:**
- Local: http://localhost:8502
- Network: http://192.168.0.115:8502

---

## ✅ **Summary**

**Reg-A Production Register** provides:

✅ **MFM2 Integration** - Production mass flow meter tracking  
✅ **Bottle-Centric Entry** - Focus on bottles, not cases  
✅ **0.1% Wastage Limit** - Strict excise compliance  
✅ **Batch Tracking** - Links to Reg-74 batches  
✅ **Multi-Session Support** - Same batch, multiple days  
✅ **Real-time Validation** - Prevents errors before submission  
✅ **Automatic Calculations** - BL, AL, wastage, efficiency  
✅ **BRT Integration** - Auto-fetch stock from Reg-74  
✅ **Complete Audit Trail** - All data synced to Google Sheets  

**Built like a genius!** 🎯🍾
