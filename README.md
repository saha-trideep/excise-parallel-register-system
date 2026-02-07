# 📊 Excise Parallel Register System

**Comprehensive Digital Register Management for SIP 2 LIFE DISTILLERIES**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)

---

## 🎯 Overview

The Excise Parallel Register System is a comprehensive digital solution for managing excise-related registers in distillery operations. Built with Streamlit, it provides an intuitive interface for tracking production, fees, inventory, and excise duty, with a **Local-First Desktop Storage** architecture.

---

## ✨ Features

### 📁 **Local-First Desktop Storage**
- **Primary Storage**: Data is saved directly to `C:\Users\Lenovo\Desktop\Excise_Register_Data\` as Excel files.
- **Backups**: Local CSV backups and optional Google Sheets synchronization.
- **Files**: `Reg76_Data.xlsx`, `Reg74_Data.xlsx`, `RegA_Data.xlsx`, `RegB_Data.xlsx`.

### 🚛 **Reg-76 - Spirit Receipt**
- Tracks spirit receipt from tanker/drums.
- **New Features**: 
  - "Weight of Empty Drum/Tanker" field.
  - "Indication" field for precise measurements.
  - Automatic generation of unique IDs.

### 🧪 **Reg-74 - Spirit Operations**
- Manages Unloading, Reduction, Blending, and Transfer operations.
- **New Features**:
  - Full Opening/Closing stock verification (Dip, Temp, Indication).
  - Wastage calculation and visualization.
  - Desktop Excel integration.

### 🍾 **Reg-A - Production Register**
- Tracks Bottling Operations.
- **New Features**:
  - Expanded bottle sizes (`300ml`, `500ml`, `600ml` + standard sizes).
  - Production Increase & Chargeable Wastage tracking.
  - Auto-fill from Reg-74 batches.

### 📦 **Reg-B - Finished Goods Stock**
- Issue of Country Liquor in Bottles.
- Production fees account (₹3 per bottle).
- Multi-size bottle tracking (All sizes supported).
- Daily summary generation.

### 💰 **Excise Duty Register**
- Personal ledger account of excise duty for IML.
- Strength-based duty rates (auto-calculated).
- Financial account tracking with E-Challan.
- Master-Detail tracking of issued bottles.

### 🔄 **Integration**
- Seamless data flow: `Reg-76 -> Reg-74 -> Reg-A -> Reg-B -> Excise Duty`.
- Real-time validation and automatic calculations.

---

## 🚀 Quick Start

1. **Run the application:**
   ```bash
   streamlit run Home.py
   ```
2. **Access the app:**
   - Open your browser to `http://localhost:8501`

---

## 📁 Project Structure

```
excise-parallel-register-system/
├── Home.py                          # Main landing page
├── reg76.py                         # Reg-76 Application
├── reg74.py                         # Reg-74 Application
├── rega.py                          # Reg-A Application
├── pages/
│   ├── 1_📦_Reg_B.py               # Reg-B Application
│   ├── 2_💰_Excise_Duty.py         # Excise Duty Application
│   └── 6_📚_Daily_Handbook.py      # Daily Handbook Generator
├── desktop_storage.py               # Desktop Excel Storage logic
├── *_schema.py                      # Data Models
├── *_backend.py                     # Data Operations
└── README.md                        # This file
```

---

## 🛠️ Technology Stack

- **Frontend:** Streamlit
- **Backend:** Python + Pandas
- **Storage:** Local Excel (Primary) + Google Sheets (Backups)

---

## 📈 Version History

### v2.0.0 (February 2026) - Desktop Edition
- ✅ **New Feature**: Desktop Excel Storage integration.
- ✅ **Update**: Reg-76 schema expansion (Empty Weight, Indication).
- ✅ **Update**: Reg-74 schema expansion (Opening Dip/Temp/Indication).
- ✅ **Update**: Reg-A UI update for 300/500/600ml bottles.
- ✅ **Verification**: Reg-B & Excise Duty format alignment.

### v1.0.0 (January 2026)
- Initial release with Web-based storage (Google Sheets).
- Reg-B and Excise Duty implementation.

---

**Ready for deployment!** 🚀
