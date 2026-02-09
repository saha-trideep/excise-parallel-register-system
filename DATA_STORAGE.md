# 💾 Data Storage Locations - All Registers

## 📋 Overview

Here's where each register saves its data on Streamlit Cloud and locally.

---

## 🗄️ Storage Summary

| Register | Storage Type | File/Database | Location |
|----------|--------------|---------------|----------|
| **Reg-A** | CSV | `rega_data.csv` | Root directory |
| **Reg-74** | CSV | `reg74_data.csv` | Root directory |
| **Reg-76** | CSV | `reg76_data.csv` | Root directory |
| **Reg-78** | CSV | `reg78_data.csv` | Root directory |
| **Reg-B** | SQLite | `excise_registers.db` | Root directory |
| **Excise Duty** | SQLite | `excise_registers.db` | Root directory |

---

## 📁 Detailed Breakdown

### **1. Reg-A (Production Register)**
- **Storage:** CSV file
- **File:** `rega_data.csv`
- **Location:** `./rega_data.csv`
- **Backend:** `rega_backend.py`
- **Status:** ✅ Saves locally

### **2. Reg-74 (Vat Operations)**
- **Storage:** CSV file (with Google Sheets option)
- **File:** `reg74_data.csv`
- **Location:** `./reg74_data.csv`
- **Backend:** `reg74_backend.py`
- **Google Sheets:** Optional (needs credentials)
- **Status:** ✅ Saves locally, ⚠️ Google Sheets needs setup

### **3. Reg-76 (SIP 2 Register)**
- **Storage:** CSV file
- **File:** `reg76_data.csv`
- **Location:** `./reg76_data.csv`
- **Backend:** `reg76_backend.py`
- **Status:** ✅ Saves locally

### **4. Reg-78 (Production Fees)**
- **Storage:** CSV file
- **File:** `reg78_data.csv`
- **Location:** `./reg78_data.csv`
- **Backend:** `reg78_backend.py`
- **Status:** ✅ Saves locally

### **5. Reg-B (Bottle Issues)**
- **Storage:** SQLite database
- **Database:** `excise_registers.db`
- **Location:** `./excise_registers.db`
- **Tables:**
  - `regb_production_fees`
  - `regb_bottle_stock`
  - `regb_daily_summary`
- **Backend:** `regb_backend.py`
- **Status:** ✅ Saves locally

### **6. Excise Duty Register**
- **Storage:** SQLite database
- **Database:** `excise_registers.db` (same as Reg-B)
- **Location:** `./excise_registers.db`
- **Tables:**
  - `excise_duty_ledger`
  - `excise_duty_bottles`
  - `excise_duty_summary`
- **Backend:** `excise_duty_backend.py`
- **Status:** ✅ Saves locally

---

## 🌐 On Streamlit Cloud

### **File Locations:**
All files are saved in the **app's root directory**:
```
/mount/src/excise-parallel-register-system/
├── rega_data.csv
├── reg74_data.csv
├── reg76_data.csv
├── reg78_data.csv
└── excise_registers.db
```

### **⚠️ Important Warning:**

**Data is EPHEMERAL on Streamlit Cloud!**

- ❌ Files are **lost** when app restarts
- ❌ Files are **lost** when app redeploys
- ❌ Files are **lost** after inactivity

**Why?**
- Streamlit Cloud uses temporary file system
- Not designed for persistent storage
- Files reset on every deployment

---

## 💡 Current Status

### **Local Development:**
✅ **All registers save data perfectly!**
- CSV files created in project directory
- SQLite database created in project directory
- Data persists between runs
- Can be backed up manually

### **Streamlit Cloud:**
⚠️ **Data is temporary!**
- Files created but lost on restart
- Good for testing/demo
- **NOT suitable for production**

---

## 🔧 Solutions for Production

### **Option 1: Google Sheets (Recommended)**
- ✅ Data persists forever
- ✅ Real-time sync
- ✅ Easy to view/export
- ✅ Multi-user access
- 📝 Needs setup (see `GOOGLE_SHEETS_FUTURE.md`)

### **Option 2: PostgreSQL Database**
- ✅ Data persists forever
- ✅ Professional solution
- ✅ Better performance
- ⚠️ Requires external database
- 💰 Free tier available (Supabase, Neon)

### **Option 3: Cloud Storage**
- ✅ Data persists forever
- ✅ File-based (CSV)
- ⚠️ Requires AWS S3 or Google Cloud Storage
- 💰 Minimal cost

---

## 📊 Data Files Currently in Project

Check if these files exist locally:

```bash
# In project directory
ls *.csv
ls *.db
```

**Expected files:**
- `rega_data.csv` (if Reg-A used)
- `reg74_data.csv` (if Reg-74 used)
- `reg76_data.csv` (if Reg-76 used)
- `reg78_data.csv` (if Reg-78 used)
- `excise_registers.db` (if Reg-B or Excise Duty used)

---

## 🔍 How to Check Data

### **For CSV files:**
```python
import pandas as pd

# Read any CSV
df = pd.read_csv('rega_data.csv')
print(df)
```

### **For SQLite database:**
```python
import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect('excise_registers.db')

# List all tables
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

# Read a table
df = pd.read_sql_query("SELECT * FROM regb_production_fees", conn)
print(df)
```

---

## 📝 Backup Strategy

### **For Local Development:**

1. **Manual Backup:**
   ```bash
   # Copy all data files
   copy *.csv backup/
   copy *.db backup/
   ```

2. **Git Backup (Optional):**
   - Add data files to git (if small)
   - Push to private repository

### **For Streamlit Cloud:**

1. **Export Data Regularly:**
   - Add export buttons in each register
   - Download CSV/Excel files
   - Store locally or in cloud

2. **Implement Google Sheets:**
   - Auto-sync to Google Sheets
   - Data always backed up
   - Can export anytime

---

## ✅ Summary

### **Current Setup:**

| Register | Saves Data? | Persists Locally? | Persists on Cloud? |
|----------|-------------|-------------------|-------------------|
| Reg-A | ✅ Yes | ✅ Yes | ❌ No |
| Reg-74 | ✅ Yes | ✅ Yes | ❌ No |
| Reg-76 | ✅ Yes | ✅ Yes | ❌ No |
| Reg-78 | ✅ Yes | ✅ Yes | ❌ No |
| Reg-B | ✅ Yes | ✅ Yes | ❌ No |
| Excise Duty | ✅ Yes | ✅ Yes | ❌ No |

### **Recommendation:**

**For Testing:** ✅ Current setup is perfect!

**For Production:** Implement one of:
1. Google Sheets sync (easiest)
2. PostgreSQL database (most professional)
3. Cloud storage (good for CSV files)

---

## 🎯 Next Steps

1. **Test locally** - All data saves perfectly ✅
2. **Test on Streamlit Cloud** - Data works but is temporary ⚠️
3. **For production** - Implement Google Sheets or PostgreSQL 📝

---

**All registers are saving data!** Just remember that on Streamlit Cloud, the data is temporary unless you implement persistent storage. 🎉
