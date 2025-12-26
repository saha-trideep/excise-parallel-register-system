# Streamlit Excise Register System - Developer Handoff Guide

## 📋 For: SIP2LIFE Data Management Project Developer
## 📅 Date: December 26, 2025
## 🎯 Purpose: Implement Register Engine functionality based on working Streamlit prototype

---

## 🌟 Executive Summary

This Streamlit project is a **fully functional prototype** of an Excise Register Management System for SIP2LIFE Distilleries. It demonstrates the complete workflow, calculations, and data management for three critical excise registers:

- **Reg-76**: Spirit Receipt Register
- **Reg-74**: Vat Operations Register  
- **Reg-A**: Production & Bottling Register

**Your task**: Implement similar functionality in the SIP2LIFE React/Node.js application's Register Engine section.

---

## 🏗️ Current Streamlit Project Architecture

### **Tech Stack:**
```
Frontend: Streamlit (Python)
Backend: Python modules
Database: SQLite + CSV files
Cloud Sync: Google Sheets (via gspread)
Authentication: Simple password-based
Deployment: Streamlit Cloud
```

### **Project Structure:**
```
excise-parallel-register-system/
├── Home.py                          # Main entry point
├── auth.py                          # Authentication module
├── pages/
│   ├── 1_Reg_B.py                   # Reg-B Register (Bond Register)
│   ├── 2_Excise_Duty.py             # Excise Duty Calculator
│   ├── 3_Reg_A.py                   # Production Register
│   ├── 4_Reg_74.py                  # Vat Operations
│   ├── 5_Reg_76.py                  # Spirit Receipt
│   ├── 6_Reg_78.py                  # Dispatch Register
│   └── 6_Daily_Handbook.py          # Daily Reports
├── Backend Modules:
│   ├── reg76_backend.py             # Reg-76 CRUD operations
│   ├── reg74_backend.py             # Reg-74 operations
│   ├── rega_backend.py              # Reg-A operations
│   ├── regb_backend.py              # Reg-B operations
│   └── reg78_backend.py             # Reg-78 operations
├── Schema Definitions:
│   ├── schema.py                    # Reg-76 columns
│   ├── reg74_schema.py              # Reg-74 schema
│   ├── rega_schema.py               # Reg-A schema
│   └── regb_schema.py               # Reg-B schema
├── Utilities:
│   ├── utils.py                     # Calculation functions
│   ├── pdf_generator.py             # PDF generation
│   └── handbook_generator.py        # Daily handbook
└── Data Storage:
    ├── excise_registers.db          # SQLite database
    ├── reg76_data.csv               # Reg-76 CSV backup
    └── Google Sheets sync           # Cloud backup
```

---

## 📊 Register-by-Register Implementation Guide

### **1. REG-76: Spirit Receipt Register**

#### **Purpose:**
Track incoming spirit shipments from other distilleries, calculate transit wastage, and record storage vat allocation.

#### **Key Features Implemented:**

