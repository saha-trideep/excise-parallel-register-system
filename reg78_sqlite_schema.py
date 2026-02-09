"""
Reg-78 SQLite Schema - Daily Synopsis Register
Database schema for daily synopsis auto-aggregated from Reg-76, Reg-74, and Reg-A
"""

# ============================================================================
# DATABASE SCHEMA (SQLite)
# ============================================================================

CREATE_REG78_TABLE = """
CREATE TABLE IF NOT EXISTS reg78_synopsis (
    reg78_id TEXT PRIMARY KEY,
    
    -- Identity
    synopsis_date TEXT NOT NULL UNIQUE,
    synopsis_hour TEXT,
    
    -- Opening Balance and Receipts & Increases (CREDIT SIDE)
    opening_balance_bl REAL DEFAULT 0.0,
    opening_balance_al REAL DEFAULT 0.0,
    
    -- Consignment Received (from Reg-76)
    consignment_count INTEGER DEFAULT 0,
    consignment_pass_numbers TEXT,
    consignment_received_bl REAL DEFAULT 0.0,
    consignment_received_al REAL DEFAULT 0.0,
    
    -- Quantity Received through MFM1 (from Reg-76)
    mfm1_total_bl REAL DEFAULT 0.0,
    mfm1_total_al REAL DEFAULT 0.0,
    
    -- Operational Increase (from Reg-74)
    operational_increase_bl REAL DEFAULT 0.0,
    operational_increase_al REAL DEFAULT 0.0,
    operational_increase_remarks TEXT,
    
    -- Production Increase (from Reg-A)
    production_increase_bl REAL DEFAULT 0.0,
    production_increase_al REAL DEFAULT 0.0,
    production_increase_remarks TEXT,
    
    -- Increase during Stock Audit
    audit_increase_bl REAL DEFAULT 0.0,
    audit_increase_al REAL DEFAULT 0.0,
    audit_increase_remarks TEXT,
    
    -- Total Balance (Credit Side)
    total_credit_bl REAL DEFAULT 0.0,
    total_credit_al REAL DEFAULT 0.0,
    
    -- ISSUES (DEBIT SIDE)
    
    -- Issues on Payment of Duty (from Reg-A)
    production_total_bl REAL DEFAULT 0.0,
    production_total_al REAL DEFAULT 0.0,
    production_fees_rate REAL DEFAULT 3.0,
    total_production_fees REAL DEFAULT 0.0,
    issues_on_duty_bl REAL DEFAULT 0.0,
    issues_on_duty_al REAL DEFAULT 0.0,
    
    -- Sample Drawn
    sample_drawn_bl REAL DEFAULT 0.0,
    sample_drawn_al REAL DEFAULT 0.0,
    sample_purpose TEXT,
    
    -- Operational Wastage (from Reg-74)
    operational_wastage_bl REAL DEFAULT 0.0,
    operational_wastage_al REAL DEFAULT 0.0,
    operational_wastage_percentage REAL,
    
    -- Production Wastage (from Reg-A)
    production_wastage_bl REAL DEFAULT 0.0,
    production_wastage_al REAL DEFAULT 0.0,
    production_wastage_percentage REAL,
    
    -- Wastage during Stock Audit
    audit_wastage_bl REAL DEFAULT 0.0,
    audit_wastage_al REAL DEFAULT 0.0,
    audit_wastage_remarks TEXT,
    
    -- Total Debit
    total_debit_bl REAL DEFAULT 0.0,
    total_debit_al REAL DEFAULT 0.0,
    
    -- Closing Balance (Spirit Left in Vats)
    closing_balance_bl REAL DEFAULT 0.0,
    closing_balance_al REAL DEFAULT 0.0,
    
    -- VAT-wise Breakdown (from Reg-74)
    sst5_closing_bl REAL DEFAULT 0.0, sst5_closing_al REAL DEFAULT 0.0,
    sst6_closing_bl REAL DEFAULT 0.0, sst6_closing_al REAL DEFAULT 0.0,
    sst7_closing_bl REAL DEFAULT 0.0, sst7_closing_al REAL DEFAULT 0.0,
    sst8_closing_bl REAL DEFAULT 0.0, sst8_closing_al REAL DEFAULT 0.0,
    sst9_closing_bl REAL DEFAULT 0.0, sst9_closing_al REAL DEFAULT 0.0,
    sst10_closing_bl REAL DEFAULT 0.0, sst10_closing_al REAL DEFAULT 0.0,
    brt11_closing_bl REAL DEFAULT 0.0, brt11_closing_al REAL DEFAULT 0.0,
    brt12_closing_bl REAL DEFAULT 0.0, brt12_closing_al REAL DEFAULT 0.0,
    brt13_closing_bl REAL DEFAULT 0.0, brt13_closing_al REAL DEFAULT 0.0,
    brt14_closing_bl REAL DEFAULT 0.0, brt14_closing_al REAL DEFAULT 0.0,
    brt15_closing_bl REAL DEFAULT 0.0, brt15_closing_al REAL DEFAULT 0.0,
    brt16_closing_bl REAL DEFAULT 0.0, brt16_closing_al REAL DEFAULT 0.0,
    brt17_closing_bl REAL DEFAULT 0.0, brt17_closing_al REAL DEFAULT 0.0,
    
    -- Verification & Reconciliation
    physical_stock_bl REAL,
    physical_stock_al REAL,
    book_stock_bl REAL,
    book_stock_al REAL,
    variance_bl REAL,
    variance_al REAL,
    variance_percentage REAL,
    variance_remarks TEXT,
    
    -- Duty Calculation Summary
    total_bottles_produced INTEGER DEFAULT 0,
    total_al_in_bottles REAL DEFAULT 0.0,
    duty_payable REAL DEFAULT 0.0,
    duty_paid REAL DEFAULT 0.0,
    duty_pending REAL DEFAULT 0.0,
    
    -- Officer Approval
    prepared_by TEXT,
    verified_by TEXT,
    excise_officer_name TEXT,
    excise_officer_signature TEXT,
    approval_date TEXT,
    remarks TEXT,
    
    -- Status & Timestamps
    status TEXT NOT NULL DEFAULT 'draft',
    created_at TEXT NOT NULL,
    updated_at TEXT
);
"""

# Index for faster queries
CREATE_REG78_INDEXES = """
CREATE INDEX IF NOT EXISTS idx_reg78_synopsis_date ON reg78_synopsis(synopsis_date);
CREATE INDEX IF NOT EXISTS idx_reg78_status ON reg78_synopsis(status);
"""
