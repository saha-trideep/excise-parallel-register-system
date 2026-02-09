"""
Reg-74 SQLite Schema - Spirit Storage and Operations Register
Database schema for tracking spirit operations (Unloading, Transfer, Reduction, Blending)
"""

# ============================================================================
# DATABASE SCHEMA (SQLite)
# ============================================================================

CREATE_REG74_TABLE = """
CREATE TABLE IF NOT EXISTS reg74_operations (
    reg74_id TEXT PRIMARY KEY,
    
    -- Identity & Reference
    operation_type TEXT NOT NULL,
    operation_date TEXT NOT NULL,
    batch_no TEXT,
    ref_reg76_id TEXT,
    
    -- Source Details (Opening Balance / Receipt)
    source_vat TEXT,
    source_opening_bl REAL DEFAULT 0.0,
    source_opening_al REAL DEFAULT 0.0,
    source_opening_strength REAL,
    
    -- Storage Wastage (Before Operation)
    expected_opening_bl REAL,
    expected_opening_al REAL,
    actual_opening_bl REAL,
    actual_opening_al REAL,
    opening_dip_cm REAL,
    opening_temp REAL,
    opening_indication TEXT,
    storage_wastage_bl REAL DEFAULT 0.0,
    storage_wastage_al REAL DEFAULT 0.0,
    storage_wastage_percentage REAL,
    storage_days INTEGER,
    storage_wastage_note TEXT,
    
    -- Receipt/Transfer In Details
    receipt_date TEXT,
    receipt_bl REAL DEFAULT 0.0,
    receipt_al REAL DEFAULT 0.0,
    receipt_strength REAL,
    receipt_temp REAL,
    receipt_density REAL,
    
    -- Water Addition (for Reduction)
    water_added_bl REAL DEFAULT 0.0,
    water_temp REAL,
    target_strength REAL,
    
    -- Total After Receipt/Addition
    total_bl REAL DEFAULT 0.0,
    total_al REAL DEFAULT 0.0,
    total_strength REAL,
    
    -- Issue/Transfer Out Details
    issue_date TEXT,
    issue_bl REAL DEFAULT 0.0,
    issue_al REAL DEFAULT 0.0,
    issue_strength REAL,
    issue_temp REAL,
    issue_density REAL,
    destination_vat TEXT,
    
    -- Closing Balance
    closing_bl REAL DEFAULT 0.0,
    closing_al REAL DEFAULT 0.0,
    closing_strength REAL,
    
    -- Wastage/Variance
    wastage_bl REAL DEFAULT 0.0,
    wastage_al REAL DEFAULT 0.0,
    wastage_percentage REAL,
    wastage_remarks TEXT,
    
    -- Dip Measurements (Physical Verification)
    dip_reading_cm REAL,
    dip_temp REAL,
    closing_indication TEXT,
    dip_calculated_bl REAL,
    dip_variance_bl REAL,
    
    -- Regulatory & Tracking
    permit_no TEXT,
    pass_no TEXT,
    pass_date TEXT,
    evc_no TEXT,
    evc_date TEXT,
    
    -- Remarks & Approval
    operation_remarks TEXT,
    officer_name TEXT,
    officer_signature_date TEXT,
    status TEXT NOT NULL DEFAULT 'draft',
    created_at TEXT NOT NULL,
    updated_at TEXT
);
"""

# Index for faster queries
CREATE_REG74_INDEXES = """
CREATE INDEX IF NOT EXISTS idx_reg74_operation_date ON reg74_operations(operation_date);
CREATE INDEX IF NOT EXISTS idx_reg74_operation_type ON reg74_operations(operation_type);
CREATE INDEX IF NOT EXISTS idx_reg74_source_vat ON reg74_operations(source_vat);
CREATE INDEX IF NOT EXISTS idx_reg74_destination_vat ON reg74_operations(destination_vat);
CREATE INDEX IF NOT EXISTS idx_reg74_ref_reg76 ON reg74_operations(ref_reg76_id);
CREATE INDEX IF NOT EXISTS idx_reg74_batch_no ON reg74_operations(batch_no);
CREATE INDEX IF NOT EXISTS idx_reg74_status ON reg74_operations(status);
"""
