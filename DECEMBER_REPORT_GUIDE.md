# 📊 GENERATE DECEMBER REPORT - STEP BY STEP GUIDE

## 🎯 Goal
Generate a professional PDF report for December 4-30, 2025 using your CSV data.

---

## ✅ STEP 1: Import Your December Data

### Method 1: Double-click the Batch File (EASIEST)
1. Open File Explorer
2. Navigate to your project folder (where the app is installed)
3. Find and double-click: **IMPORT_DECEMBER_DATA.bat**
4. Wait for "Successfully imported X activities!" message
5. Press any key to close

### Method 2: Using Command Prompt
1. Press Win+R, type `cmd`, press Enter
2. Copy and paste:
```
cd [Your-Project-Folder]
python import_december_data.py
```
3. Press Enter

---

## ✅ STEP 2: Generate the PDF Report

### In Your Streamlit App (Already Open):

1. **Navigate to Maintenance Log**
   - Look at the left sidebar
   - Click on: **🔧 Maintenance Log**

2. **Go to Monthly Report Tab**
   - Click on the **"📄 Monthly Report"** tab (third tab)

3. **Set Date Range**
   - Report Start Date: **04-12-2025** (December 4, 2025)
   - Report End Date: **30-12-2025** (December 30, 2025)

4. **Generate Report**
   - Click the blue button: **"📄 Generate PDF Report"**
   - Wait 5-10 seconds for processing

5. **Download Report**
   - Click the **"📥 Download Report"** button that appears
   - PDF will be saved to your Downloads folder

---

## 📄 What the Report Contains

Your PDF report will include:

### Page 1: Cover Page
- Company details (Endress+Hauser)
- Customer: SIP2LIFE DISTILLERIES PVT. LTD.
- Report period: December 4-30, 2025
- Summary metrics:
  - Total activities
  - Total hours worked
  - Field Service Engineer: Trideep Saha
  - Plant HR Manager: Samrat Chatterjee

### Page 2: Detailed Activity Log
- Date-wise activities table
- Instruments maintained
- Activity descriptions
- Time spent
- Status checkmarks

### Page 3: Authorization & Signatures
- Certification statement
- Signature sections for:
  - Plant HR Manager (Samrat Chatterjee)
  - Field Service Engineer (Trideep Saha)
- Date fields

---

## 🎨 Report Features

✅ Professional E+H branding (Blue colors)
✅ NABL compliance documentation
✅ Confidential/Internal marking
✅ Page numbers
✅ Company contact details
✅ Ready to print and sign

---

## 🔍 Preview Your Data First (Optional)

Before generating the PDF, you can preview your data:

1. Click on **"📊 View Activities"** tab
2. Set date range: Dec 4-30, 2025
3. Click **"🔍 Search"**
4. You'll see:
   - Total Activities count
   - Total Hours worked
   - Average Time per activity
   - Unique Days worked
   - Full activity table

---

## 🐛 Troubleshooting

### "No data found"
- Make sure you ran IMPORT_DECEMBER_DATA.bat first
- Check if the CSV file is at: `C:\Users\Lenovo\Desktop\Daily Activity Database - Activity.csv`

### "Module not found" error when importing
```
pip install pandas
```

### PDF generation fails
```
pip install reportlab
```

### Can't find the batch file
Path: `IMPORT_DECEMBER_DATA.bat` (in project folder)

---

## 📂 File Locations

**CSV Source:** `C:\Users\Lenovo\Desktop\Daily Activity Database - Activity.csv`

**Import Script:** `./import_december_data.py`

**Database:** `./excise_registers.db`

**Generated PDF:** Will be in the project folder with name like:
`maintenance_report_2025-12-04_2025-12-30.pdf`

---

## ✨ Quick Summary

1. ✅ Run **IMPORT_DECEMBER_DATA.bat** (double-click it)
2. ✅ Open Streamlit app (if not already open)
3. ✅ Go to **🔧 Maintenance Log** → **📄 Monthly Report** tab
4. ✅ Set dates: Dec 4-30, 2025
5. ✅ Click **Generate PDF Report**
6. ✅ Click **Download Report**
7. ✅ Done! 🎉

---

## 📞 Need Help?

Check the app is running at: http://localhost:8501

Restart app: Double-click **START_APP.bat**

Field Service Engineer: Trideep Saha
Email: trideep.s@primetech-solutions.in

