# Database Structure Analysis: SIP2LIFE vs Current Excise System

## 📊 Overview

This document compares the database structure and operations between:
- **SIP2LIFE Project** (Node.js + PostgreSQL + Prisma)
- **Current Excise System** (Python + Streamlit + SQLite/CSV)

---

## 🏗️ SIP2LIFE Database Structure

### **Tech Stack:**
- **Backend**: Node.js + Express
- **Database**: PostgreSQL (Supabase)
- **ORM**: Prisma
- **Storage**: Supabase Storage
- **Frontend**: React + Vite

### **Key Models:**

#### 1. **User Model**
```prisma
model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  password  String
  name      String?
  role      String   @default("EMPLOYEE")
  createdAt DateTime @default(now())
  
  // Relations
  documents Document[]
  folders   Folder[]
  registers RegisterLink[]
  auditLogs AuditLog[]
  reg76Entries   Reg76Entry[]
  reg74Events    Reg74Event[]
  regAVerifications RegAEntry[]
}
```

#### 2. **VatMaster Model**
```prisma
model VatMaster {
  id          Int      @id @default(autoincrement())
  vatCode     String   @unique // SST-5 to SST-10, BRT-11 to BRT-17
  vatType     String   // SST, BRT
  capacityBl  Float?
  status      String   @default("IDLE")
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
  
  // Relations
  events      Reg74Event[]
  batches     BatchMaster[]
}
```

#### 3. **Reg74Event Model** (Event-Based System)
```prisma
model Reg74Event {
  id               Int      @id @default(autoincrement())
  vatId            Int
  eventDateTime    DateTime
  eventType        String   // UNLOADING, INTERNAL_TRANSFER, WATER_ADDITION, etc.
  
  // JSON Data Blocks (flexible structure)
  openingData      Json?
  receiptData      Json?
  issueData        Json?
  adjustmentData   Json?
  productionData   Json?
  closingData      Json?
  
  batchId          Int?
  remarks          String?
  createdBy        Int
  createdAt        DateTime @default(now())
}
```

#### 4. **BatchMaster Model**
```prisma
model BatchMaster {
  id              Int      @id @default(autoincrement())
  baseBatchNo     String   @unique // e.g. 10AJD01
  brandId         Int
  vatId           Int      // BRT vat
  sourceVatId     Int?     // SST vat
  startDate       DateTime
  totalVolumeBl   Float?
  totalVolumeAl   Float?
  status          String   @default("OPEN")
  
  // Relations
  events          Reg74Event[]
  regAEntries     RegAEntry[]
}
```

#### 5. **RegAEntry Model** (Production Register)
```prisma
model RegAEntry {
  id              Int      @id @default(autoincrement())
  batchId         Int
  sessionNo       Int      @default(1) // Multi-day support
  
  // Receipt Volume
  receiptFromVat  String?
  receiptStrength Float?
  receiptBl       Float?
  receiptAl       Float?
  
  // Blending
  blendingToVat   String?
  blendingStrength Float?
  blendingBl      Float?
  blendingAl      Float?
  
  // Production
  productionDate  DateTime?
  mfmDensity      Float?
  mfmStrength     Float?
  mfmTotalBl      Float?
  mfmTotalAl      Float?
  
  // Bottling (Bottle counts, not cases)
  bottling750     Int?     @default(0)
  bottling600     Int?     @default(0)
  bottling500     Int?     @default(0)
  bottling375     Int?     @default(0)
  bottling300     Int?     @default(0)
  bottling180     Int?     @default(0)
  
  // Wastage
  productionWastage  Float?
  allowableWastage   Float? // 0.1% threshold
  chargeableWastage  Float?
  
  status          String   @default("PLANNED")
  verifiedBy      Int?
}
```

#### 6. **Reg76Entry Model** (Spirit Receipt)
```prisma
model Reg76Entry {
  id                    Int      @id @default(autoincrement())
  receiptDate           DateTime
  permitNo              String
  exportingDistillery   String
  vehicleNo             String
  natureOfSpirit        String
  storageVat            String
  
  // Advised quantities
  advisedBl             Float
  advisedAl             Float
  advisedStrength       Float
  advisedMassKg         Float
  
  // Received quantities
  receivedStrength      Float
  receivedBl            Float
  receivedAl            Float
  
  // Wastage
  transitWastageBl      Float
  transitWastageAl      Float
  
  createdBy             Int
  createdAt             DateTime @default(now())
  updatedAt             DateTime @updatedAt
}
```

---

## 🔄 Current Excise System Structure

### **Tech Stack:**
- **Backend**: Python + Streamlit
- **Database**: SQLite + CSV files
- **Storage**: Local files + Google Sheets sync

### **Current Models:**

#### Reg-76 (Spirit Receipt)
- CSV-based storage
- Manual calculations
- Google Sheets sync
- No user tracking
- No audit logs

