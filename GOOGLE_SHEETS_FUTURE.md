# 📊 Google Sheets Integration - Future Enhancement

## 📋 Status: Planned for Later

Google Sheets integration is planned for **all registers** to enable:
- Real-time data synchronization
- Cloud backup
- Multi-user access
- Data persistence across app restarts

---

## 🎯 Registers to Integrate

### ✅ **Already Implemented:**
1. **Reg-74** - Vat Operations (partial implementation, needs secrets)

### 📝 **Planned:**
2. **Reg-A** - Production Register
3. **Reg-B** - Bottle Issues
4. **Reg-76** - SIP 2 Register
5. **Reg-78** - Production Fees
6. **Excise Duty Register**

---

## 🔧 Implementation Plan

### **Phase 1: Setup Google Cloud Project**
- [x] Create Google Cloud project
- [x] Enable Google Sheets API
- [x] Create service account
- [x] Generate credentials JSON

### **Phase 2: Backend Integration**
- [x] Reg-74 backend (done)
- [ ] Reg-A backend
- [ ] Reg-B backend
- [ ] Reg-76 backend
- [ ] Reg-78 backend
- [ ] Excise Duty backend

### **Phase 3: Streamlit Cloud Configuration**
- [ ] Add credentials to Streamlit secrets
- [ ] Test all registers
- [ ] Verify data sync

### **Phase 4: Testing & Deployment**
- [ ] Test CRUD operations
- [ ] Test concurrent access
- [ ] Verify data integrity
- [ ] Deploy to production

---

## 📝 Implementation Pattern

Each register will follow this pattern:

```python
# In backend file (e.g., regb_backend.py)

import streamlit as st
try:
    import gspread
    from google.oauth2.service_account import Credentials
    GSPREAD_AVAILABLE = True
except ImportError:
    GSPREAD_AVAILABLE = False

def get_google_client():
    """Returns gspread client"""
    if not GSPREAD_AVAILABLE:
        return None
        
    try:
        # Try Streamlit secrets first (for Streamlit Cloud)
        if "gsheets_credentials" in st.secrets:
            scopes = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]
            creds = Credentials.from_service_account_info(
                st.secrets["gsheets_credentials"],
                scopes=scopes
            )
            return gspread.authorize(creds)
        # Fallback to local JSON file
        elif os.path.exists(JSON_KEY):
            creds = Credentials.from_service_account_file(JSON_KEY, scopes=scopes)
            return gspread.authorize(creds)
    except Exception as e:
        st.warning(f"Google Sheets not available. Using local database.")
    return None

def sync_to_google_sheets(data):
    """Sync data to Google Sheets"""
    client = get_google_client()
    if client:
        # Sync logic here
        pass
    # Fallback to local database
    save_to_local_db(data)
```

---

## 🔐 Streamlit Cloud Secrets Format

Add this to Streamlit Cloud → Settings → Secrets:

```toml
[gsheets_credentials]
type = "service_account"
project_id = "the-program-482110-e4"
private_key_id = "YOUR_PRIVATE_KEY_ID"
private_key = "-----BEGIN PRIVATE KEY-----\nYOUR_KEY\n-----END PRIVATE KEY-----\n"
client_email = "YOUR_SERVICE_ACCOUNT@the-program-482110-e4.iam.gserviceaccount.com"
client_id = "YOUR_CLIENT_ID"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "YOUR_CERT_URL"
```

---

## 📊 Google Sheets Structure

### **One Spreadsheet, Multiple Worksheets:**

```
Excise Registers Spreadsheet
├── Reg-A (worksheet)
├── Reg-74 (worksheet)
├── Reg-76 (worksheet)
├── Reg-78 (worksheet)
├── Reg-B (worksheet)
└── Excise Duty (worksheet)
```

**Spreadsheet URL:** `https://docs.google.com/spreadsheets/d/YOUR_SPREADSHEET_ID`

---

## ✅ Benefits

### **With Google Sheets:**
- ✅ Data persists across app restarts
- ✅ Real-time sync
- ✅ Multi-user access
- ✅ Cloud backup
- ✅ Easy data export
- ✅ Audit trail

### **Without Google Sheets (Current):**
- ✅ Works immediately
- ✅ No setup required
- ✅ No external dependencies
- ⚠️ Data lost on app restart (Streamlit Cloud)
- ⚠️ Local database only

---

## 🎯 Current Recommendation

### **For Now:**
- Use **local database** (SQLite/CSV)
- Works perfectly for testing
- No configuration needed

### **For Production:**
- Implement **Google Sheets sync**
- Add credentials to Streamlit secrets
- Enable for all registers

---

## 📝 Next Steps

When ready to implement:

1. **Create Google Spreadsheet:**
   - Create one spreadsheet
   - Add worksheets for each register
   - Share with service account email

2. **Update Backend Files:**
   - Add Google Sheets integration code
   - Implement sync functions
   - Add fallback to local database

3. **Configure Streamlit Cloud:**
   - Add credentials to secrets
   - Test each register
   - Verify sync

4. **Deploy:**
   - Push to GitHub
   - Streamlit Cloud auto-redeploys
   - Test in production

---

## 📌 Notes

- Service account email: `excise-sync@the-program-482110-e4.iam.gserviceaccount.com`
- Credentials file: `the-program-482110-e4-7ef9d425d794.json` (local only, not in GitHub)
- All registers will use the same service account
- Each register gets its own worksheet

---

**Implementation Timeline:** To be determined based on priority

**Current Status:** All registers work with local database ✅
