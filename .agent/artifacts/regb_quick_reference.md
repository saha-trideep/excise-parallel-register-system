# Reg-B Quick Reference Guide

## 🚀 Getting Started

### Launch Reg-B
```bash
python -m streamlit run regb.py --server.port 8506
```

**Access:** http://localhost:8506

---

## 📅 Daily Entry Workflow

### Step 1: Select Date
- Use the **Date Selection** in the sidebar
- Default: Today's date
- Can select any past date

### Step 2: Enable Auto-Fill (Recommended)
✅ **Auto-fill from Reg-A Production** - Fetches production data  
✅ **Auto-fill Opening Balances** - Uses previous day's closing

---

## 💰 Section 1: Production Fees Account

### Fields to Enter:

| Field | Description | Auto-Fill |
|-------|-------------|-----------|
| Opening Balance | Previous day's closing | ✅ Yes |
| Deposit Amount | Today's deposit | ❌ Manual |
| E-Challan Number | Challan reference | ❌ Manual |
| E-Challan Date | Challan date | ❌ Manual |
| IML Bottles Qty | IML bottles count | ❌ Manual |
| Total Bottles Produced | All bottles | ✅ From Reg-A |

### Auto-Calculated:
- ✅ Total Amount Credited = Opening + Deposit
- ✅ Fee per Bottle = ₹3.00 (constant)
- ✅ Total Fees Debited = Bottles × ₹3.00
- ✅ Closing Balance = Credited - Debited

### Optional:
- Remarks
- Excise Officer Name

**Click:** 💾 **Save Production Fees**

---

## 🍾 Section 2: Bottle Stock Inventory

### Step 1: Select Product Variant

| Field | Options |
|-------|---------|
| Product Name | Country Liquor (or custom) |
| Strength | 50° U.P. (28.5% v/v), 60° U.P. (22.8% v/v), 70° U.P. (17.1% v/v), 80° U.P. (11.4% v/v) |
| Bottle Size (ml) | 750ml, 600ml, 500ml, 375ml, 300ml, 180ml |

### Step 2: Enter Stock Data

| Field | Description | Auto-Fill |
|-------|-------------|-----------|
| Opening Balance | Previous closing | ✅ Yes |
| Received from Production | Today's production | ✅ From Reg-A |
| Wastage/Breakage | Damaged bottles | ❌ Manual |
| Issued on Duty | Sold/issued | ❌ Manual |

### Auto-Calculated:
- ✅ Total Accounted = Opening + Received
- ✅ Closing Balance = Total - Wastage - Issued
- ✅ All BL (Bulk Litres) values
- ✅ All AL (Absolute Litres) values
- ✅ Wastage percentage

**Click:** 💾 **Save Bottle Stock**

### Step 3: Repeat for Each Variant
Add entries for different sizes/strengths as needed.

---

## 📊 View Modes

### 1️⃣ Data Entry (Default)
- Enter production fees
- Enter bottle stock
- Save individual entries

### 2️⃣ Summary View
- **Production Fees Summary:**
  - Opening, Deposit, Credited, Debited, Closing
- **Bottle Stock Summary (3 Tabs):**
  - 📦 Bottles: All bottle quantities
  - 🔵 BL: Bulk Litres totals
  - 🔴 AL: Absolute Litres totals

### 3️⃣ Administrative View
- Coming soon: Multi-date reports, analytics, PDF export

---

## 🧮 Quick Calculations

### Bottles to BL:
```
BL = (bottles × bottle_size_ml) / 1000

Example:
1,000 bottles × 750ml = 750.000 BL
```

### BL to AL:
```
AL = BL × (strength / 100)

Example (60° U.P. = 22.8% v/v):
750 BL × 22.8% = 171.000 AL
```

### Production Fees:
```
Fees = bottles × ₹3.00

Example:
1,000 bottles × ₹3 = ₹3,000.00
```

---

## ✅ Validation Rules

### Stock Balance:
```
Total Accounted = Wastage + Issued + Closing
```
✅ Must balance exactly

### Fees Balance:
```
Total Credited = Fees Debited + Closing Balance
```
✅ Must balance exactly

### Wastage Alert:
⚠️ System shows wastage percentage if > 0%

---

## 🎯 Common Scenarios

