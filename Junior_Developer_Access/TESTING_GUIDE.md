# 🧪 Junior Developer Testing Guide: Excise Parallel Register System

## 🎯 **Objective**
Your task is to verify that this digital system acts as a **flawless mirror** to the physical excise registers. You must ensure that every column in the physical Excel format exists in the app, data flows correctly between registers, and files save to the correct location.

## ⚙️ **The "Golden Rule" of Testing**
> **"If it's in the Excel Register, it MUST be in the App."**

---

## 🔍 **Phase 1: The "Column-by-Column" Inspection**
For each register listed below, open the **"Registers.xls"** file on one screen and the **Streamlit App** on the other.

### **1. 📝 Manual Entry Registers (Verify Inputs)**
These forms require user input. Check that every Excel column has a matching input field.

*   **Reg-76 (Spirit Receipt)**
    *   *Check:* Does the form ask for Permit No, Invoice Date, MFM readings?
    *   *Verify:* Can you enter the "Received A.L." and "Wastage"?
*   **Reg-74 (Spirit Operations)**
    *   *Check:* Are there fields for Dip(cm) and Temperature?
    *   *Verify:* Does the system automatically calculate B.L., Strength, and A.L. when you enter the Dip?
*   **Reg-A (Production)**
    *   *Check:* Are all bottling lines (Line 1, Line 2...) selectable?
    *   *Check:* Can you enter production counts for all bottle sizes (180ml, 375ml, 750ml, etc.)?
*   **Reg-B (Bottle Issues)**
    *   *Check:* Can you manually enter the "Opening Balance", "Issues", and "Closing Balance"? 
*   **Excise Duty Ledger**
    *   *Check:* Can you deposit money and record duty debited?

### **2. 🤖 Automated Registers (Verify Read-Only/Auto-Fill)**
These forms should **NOT** accept manual data entry. They should calculate values based on previous inputs.

*   **Reg-78 (Production Fees)**
    *   *Inspection:* Do **NOT** type here.
    *   *Verify:* Does it automatically calculate fees based on the production numbers you entered in Reg-A?
*   **Daily Handbook**
    *   *Inspection:* This is a generated PDF.
    *   *Verify:* Does it auto-fill the "SST Stock", "Production", and "Duty" sections?
    *   *Check:* Is the "Issued Bottle Details" section blank (as intended for manual filler)?

---

## 🔄 **Phase 2: Validation of Data Flow (The Chain Reaction)**
Test the "Domino Effect". Data entered in one register must automatically update the others.

1.  **Step 1 (Receipt)**: Enter a receipt in **Reg-76** (e.g., 10,000 A.L. into SST-5).
    *   *Test:* Go to **Reg-74**. Does SST-5 now show that stock available?
    *   *Test:* Go to **Handbook**. Does the "Received (A.L.)" column in the SST table show this amount?
2.  **Step 2 (Operation)**: Perform a transfer in **Reg-74**.
    *   *Test:* Check the stock levels. Did the Source Vat decrease and Destination Vat increase?
3.  **Step 3 (Production)**: Enter production in **Reg-A**.
    *   *Test:* Go to **Reg-78**. Did the production fees increase automatically?

---

## 💾 **Phase 3: Data Storage Verification**
The system must save data to your local machine, not just in the browser.

*   **The Desktop Check**:
    1.  Minimize the application.
    2.  Go to your **Desktop**.
    3.  Look for a folder (e.g., `Excise_Registers_Data`).
    4.  Open the Excel files inside.
    5.  **Critcial Check**: confirm the row you just added in the app appears in this Excel file.

---

## 🐞 **Reporting Bugs**
If you find a discrepancy, report it using this format:
*   **Register**: (e.g., Reg-74)
*   **Missing Field**: (e.g., "Excel has column 'Temp', App key is missing")
*   **Calculation Error**: (e.g., "Excel says 500 * 4 = 2000, App says 2001")
*   **File Error**: (e.g., "Data did not save to Desktop Excel file")
