# 🗄️ Excise System Database Schema & Data Relationships

This document details the hybrid database structure (SQLite + CSV) and the relational links that power the automation "Ripple Effect".

## 📊 Entity Relationship Diagram (ERD)

```mermaid
erDiagram
    %% TRANSIT & STORAGE (CSV BASED)
    REG76_RECEIPT {
        string reg76_id PK
        string permit_no
        string pass_no
        float receipt_bl
        float receipt_al
    }

    REG74_OPERATIONS {
        string reg74_id PK
        string ref_reg76_id FK "Links to R76_ID"
        string batch_no UK "Unique Batch Reference"
        string source_vat
        string destination_vat
        float closing_bl
        float storage_wastage_al
    }

    %% PRODUCTION (CSV BASED)
    REGA_PRODUCTION {
        string rega_id PK
        string batch_no FK "Links to R74_Batch"
        string ref_reg74_id FK "Links to R74_ID"
        int total_bottles
        float wastage_al
        string brand_name
    }

    REG78_SYNOPSIS {
        string reg78_id PK
        date synopsis_date
        float total_production_fees
        float opening_balance_bl
        float closing_balance_bl
    }

    %% INVENTORY & FINANCIALS (SQLITE BASED)
    REGB_BOTTLE_STOCK {
        int regb_stock_id PK
        date date
        string product_name FK "Maps to RegA.brand_name"
        int quantity_received FK "From RegA.total_bottles"
        int issue_on_duty_bottles
        float closing_balance_bottles
    }

    EXCISE_DUTY_LEDGER {
        int duty_id PK
        date date
        float opening_balance
        float amount_credited
        float duty_debited FK "Calculated from RegB.Issues"
        float closing_balance
    }

    %% RELATIONSHIPS
    REG76_RECEIPT ||--o{ REG74_OPERATIONS : "unloads into"
    REG74_OPERATIONS ||--o{ REGA_PRODUCTION : "provides spirit for"
    REGA_PRODUCTION ||--o{ REGB_BOTTLE_STOCK : "populates inventory"
    REGA_PRODUCTION ||--o{ REG78_SYNOPSIS : "updates synopsis"
    REGB_BOTTLE_STOCK ||--o{ EXCISE_DUTY_LEDGER : "triggers duty debit"

```

## 🛠️ Data Storage Breakdown

### **1. Filesystem CSV (Operational Data)**
These files track the high-volume, real-time physical movement of spirit.
- `reg76_data.csv`: Tanker Arrivals.
- `reg74_data.csv`: Spirit Storage & Blending (The Base Registry).
- `rega_data.csv`: Daily Bottling & Production Efficiency.
- `reg78_data.csv`: Daily Consolidated Synopsis.

### **2. SQLite Database: `excise_registers.db` (Ledger Data)**
Used for relational tracking, historical inventory, and financial balances.
- `regb_bottle_stock`: Finished goods inventory tracking.
- `regb_production_fees`: Tracking the ₹3/bottle fee account.
- `excise_duty_ledger`: Primary government financial account.
- `excise_duty_bottles`: Specific duty calculations per brand issued.

## 🔗 Key Relational Hooks

| Linkage | From Field | To Field | Purpose |
| :--- | :--- | :--- | :--- |
| **Receipt Link** | `reg76_data.permit_no` | `reg74_data.permit_no` | Ensures tanker data flows to unloading. |
| **Batch Link** | `reg74_data.batch_no` | `rega_data.batch_no` | Ensures production pulls from correct blend. |
| **Inventory Link**| `rega_data.brand_name` | `regb_stock.product_name` | Auto-adds production to Warehouse stock. |
| **Synopsis Link** | `rega_data.production_date`| `reg78_data.synopsis_date` | Auto-calculates daily fees and wastage. |
| **Duty Link** | `regb_stock.issue_on_duty` | `duty_ledger.duty_debited` | Auto-calculates tax when bottles leave godown. |

---
**Document Status**: ✅ Integrated  
**Version**: 2.0  
**Archirect**: Antigravity AI