### Scenario 1: Normal Production Day
1. Select today's date
2. Opening balance auto-fills
3. Enter deposit (if any)
4. Production data auto-fills from Reg-A
5. Enter wastage (if any)
6. Enter issued quantity
7. Save both sections

### Scenario 2: Multiple Bottle Sizes
1. Complete entry for first size (e.g., 750ml)
2. Change bottle size dropdown to next (e.g., 375ml)
3. Enter data for that size
4. Repeat for all sizes produced

### Scenario 3: No Production Today
1. Select date
2. Opening balance auto-fills
3. Enter deposit (if any)
4. Total bottles = 0 (no auto-fill)
5. Fees = ₹0.00
6. Stock: Only enter issued/wastage if applicable

### Scenario 4: Viewing Past Data
1. Select past date
2. Switch to "Summary View"
3. Review all metrics
4. Can edit by switching back to "Data Entry"

---

## 🔧 Sidebar Actions

### 🗑️ Delete Entry
- Removes ALL data for selected date
- Use with caution!
- Cannot be undone

### 📊 Generate Summary
- Creates consolidated daily summary
- Saves to database
- Required for summary view

---

## 💡 Tips & Best Practices

### ✅ Do's:
- ✅ Enable auto-fill for faster entry
- ✅ Verify auto-filled data before saving
- ✅ Enter wastage/breakage accurately
- ✅ Generate summary after completing entries
- ✅ Use summary view for verification
- ✅ Enter E-Challan details for deposits

### ❌ Don'ts:
- ❌ Don't skip validation errors
- ❌ Don't delete entries without backup
- ❌ Don't enter negative values
- ❌ Don't forget to save each section
- ❌ Don't mix up bottle sizes

---

## 📋 Data Entry Checklist

Daily completion checklist:

- [ ] Date selected
- [ ] Production fees opening balance verified
- [ ] Deposit entered (if applicable)
- [ ] E-Challan details entered (if deposit made)
- [ ] Production data verified
- [ ] Production fees saved
- [ ] All bottle variants entered:
  - [ ] 750ml variant
  - [ ] 375ml variant
  - [ ] 180ml variant
  - [ ] 90ml variant
- [ ] Wastage/breakage recorded
- [ ] Issued quantities recorded
- [ ] All stock entries saved
- [ ] Summary generated
- [ ] Summary verified

---

## 🆘 Troubleshooting

### Problem: Auto-fill not working
**Solution:** 
- Ensure Reg-A has data for selected date
- Check auto-fill toggles are enabled
- Verify date selection

### Problem: Validation error
**Solution:**
- Check all required fields filled
- Verify calculations match
- Ensure no negative values

### Problem: Data not saving
**Solution:**
- Check for validation errors
- Ensure database is accessible
- Verify all required fields

### Problem: Summary shows ₹0.00
**Solution:**
- Click "Generate Summary" button
- Ensure data is saved first
- Check date selection

---

## 📊 Understanding the Summary

### Production Fees Summary:
- **Opening:** Start of day balance
- **Deposit:** Money added today
- **Credited:** Total available (Opening + Deposit)
- **Debited:** Fees charged for production
- **Closing:** End of day balance (Credited - Debited)

### Bottle Stock Summary:
- **Opening:** Start of day stock
- **Received:** Production added today
- **Total:** All stock to account for
- **Wastage:** Damaged/broken bottles
- **Issued:** Sold/released bottles
- **Closing:** End of day stock

---

## 🎓 Example Entry

### Date: January 24, 2025

**Production Fees:**
- Opening: ₹5,000.00 (auto)
- Deposit: ₹10,000.00
- E-Challan: ECH/2025/001234
- Bottles: 2,500 (auto from Reg-A)
- Fees: ₹7,500.00 (auto)
- Closing: ₹7,500.00 (auto)

**Stock (Country Liquor 60° U.P. (22.8% v/v) - 750ml):**
- Opening: 500 bottles (auto)
- Received: 1,000 bottles (auto from Reg-A)
- Total: 1,500 bottles
- Wastage: 10 bottles
- Issued: 800 bottles
- Closing: 690 bottles
- Closing BL: 517.500
- Closing AL: 117.990

---

## 📞 Support

For issues or questions:
1. Check this guide first
2. Review validation messages
3. Verify Reg-A integration
4. Check database connectivity

---

**Last Updated:** January 24, 2025  
**Version:** 1.0  
**Application:** Reg-B - Issue of Country Liquor in Bottles