#### Reg-74 (Vat Operations)
- SQLite database
- Event-based tracking
- No batch management
- Limited wastage tracking

#### Reg-A (Production)
- SQLite database
- Batch-centric
- Case-based bottling (needs to change to bottle counts)
- Basic wastage calculation

---

## 🎯 Key Differences

| Feature | SIP2LIFE | Current System |
|---------|----------|----------------|
| **Database** | PostgreSQL | SQLite + CSV |
| **ORM** | Prisma | Raw SQL / Pandas |
| **User Management** | Full RBAC | Basic auth |
| **Audit Logs** | Comprehensive | None |
| **Relationships** | Foreign keys | Manual |
| **Batch Tracking** | Integrated | Separate |
| **Wastage** | Dual thresholds | Single |
| **Multi-day Production** | Session support | Limited |
| **Data Validation** | Schema-level | Application-level |
| **Bottling** | Bottle counts | Cases (needs fix) |

---

## 💡 Recommended Implementation Strategy

### **Phase 1: Database Migration (SQLite → PostgreSQL)**

1. **Set up Supabase** (Free tier available)
2. **Create Prisma schema** for all registers
3. **Migrate existing data** from CSV/SQLite
4. **Implement relationships** between models

### **Phase 2: Backend Restructuring**

1. **Create backend modules** for each register:
   - `reg76_backend.py` → Use Prisma/SQLAlchemy
   - `reg74_backend.py` → Event-based system
   - `rega_backend.py` → Batch-centric with sessions

2. **Implement CRUD operations**:
   - Create
   - Read (with filters)
   - Update
   - Delete (with audit)

3. **Add audit logging**:
   - Track all changes
   - User attribution
   - Timestamp everything

### **Phase 3: Data Relationships**

1. **Link Reg-76 → Reg-74**:
   - Spirit receipt creates vat event
   - Auto-populate opening stock

2. **Link Reg-74 → Reg-A**:
   - Batch creation from vat transfer
   - Track source vat

3. **Wastage Tracking**:
   - Storage wastage (0.3% for SST/BRT)
   - Production wastage (0.1% for bottling)

### **Phase 4: UI Enhancements**

1. **Batch Management Dashboard**
2. **Vat Status Overview**
3. **Wastage Reports**
4. **Audit Trail Viewer**

---

## 📋 Implementation Checklist

### **Immediate Actions:**

- [ ] Set up Supabase account
- [ ] Create Prisma schema file
- [ ] Install required packages (`prisma`, `sqlalchemy`)
- [ ] Create migration scripts
- [ ] Test with sample data

### **Short-term (1-2 weeks):**

- [ ] Migrate Reg-76 to PostgreSQL
- [ ] Implement delete functionality (DONE ✅)
- [ ] Add user tracking
- [ ] Create audit log system

### **Medium-term (1 month):**

- [ ] Migrate Reg-74 with event system
- [ ] Implement batch management
- [ ] Link Reg-74 → Reg-A
- [ ] Fix bottling to use bottle counts

### **Long-term (2-3 months):**

- [ ] Complete data relationships
- [ ] Advanced reporting
- [ ] Performance optimization
- [ ] Mobile-responsive UI

---

## 🛠️ Technical Requirements

### **New Dependencies:**

```txt
# Database
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
alembic==1.13.1

# Or use Prisma (if you want same as SIP2LIFE)
prisma==0.11.0

# Existing
streamlit
pandas
python-dotenv
```

### **Environment Variables:**

```env
# PostgreSQL (Supabase)
DATABASE_URL=postgresql://user:pass@host:5432/dbname
DIRECT_URL=postgresql://user:pass@host:5432/dbname

# Or keep SQLite for now
DATABASE_URL=sqlite:///excise_registers.db
```

---

## 📊 Data Migration Plan

### **Step 1: Export Current Data**
```python
# Export CSV data
import pandas as pd
reg76_df = pd.read_csv('reg76_data.csv')
reg76_df.to_json('reg76_export.json', orient='records')
```

### **Step 2: Create PostgreSQL Schema**
```sql
-- Will be generated from Prisma schema
```

### **Step 3: Import Data**
```python
# Import to PostgreSQL
from sqlalchemy import create_engine
engine = create_engine(DATABASE_URL)
reg76_df.to_sql('reg76_entry', engine, if_exists='append')
```

---

## 🎯 Next Steps

**Would you like me to:**

1. ✅ **Create a Prisma schema** for your current system?
2. ✅ **Set up PostgreSQL migration** scripts?
3. ✅ **Implement the event-based Reg-74** system?
4. ✅ **Add batch management** like SIP2LIFE?
5. ✅ **Create audit logging** system?

Let me know which aspect you'd like to implement first!

---

**Created:** December 26, 2025, 15:30 IST  
**Author:** Analysis of sip2lifedatamanagement repository  
**Status:** Ready for implementation
