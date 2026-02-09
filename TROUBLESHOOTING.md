# 🚨 TROUBLESHOOTING GUIDE - App Won't Start

## Problem: "This site can't be reached" at localhost:8501

### ✅ SOLUTION: Manual Start

**Option 1: Using Command Prompt (Recommended)**

1. Press `Win + R`
2. Type: `cmd` and press Enter
3. Copy and paste this command:
```
cd [Your-Project-Folder] && streamlit run Home.py
```
4. Press Enter
5. Wait for "You can now view your Streamlit app in your browser"
6. Open browser to: http://localhost:8501

**Option 2: Double-click START_APP.bat**

1. Open File Explorer (should be open now)
2. Find `START_APP.bat` in the folder
3. Double-click it
4. Wait for browser to open

**Option 3: Using PowerShell**

1. Press `Win + X`, choose "PowerShell" or "Terminal"
2. Run:
```powershell
cd "[Your-Project-Folder]"
streamlit run Home.py
```

---

## 🔍 Check if Streamlit is Installed

Open Command Prompt and run:
```
streamlit --version
```

If you get an error, install it:
```
pip install streamlit
```

---

## 📦 Install Missing Package

If PDF generation fails, install reportlab:
```
pip install reportlab
```

---

## 🐛 Common Errors & Fixes

### Error: "streamlit: command not found"
**Fix:**
```
pip install streamlit
```

### Error: "No module named 'maintenance_schema'"
**Fix:** Make sure you're in the correct directory:
```
cd [Your-Project-Folder]
```

### Error: "Port 8501 is already in use"
**Fix:** Kill the old process:
```
taskkill /F /IM streamlit.exe
```
Or use a different port:
```
streamlit run Home.py --server.port 8502
```
Then open: http://localhost:8502

---

## ✅ EASIEST METHOD:

**Just double-click `START_APP.bat` in the File Explorer window I opened!**

---

## 📞 Still Having Issues?

1. Check if Python is installed: Open CMD and type `python --version`
2. Check if pip works: `pip --version`
3. Reinstall Streamlit: `pip uninstall streamlit` then `pip install streamlit`

---

## 🎯 Expected Output When Working:

```
You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

Then browser will auto-open to the app!

