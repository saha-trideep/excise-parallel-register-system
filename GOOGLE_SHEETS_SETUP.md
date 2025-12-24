# 📊 Google Sheets Integration Setup Guide

## ✅ **Status: Fixed and Pushed!**

The Google Sheets integration now works with **two modes**:

1. **Streamlit Cloud** - Uses secrets (secure)
2. **Local Development** - Uses JSON file (fallback)
3. **CSV Fallback** - Works without Google Sheets

---

## 🔧 **How It Works Now**

### **Priority Order:**
1. ✅ Try Streamlit Cloud secrets first
2. ✅ Fallback to local JSON file
3. ✅ Fallback to CSV if both fail

**Result:** Reg-74 will **always work**, even without Google Sheets!

---

## 🌐 **For Streamlit Cloud Deployment**

### **Option A: Enable Google Sheets Sync** (Recommended)

#### **Step 1: Get Your Credentials**

You have the file: `the-program-482110-e4-7ef9d425d794.json`

Open it - it looks like this:
```json
{
  "type": "service_account",
  "project_id": "the-program-482110-e4",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "...@the-program-482110-e4.iam.gserviceaccount.com",
  "client_id": "...",
  ...
}
```

#### **Step 2: Add to Streamlit Cloud Secrets**

1. Go to your app on Streamlit Cloud
2. Click **"⚙️ Settings"** (bottom right)
3. Click **"Secrets"**
4. Paste this (replace with your actual values):

```toml
[gsheets_credentials]
type = "service_account"
project_id = "the-program-482110-e4"
private_key_id = "YOUR_PRIVATE_KEY_ID"
private_key = "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY_HERE\n-----END PRIVATE KEY-----\n"
client_email = "YOUR_SERVICE_ACCOUNT@the-program-482110-e4.iam.gserviceaccount.com"
client_id = "YOUR_CLIENT_ID"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "YOUR_CERT_URL"
```

**OR** paste the entire JSON as a string:

```toml
[gsheets_credentials]
# Copy the ENTIRE contents of your JSON file here
```

#### **Step 3: Save and Restart**

- Click "Save"
- App will automatically restart
- Google Sheets sync will work!

---

### **Option B: Use CSV Only** (No Setup Needed)

**Current Status:** ✅ **Already Working!**

- Reg-74 will use local CSV file
- No Google Sheets needed
- Data saved locally in `reg74_data.csv`

**Advantages:**
- ✅ No setup required
- ✅ Works immediately
- ✅ No external dependencies

**Disadvantages:**
- ⚠️ Data lost on app restart (Streamlit Cloud)
- ⚠️ No real-time sync

---

## 💡 **Recommendation**

### **For Testing/Development:**
- Use **CSV mode** (current setup)
- No configuration needed
- Works immediately

### **For Production:**
- Use **Google Sheets sync**
- Add credentials to Streamlit secrets
- Real-time data sync
- Data persistence

---

## 🔍 **How to Check Which Mode is Active**

When you open Reg-74, you'll see:

**Google Sheets Active:**
```
✅ Connected to Google Sheets
```

**CSV Fallback Active:**
```
⚠️ Google Sheets not available. Using local CSV.
```

---

## 📋 **Current Setup**

### **What's Already Done:**
- ✅ Code updated to support Streamlit secrets
- ✅ CSV fallback implemented
- ✅ Dependencies added to requirements.txt
- ✅ Pushed to GitHub
- ✅ Streamlit Cloud will auto-redeploy

### **What You Need to Do:**
- **Nothing!** App works with CSV
- **Optional:** Add Google Sheets credentials for sync

---

## 🎯 **Quick Decision Guide**

### **Use CSV if:**
- You're just testing
- You don't need data persistence
- You want zero setup

### **Use Google Sheets if:**
- You need data to persist
- You want real-time sync
- You're deploying to production

---

## 📝 **Example: Adding Secrets**

Here's exactly what to paste in Streamlit Cloud Secrets:

```toml
[gsheets_credentials]
type = "service_account"
project_id = "the-program-482110-e4"
private_key_id = "7ef9d425d794..."
private_key = "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASC...\n-----END PRIVATE KEY-----\n"
client_email = "excise-sync@the-program-482110-e4.iam.gserviceaccount.com"
client_id = "123456789..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/excise-sync%40the-program-482110-e4.iam.gserviceaccount.com"
```

**Important:** Replace all values with your actual credentials from the JSON file!

---

## ✅ **Summary**

**Current Status:**
- ✅ Reg-74 works on Streamlit Cloud (CSV mode)
- ✅ No errors
- ✅ Data saved locally
- ✅ Google Sheets optional

**To Enable Google Sheets:**
1. Add credentials to Streamlit Cloud secrets
2. That's it!

**No Action Needed:**
- App works as-is with CSV
- Google Sheets is optional

---

**Your app is fully functional now!** 🎉