**A. Data Entry Form:**
- 8 sections with 50+ fields
- Real-time calculations
- Validation for mandatory fields
- Auto-ID generation (R76-YYYYMM###)

**B. Calculations:**
```python
# Bulk Liters (BL) = Mass (kg) / Density (gm/cc)
BL = mass_kg / density

# Absolute Liters (AL) = BL × (Strength % / 100)
AL = BL * (strength / 100)

# Transit Wastage = Advised AL - Received AL
transit_wastage = advised_al - received_al

# Chargeable Wastage = max(0, wastage - allowable)
chargeable_wastage = max(0, wastage - allowable_wastage)
```

**C. Database Schema:**
```python
COLUMNS = [
    "reg76_id",              # Primary key
    "permit_no",             # Import permit number
    "distillery",            # Source distillery
    "spirit_nature",         # ENA, GENA, RS, Ethanol
    "vehicle_no",            # Tanker registration
    "invoice_no",            # Invoice number
    "invoice_date",          # Invoice date
    "date_dispatch",         # Dispatch date
    "date_arrival",          # Arrival date
    "date_receipt",          # Receipt & examination date
    "days_in_transit",       # Auto-calculated
    
    # Advised Quantity (as per pass)
    "adv_weight_kg",         # Weight in kg
    "adv_avg_density",       # Density gm/cc
    "adv_strength",          # Strength % v/v
    "adv_temp",              # Temperature °C
    "adv_bl",                # Calculated BL
    "adv_al",                # Calculated AL
    "adv_bl_20c",            # BL at 20°C
    
    # Weigh Bridge Data
    "wb_laden_consignee",    # Laden weight at consignee
    "wb_unladen_consignee",  # Unladen weight
    "wb_laden_pass",         # Laden weight as per pass
    "wb_unladen_pass",       # Unladen as per pass
    
    # Received Quantity (MFM-1)
    "rec_mass_kg",           # Mass received
    "rec_unload_temp",       # Unloading temperature
    "rec_density_at_temp",   # Density at temp
    "rec_density_20c",       # Density at 20°C
    "rec_strength",          # Strength measured
    "rec_bl",                # Calculated BL
    "rec_al",                # Calculated AL
    
    # Wastage/Increase
    "diff_advised_al",       # Difference
    "transit_wastage_al",    # Wastage in AL
    "transit_increase_al",   # Increase in AL
    "allowable_wastage_al",  # Allowable limit
    "chargeable_wastage_al", # Chargeable amount
    
    # Storage & Remarks
    "storage_vat_no",        # SST-5 to SST-10
    "evc_generated_date",    # EVC date
    "excise_remarks",        # Official remarks
    "status",                # Submitted/Verified
    "created_at"             # Timestamp
]
```

**D. CRUD Operations:**
```python
# Create
def save_record(data_dict):
    # Generate ID
    # Validate data
    # Save to CSV
    # Sync to Google Sheets
    # Return ID

# Read
def get_data():
    # Load from CSV
    # Filter empty rows
    # Return DataFrame

# Update (not implemented yet)

# Delete
def delete_record(reg76_id):
    # Remove from CSV
    # Sync to Google Sheets
    # Return success/failure

# Filter
def filter_records(date_from=None, tanker_no=None):
    # Apply filters
    # Return filtered DataFrame
```

**E. UI Components:**
- Tab 1: Secure Data Entry (8 sections)
- Tab 2: Administrative View (table + filters + delete)
- Export to CSV
- Generate PDF
- Sync with Google Sheets

**F. What You Need to Implement in SIP2LIFE:**

1. **Create Reg76Entry API endpoints:**
   ```javascript
   POST   /api/registers/reg76          // Create entry
   GET    /api/registers/reg76          // List all
   GET    /api/registers/reg76/:id      // Get one
   PUT    /api/registers/reg76/:id      // Update
   DELETE /api/registers/reg76/:id      // Delete
   GET    /api/registers/reg76/filter   // Filter by date/vehicle
   ```

2. **Frontend Form (React):**
   - Multi-step form or accordion sections
   - Real-time calculation of BL, AL, wastage
   - Validation before submit
   - Auto-save drafts

3. **Database:**
   - Use existing `Reg76Entry` model from Prisma schema
   - Add indexes on `receiptDate`, `permitNo`, `vehicleNo`
   - Add audit logging

4. **Calculations:**
   - Create utility functions for BL/AL calculations
   - Implement wastage calculation logic
   - Temperature correction formulas

---

### **2. REG-74: Vat Operations Register**

#### **Purpose:**
Track all operations on Spirit Storage Tanks (SST) and Blending/Reduction Tanks (BRT), including receipts, transfers, water addition, and production.

#### **Key Features Implemented:**

**A. Event-Based System:**
```python
# Event Types:
OPENING          # Daily opening stock
UNLOADING        # Receipt from Reg-76
INTERNAL_TRANSFER # SST → BRT transfer
WATER_ADDITION   # Water for reduction
BLENDING         # Spirit blending
PRODUCTION       # Bottling production
ADJUSTMENT       # Stock adjustments
CLOSING          # Daily closing stock
```

**B. Database Schema:**
```python
# Vat Master
vat_id, vat_code, vat_type, capacity_bl, status

# Reg-74 Events
event_id, vat_id, event_datetime, event_type,
opening_data (JSON), receipt_data (JSON),
issue_data (JSON), adjustment_data (JSON),
production_data (JSON), closing_data (JSON),
batch_id, remarks, created_by, created_at
```

**C. JSON Data Blocks:**
```python
# Opening Data (Cols 1-7)
{
    "dip_cm": 150.5,
    "temp": 20.0,
    "alc_ind": 0.9650,
    "strength": 96.5,
    "volume_bl": 12000.0,
    "volume_al": 11580.0
}

# Receipt Data (Cols 8-11)
{
    "source": "R76-202512001",
    "qty_bl": 5000.0,
    "strength": 96.5,
    "qty_al": 4825.0
}

# Production Data (Cols 25-33)
{
    "rlt_bl": 3000.0,
    "strength": 42.8,
    "rlt_al": 1284.0,
    "vat_count": 2,
    "mfm_bl": 2995.0,
    "density": 0.9234,
    "mfm_strength": 42.8,
    "mfm_al": 1281.86,
    "dead_stock_al": 2.14,
    "batch_session_suffix": "Batch-1"
}
```

**D. Dashboard Features:**
- Vat status overview (IDLE, IN_USE, PRODUCTION)
- Daily operations log
- Stock reconciliation
- Wastage tracking (0.3% threshold for storage)

**E. What You Need to Implement in SIP2LIFE:**

1. **Use existing `Reg74Event` model** - Already perfect!

2. **Create API endpoints:**
   ```javascript
   POST   /api/registers/reg74/events           // Create event
   GET    /api/registers/reg74/events           // List events
   GET    /api/registers/reg74/vats/:vatId      // Vat history
   GET    /api/registers/reg74/dashboard        // Dashboard data
   POST   /api/registers/reg74/reconcile        // Daily reconciliation
   ```

3. **Frontend Components:**
   - Vat selection dropdown
   - Event type selector
   - Dynamic form based on event type
   - Real-time stock calculation
   - Dashboard with vat status cards

4. **Business Logic:**
   - Validate opening stock = previous closing
   - Calculate wastage on each operation
   - Alert if wastage > 0.3%
   - Auto-create closing events

---

### **3. REG-A: Production & Bottling Register**

#### **Purpose:**
Track batch-wise production, bottling operations, and production wastage.

#### **Key Features Implemented:**

**A. Batch-Centric Approach:**
```python
# Each batch has:
- Batch number (e.g., 10AJD01)
- Source vat (SST)
- Blending vat (BRT)
- Production sessions (multi-day support)
- Bottle counts (NOT cases!)
```

**B. Multi-Day Production:**
```python
# Session support:
Batch-1: Day 1 production
Batch-2: Day 2 production (same batch, new session)
Batch-3: Day 3 production
```

**C. Bottling - BOTTLE COUNTS (Critical!):**
```python
# NOT cases, but individual bottles:
bottling_750ml = 1000  # 1000 bottles of 750ml
bottling_600ml = 500   # 500 bottles of 600ml
bottling_500ml = 2000  # 2000 bottles of 500ml
bottling_375ml = 0
bottling_300ml = 0
bottling_180ml = 100   # 100 bottles of 180ml

# Calculate total BL:
total_bl = (750*1000 + 600*500 + 500*2000 + 180*100) / 1000
```

**D. Wastage Calculation:**
```python
# Production wastage threshold: 0.1%
mfm_al = 1000.0  # MFM reading
bottled_al = 998.5  # Calculated from bottles

production_wastage = mfm_al - bottled_al  # 1.5 AL
allowable_wastage = mfm_al * 0.001  # 1.0 AL (0.1%)
chargeable_wastage = max(0, production_wastage - allowable_wastage)  # 0.5 AL
```

**E. Database Schema:**
```python
# Batch Master
batch_id, base_batch_no, brand_id, vat_id,
source_vat_id, start_date, total_volume_bl,
total_volume_al, status

# Reg-A Entry
entry_id, batch_id, session_no,
receipt_from_vat, receipt_strength, receipt_bl, receipt_al,
blending_to_vat, blending_strength, blending_bl, blending_al,
production_date, mfm_density, mfm_strength, mfm_total_bl, mfm_total_al,
bottling_750, bottling_600, bottling_500, bottling_375, bottling_300, bottling_180,
spirit_bottled_bl, avg_strength, spirit_bottled_al,
production_wastage, allowable_wastage, chargeable_wastage,
status, verified_by
```

**F. What You Need to Implement in SIP2LIFE:**

1. **Use existing models:**
   - `BatchMaster` ✅
   - `RegAEntry` ✅ (already has bottle counts!)

2. **Create API endpoints:**
   ```javascript
   POST   /api/registers/rega/batches           // Create batch
   GET    /api/registers/rega/batches           // List batches
   POST   /api/registers/rega/entries           // Create production entry
   GET    /api/registers/rega/entries/:batchId  // Get batch entries
   PUT    /api/registers/rega/entries/:id       // Update entry
   POST   /api/registers/rega/verify/:id        // Verify entry
   ```

3. **Frontend:**
   - Batch creation form (link to Reg-74 transfer)
   - Production entry form with:
     - MFM readings
     - Bottle count inputs (6 sizes)
     - Auto-calculate BL/AL from bottles
     - Wastage calculation display
   - Multi-session support (Batch-1, Batch-2, etc.)

4. **Critical Fix Needed:**
   - Your Prisma schema already has bottle counts ✅
   - Just need to implement the UI
   - Calculate BL from bottles, not cases

---

## 🔧 Common Utilities Needed

### **1. Calculation Functions:**

```javascript
// utils/exciseCalculations.js

// Calculate Bulk Liters
export function calculateBL(massKg, densityGmCc) {
  return massKg / densityGmCc;
}

// Calculate Absolute Liters
export function calculateAL(bulkLiters, strengthPercent) {
  return bulkLiters * (strengthPercent / 100);
}

// Calculate BL from bottle counts
export function calculateBLFromBottles(bottles) {
  const { ml750, ml600, ml500, ml375, ml300, ml180 } = bottles;
  return (
    (ml750 * 750 + ml600 * 600 + ml500 * 500 + 
     ml375 * 375 + ml300 * 300 + ml180 * 180) / 1000
  );
}

// Calculate transit days
export function calculateTransitDays(dispatchDate, receiptDate) {
  const diff = new Date(receiptDate) - new Date(dispatchDate);
  return Math.floor(diff / (1000 * 60 * 60 * 24));
}

// Calculate wastage
export function calculateWastage(advisedAL, receivedAL, threshold = 0.003) {
  const wastage = advisedAL - receivedAL;
  const allowable = advisedAL * threshold;
  const chargeable = Math.max(0, wastage - allowable);
  
  return {
    wastage: Math.max(0, wastage),
    increase: Math.max(0, -wastage),
    allowable,
    chargeable
  };
}
```

### **2. Validation Functions:**

```javascript
// utils/validation.js

export function validateReg76Entry(data) {
  const errors = {};
  
  if (!data.permitNo) errors.permitNo = "Permit number required";
  if (!data.vehicleNo) errors.vehicleNo = "Vehicle number required";
  if (!data.storageVat) errors.storageVat = "Storage vat required";
  if (data.advisedMassKg <= 0) errors.advisedMassKg = "Invalid mass";
  
  return {
    isValid: Object.keys(errors).length === 0,
    errors
  };
}

export function validateReg74Event(data) {
  const errors = {};
  
  if (!data.vatId) errors.vatId = "Vat selection required";
  if (!data.eventType) errors.eventType = "Event type required";
  if (!data.eventDateTime) errors.eventDateTime = "Date/time required";
  
  // Event-specific validation
  if (data.eventType === 'UNLOADING' && !data.receiptData) {
    errors.receiptData = "Receipt data required for unloading";
  }
  
  return {
    isValid: Object.keys(errors).length === 0,
    errors
  };
}
```

### **3. PDF Generation:**

```javascript
// utils/pdfGenerator.js
import jsPDF from 'jspdf';
import 'jspdf-autotable';

export function generateReg76PDF(entries) {
  const doc = new jsPDF('landscape');
  
  doc.setFontSize(16);
  doc.text('Register-76: Spirit Receipt Register', 14, 15);
  
  const tableData = entries.map(entry => [
    entry.reg76_id,
    entry.receiptDate,
    entry.permitNo,
    entry.vehicleNo,
    entry.advisedBl.toFixed(2),
    entry.receivedBl.toFixed(2),
    entry.transitWastageAl.toFixed(2),
    entry.storageVat
  ]);
  
  doc.autoTable({
    head: [['ID', 'Date', 'Permit', 'Vehicle', 'Advised BL', 'Received BL', 'Wastage AL', 'Vat']],
    body: tableData,
    startY: 25
  });
  
  return doc;
}
```

---

## 🎯 Implementation Priority

### **Phase 1: Core Functionality (Week 1-2)**
1. ✅ Reg-76 CRUD API
2. ✅ Reg-76 Form UI
3. ✅ Calculation utilities
4. ✅ Basic validation

### **Phase 2: Vat Operations (Week 3-4)**
1. ✅ Reg-74 Event API
2. ✅ Vat dashboard
3. ✅ Event forms
4. ✅ Stock reconciliation

### **Phase 3: Production (Week 5-6)**
1. ✅ Batch management
2. ✅ Reg-A entry forms
3. ✅ Bottle count inputs
4. ✅ Wastage calculations

### **Phase 4: Integration (Week 7-8)**
1. ✅ Link Reg-76 → Reg-74
2. ✅ Link Reg-74 → Reg-A
3. ✅ Audit logging
4. ✅ Reports & exports

---

## 📚 Key Learnings from Streamlit Project

### **1. User Workflow:**
- Users prefer **tabbed interfaces** (Data Entry vs Admin View)
- **Real-time calculations** are essential
- **Confirmation dialogs** prevent accidental deletions
- **Export options** (CSV, PDF) are heavily used

### **2. Data Management:**
- **Dual storage** (local + cloud) provides reliability
- **Auto-ID generation** prevents duplicates
- **Timestamp everything** for audit trail
- **Filter by date/vehicle** is most common search

### **3. Calculations:**
- **BL/AL calculations** must be precise (3-4 decimal places)
- **Wastage thresholds** vary by register:
  - Reg-76 transit: No fixed threshold
  - Reg-74 storage: 0.3%
  - Reg-A production: 0.1%
- **Temperature corrections** are important

### **4. UI/UX:**
- **Section-wise forms** reduce cognitive load
- **Metric cards** for calculated values
- **Color coding** for wastage (green = OK, red = excess)
- **Expandable sections** keep UI clean

---

## 🚀 Quick Start Guide for SIP2LIFE Developer

### **Step 1: Review Existing Schema**
Your Prisma schema already has most models! ✅
- `Reg76Entry` ✅
- `Reg74Event` ✅
- `RegAEntry` ✅
- `BatchMaster` ✅
- `VatMaster` ✅

### **Step 2: Create API Routes**
```javascript
// server/routes/reg76.js
router.post('/reg76', createReg76Entry);
router.get('/reg76', listReg76Entries);
router.get('/reg76/:id', getReg76Entry);
router.put('/reg76/:id', updateReg76Entry);
router.delete('/reg76/:id', deleteReg76Entry);
```

### **Step 3: Build React Components**
```
client/src/components/registers/
├── Reg76/
│   ├── Reg76Form.jsx
│   ├── Reg76List.jsx
│   ├── Reg76Detail.jsx
│   └── Reg76Filters.jsx
├── Reg74/
│   ├── Reg74Dashboard.jsx
│   ├── Reg74EventForm.jsx
│   └── VatStatusCard.jsx
└── RegA/
    ├── BatchForm.jsx
    ├── ProductionEntry.jsx
    └── BottleCountInput.jsx
```

### **Step 4: Implement Calculations**
Use the utility functions provided above.

### **Step 5: Test with Sample Data**
I can provide you with test data from this Streamlit project.

---

## 📞 Support & Questions

**Streamlit Project Details:**
- **Live URL**: https://excise-parallel-register-system-msne7jvz35aflmgvkmefwb.streamlit.app/
- **GitHub**: https://github.com/saha-trideep/excise-parallel-register-system
- **Contact**: Trideep Saha

**What's Already Working:**
- ✅ Reg-76 complete with delete functionality
- ✅ Reg-74 event-based system
- ✅ Reg-A batch management
- ✅ PDF generation
- ✅ Google Sheets sync
- ✅ Authentication
- ✅ Daily handbook generation

**What You Need to Build:**
- React frontend for all registers
- API endpoints using Prisma
- Real-time calculation hooks
- Dashboard visualizations
- Audit logging UI

---

## 📊 Data Migration

If you want to import existing data from this Streamlit project:

```python
# Export from Streamlit
import pandas as pd
import json

# Reg-76
df = pd.read_csv('reg76_data.csv')
df.to_json('reg76_export.json', orient='records', date_format='iso')

# Import to SIP2LIFE PostgreSQL
# Use Prisma createMany or bulk insert
```

---

## ✅ Checklist for SIP2LIFE Implementation

### **Reg-76:**
- [ ] Create API endpoints
- [ ] Build form UI (8 sections)
- [ ] Implement calculations
- [ ] Add validation
- [ ] Test CRUD operations
- [ ] Add filters
- [ ] Export to PDF/CSV

### **Reg-74:**
- [ ] Create event API
- [ ] Build vat dashboard
- [ ] Event type forms
- [ ] JSON data handling
- [ ] Stock reconciliation
- [ ] Wastage alerts

### **Reg-A:**
- [ ] Batch creation
- [ ] Production entry form
- [ ] Bottle count inputs
- [ ] Wastage calculation
- [ ] Multi-session support
- [ ] Verification workflow

### **Integration:**
- [ ] Link registers
- [ ] Audit logging
- [ ] User permissions
- [ ] Reports
- [ ] Notifications

---

**Created:** December 26, 2025  
**For:** SIP2LIFE Data Management Project  
**From:** Streamlit Excise Register System  
**Status:** Ready for implementation  

**Good luck with the implementation! 🚀**
