# 🔧 E+H Maintenance Automation System

## Quick Start Guide

### 📦 Installation

```bash
# Navigate to project
cd C:\Users\Lenovo\.gemini\antigravity\playground\trideepexcise-parallel-register-system

# Install new dependencies
pip install reportlab

# Run the app
streamlit run Home.py
```

### 🎯 Features

1. **Daily Activity Entry**
   - Select instruments from dropdown
   - Record maintenance activities
   - Track time, issues, resolutions
   - Auto-save to SQLite database

2. **Activity Viewing**
   - Filter by date range
   - View summary statistics
   - Delete activities if needed

3. **Monthly PDF Reports**
   - Professional E+H branded reports
   - NABL compliance documentation
   - Auto-generated signatures section
   - One-click download

### 📁 New Files Created

- `maintenance_schema.py` - Database models
- `maintenance_backend.py` - Database operations  
- `maintenance_pdf.py` - PDF generation engine
- `pages/7_🔧_Maintenance_Log.py` - Streamlit UI

### 🗄️ Database

Activities are stored in `excise_registers.db` in table `maintenance_activities`

### 🎨 Usage

1. **Add Daily Entry:**
   - Go to "Daily Entry" tab
   - Select 2 instruments
   - Choose activity type
   - Fill in time and details
   - Click Submit

2. **View Activities:**
   - Go to "View Activities" tab
   - Select date range
   - View summary and details

3. **Generate Monthly Report:**
   - Go to "Monthly Report" tab
   - Select report period
   - Click "Generate PDF Report"
   - Download the PDF

### 📊 Example Workflow

```
Day 1: Add maintenance activity for RLT-1 and MFM-1
Day 2: Add activity for VALVE_ST1 and VALVE_BV1
...
Day 30: Generate monthly report
```

### 🔐 Security

- All data stored locally in SQLite
- PDF reports marked as Confidential/Internal
- No external API calls needed

### 🛠️ Customization

To add more instruments, edit the dictionaries in `pages/7_🔧_Maintenance_Log.py`:

```python
eh_instruments = {
    "RLT-1": "SB002121133",
    # Add more here
}

valves = {
    "VALVE_UL1": "2122-03-79952",
    # Add more here
}
```

### 📞 Support

Field Service Engineer: Trideep Saha
Email: trideep.s@primetech-solutions.in
Phone: +91-8670914733

---

**Endress+Hauser (India) Pvt Ltd.**
CIN: U24110MH1999PTC121643
