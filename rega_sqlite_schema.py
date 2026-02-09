"""
Reg-A SQLite Schema - Production Register (Bottling Operations)
Database schema for tracking bottling production, MFM2 readings, and production wastage
"""

# ============================================================================
# DATABASE SCHEMA (SQLite)
# ============================================================================

CREATE_REGA_TABLE = """
CREATE TABLE IF NOT EXISTS rega_production (
    rega_id TEXT PRIMARY KEY,
    
    -- Identity & Reference
    production_date TEXT NOT NULL,
    production_shift TEXT,
    session_number INTEGER DEFAULT 1,
    batch_no TEXT,
    ref_reg74_id TEXT,
    
    -- Source BRT Details
    source_brt_vat TEXT,
    brt_opening_bl REAL DEFAULT 0.0,
    brt_opening_al REAL DEFAULT 0.0,
    brt_opening_strength REAL,
    brt_available_bl REAL,
    brt_available_al REAL,
    
    -- MFM2 Readings (Production Mass Flow Meter)
    mfm2_reading_bl REAL DEFAULT 0.0,
    mfm2_reading_al REAL DEFAULT 0.0,
    mfm2_strength REAL,
    mfm2_temperature REAL,
    mfm2_density REAL,
    mfm2_start_reading REAL,
    mfm2_end_reading REAL,
    mfm2_total_passed REAL,
    
    -- Bottle Production (Bottle-Centric Entry)
    bottles_180ml INTEGER DEFAULT 0,
    bottles_300ml INTEGER DEFAULT 0,
    bottles_375ml INTEGER DEFAULT 0,
    bottles_500ml INTEGER DEFAULT 0,
    bottles_600ml INTEGER DEFAULT 0,
    bottles_750ml INTEGER DEFAULT 0,
    bottles_1000ml INTEGER DEFAULT 0,
    total_bottles INTEGER DEFAULT 0,
    
    -- Calculated Bottle Volumes
    bottles_bl_180ml REAL DEFAULT 0.0,
    bottles_bl_300ml REAL DEFAULT 0.0,
    bottles_bl_375ml REAL DEFAULT 0.0,
    bottles_bl_500ml REAL DEFAULT 0.0,
    bottles_bl_600ml REAL DEFAULT 0.0,
    bottles_bl_750ml REAL DEFAULT 0.0,
    bottles_bl_1000ml REAL DEFAULT 0.0,
    bottles_total_bl REAL DEFAULT 0.0,
    bottles_total_al REAL DEFAULT 0.0,
    
    -- Production Wastage (MFM2 vs Bottles)
    wastage_bl REAL DEFAULT 0.0,
    wastage_al REAL DEFAULT 0.0,
    wastage_percentage REAL,
    allowable_limit REAL DEFAULT 0.1,
    wastage_status TEXT,
    wastage_note TEXT,
    production_increase_al REAL DEFAULT 0.0,
    chargeable_wastage_al REAL DEFAULT 0.0,
    
    -- BRT Closing Balance (After Production)
    brt_issue_bl REAL,
    brt_issue_al REAL,
    brt_closing_bl REAL,
    brt_closing_al REAL,
    brt_closing_strength REAL,
    
    -- Dispatch Details
    dispatch_type TEXT,
    warehouse_location TEXT,
    godown_number TEXT,
    dispatch_challan_no TEXT,
    dispatch_date TEXT,
    dispatch_vehicle_no TEXT,
    dispatch_destination TEXT,
    
    -- Case Packing (Optional)
    cases_180ml INTEGER DEFAULT 0,
    cases_300ml INTEGER DEFAULT 0,
    cases_375ml INTEGER DEFAULT 0,
    cases_500ml INTEGER DEFAULT 0,
    cases_600ml INTEGER DEFAULT 0,
    cases_750ml INTEGER DEFAULT 0,
    cases_1000ml INTEGER DEFAULT 0,
    total_cases INTEGER DEFAULT 0,
    
    -- Brand & Product Details
    brand_name TEXT,
    product_type TEXT,
    label_registration_no TEXT,
    mrp_per_bottle REAL,
    
    -- Regulatory & Approval
    production_officer_name TEXT,
    production_officer_signature TEXT,
    excise_officer_name TEXT,
    excise_officer_signature TEXT,
    approval_date TEXT,
    operation_remarks TEXT,
    
    -- Multi-Session Tracking
    is_batch_complete INTEGER DEFAULT 0,
    remaining_in_brt_bl REAL,
    remaining_in_brt_al REAL,
    next_session_planned TEXT,
    
    -- Status & Timestamps
    status TEXT NOT NULL DEFAULT 'draft',
    created_at TEXT NOT NULL,
    updated_at TEXT
);
"""

# Index for faster queries
CREATE_REGA_INDEXES = """
CREATE INDEX IF NOT EXISTS idx_rega_production_date ON rega_production(production_date);
CREATE INDEX IF NOT EXISTS idx_rega_batch_no ON rega_production(batch_no);
CREATE INDEX IF NOT EXISTS idx_rega_source_brt_vat ON rega_production(source_brt_vat);
CREATE INDEX IF NOT EXISTS idx_rega_ref_reg74 ON rega_production(ref_reg74_id);
CREATE INDEX IF NOT EXISTS idx_rega_brand_name ON rega_production(brand_name);
CREATE INDEX IF NOT EXISTS idx_rega_status ON rega_production(status);
"""
