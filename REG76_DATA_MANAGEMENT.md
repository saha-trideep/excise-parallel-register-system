# Reg-76 Data Management Guide

## 📊 Understanding Data Storage

Your Reg-76 application uses a **dual-storage system** for maximum reliability:

### 1. **Primary Storage: Local CSV File**
- **File**: `reg76_data.csv`
- **Location**: Root directory of the project
- **Purpose**: Primary source of truth, fast access, offline capability
- **Format**: Standard CSV with all record fields

### 2. **Backup Storage: Google Sheets**
- **URL**: https://docs.google.com/spreadsheets/d/1Ecmrq9JUhCerhq4mebO1Jtpw8sD_tTo-79_x3Jabr68
- **Purpose**: Cloud backup, collaboration, external access
- **Sync**: Automatic on save, manual sync available

---

## ❓ Why Data Still Shows After CSV Deletion

When you delete data directly from the CSV file, the app may still show records because:

1. **Google Sheets Still Has Data**: The CSV and Google Sheets are synced. If you only delete from CSV, Google Sheets still contains the records.

2. **Browser Cache**: Streamlit may cache data in your browser session.

3. **Incomplete Deletion**: Empty rows in CSV (with commas but no data) are treated as valid rows.

---

## ✅ Proper Way to Delete Records

### **Option 1: Use the Built-in Delete Feature (RECOMMENDED)**

1. Open the Reg-76 application
2. Go to the **"📋 ADMINISTRATIVE VIEW"** tab
3. Scroll down to the **"🗑️ Delete Records"** expander
4. Select the record you want to delete from the dropdown
5. Click **"🗑️ Delete Selected"**
6. Confirm the deletion

**This method ensures:**
- ✅ Record is removed from CSV
- ✅ Record is removed from Google Sheets
- ✅ No orphaned data
- ✅ Proper cleanup

### **Option 2: Clear All Data (DANGER ZONE)**

If you want to start fresh and delete ALL records:

1. Go to **"📋 ADMINISTRATIVE VIEW"** tab
2. Open the **"⚠️ DANGER ZONE: Clear All Data"** expander
3. Type **DELETE ALL** in the confirmation box
4. Click **"🗑️ CLEAR ALL DATA"**

**⚠️ WARNING**: This is irreversible!

---

## 🔧 Manual Data Cleanup (If Needed)

If you've already manually edited the CSV and things are out of sync:

### Step 1: Clean the CSV File
1. Open `reg76_data.csv` in a text editor
2. Delete all rows except the header row (first row)
3. Save the file

The file should look like this:
```csv
reg76_id,permit_no,distillery,spirit_nature,vehicle_no,num_tankers,tanker_capacity,tanker_make_model,invoice_no,invoice_date,export_order_no,export_order_date,import_order_no,import_order_date,export_pass_no,export_pass_date,import_pass_no,import_pass_date,date_dispatch,date_arrival,date_receipt,days_in_transit,adv_weight_kg,adv_avg_density,adv_strength,adv_temp,adv_bl,adv_al,adv_bl_20c,wb_laden_consignee,wb_unladen_consignee,wb_laden_pass,wb_unladen_pass,rec_mass_kg,rec_unload_temp,rec_density_at_temp,rec_density_20c,rec_strength,rec_bl,rec_al,diff_advised_al,transit_wastage_al,allowable_wastage_al,chargeable_wastage_al,storage_vat_no,evc_generated_date,excise_remarks,officer_sig_date,status,created_at,transit_increase_al
```

### Step 2: Sync to Google Sheets
1. Open the Reg-76 app
2. Go to **"📋 ADMINISTRATIVE VIEW"** tab
3. Click the **"🔄 Sync with GSheet"** button
4. This will push the empty CSV to Google Sheets

### Step 3: Verify
1. Check the Google Sheets URL to confirm it's empty
2. Refresh the app to ensure no records show

---

## 🔄 Data Synchronization

### Automatic Sync
- **When**: Every time you save a new record
- **Direction**: CSV → Google Sheets
- **Behavior**: Overwrites Google Sheets with CSV data

### Manual Sync
- **When**: Click "🔄 Sync with GSheet" button
- **Use Case**: When you've manually edited CSV or need to force sync
- **Direction**: CSV → Google Sheets

### Important Notes
- ⚠️ CSV is always the **source of truth**
- ⚠️ Google Sheets is a **mirror/backup**
- ⚠️ Manual edits to Google Sheets will be **overwritten** on next sync

---

## 🐛 Troubleshooting

### Problem: "I deleted from CSV but data still shows"
**Solution**: 
1. Use the built-in delete feature instead
2. Or manually sync after CSV deletion using "🔄 Sync with GSheet"

### Problem: "Empty rows showing in the app"
**Solution**: 
The updated backend now automatically filters out empty rows. Just refresh the app.

### Problem: "Google Sheets sync failed"
**Possible Causes**:
1. No internet connection
2. Service account credentials missing/invalid
3. Google Sheet not shared with service account email

**Solution**:
1. Check internet connection
2. Verify `the-program-482110-e4-7ef9d425d794.json` exists
3. Share the Google Sheet with the service account email from the JSON file

### Problem: "Data inconsistency between CSV and Google Sheets"
**Solution**:
1. Decide which is correct (usually CSV)
2. Use "🔄 Sync with GSheet" to make Google Sheets match CSV
3. Or manually edit CSV and sync

---

## 📝 Best Practices

1. **Always use the app interface** for data operations (add/delete)
2. **Don't manually edit CSV** unless absolutely necessary
3. **Regular backups**: Download CSV exports periodically
4. **Monitor sync status**: Check the sidebar for Google Sheets connection status
5. **Test deletions**: Try deleting a test record first before bulk operations

---

## 🔐 Data Security

- **Local CSV**: Stored on your local machine/server
- **Google Sheets**: Secured by Google Cloud service account
- **Access Control**: Only the service account can modify Google Sheets
- **No public access**: Data is private unless you explicitly share the sheet

---

## 📞 Need Help?

If you encounter issues:
1. Check this guide first
2. Verify CSV file format
3. Check Google Sheets sync status
4. Try manual sync
5. Use the built-in delete features instead of manual edits

---

**Last Updated**: December 26, 2025
**Version**: 2.0 (with delete functionality)
