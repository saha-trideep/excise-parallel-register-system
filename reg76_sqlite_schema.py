"""
Reg-76 SQLite Schema - Spirit Receipt Register
Database schema for tracking spirit receipts from tankers/drums
"""

# ============================================================================
# DATABASE SCHEMA (SQLite)
# ============================================================================

CREATE_REG76_TABLE = """
CREATE TABLE IF NOT EXISTS reg76_receipts (
    reg76_id TEXT PRIMARY KEY,
    
    -- Identity & Transport
    permit_no TEXT NOT NULL,
    distillery TEXT,
    spirit_nature TEXT,
    vehicle_no TEXT,
    num_tankers INTEGER DEFAULT 1,
    tanker_capacity REAL,
    tanker_make_model TEXT,
    
    -- Documentation
    invoice_no TEXT,
    invoice_date TEXT,
    export_order_no TEXT,
    export_order_date TEXT,
    import_order_no TEXT,
    import_order_date TEXT,
    export_pass_no TEXT,
    export_pass_date TEXT,
    import_pass_no TEXT,
    import_pass_date TEXT,
    
    -- Dates
    date_dispatch TEXT,
    date_arrival TEXT,
    date_receipt TEXT NOT NULL,
    days_in_transit INTEGER,
    
    -- Empty Weight
    empty_tanker_weight_kg REAL,
    
    -- Advised Quantities
    adv_weight_kg REAL,
    adv_avg_density REAL,
    adv_strength REAL,
    adv_temp REAL,
    indication TEXT,
    adv_bl REAL,
    adv_al REAL,
    adv_bl_20c REAL,
    
    -- Weighbridge (Consignee)
    wb_laden_consignee REAL,
    wb_unladen_consignee REAL,
    wb_laden_pass REAL,
    wb_unladen_pass REAL,
    
    -- Received Quantities
    rec_mass_kg REAL,
    rec_unload_temp REAL,
    rec_density_at_temp REAL,
    rec_density_20c REAL,
    rec_strength REAL,
    rec_bl REAL,
    rec_al REAL,
    rec_bl_20c REAL,
    
    -- Differences & Wastage
    diff_advised_al REAL,
    transit_wastage_al REAL,
    transit_increase_al REAL,
    allowable_wastage_al REAL,
    chargeable_wastage_al REAL,
    
    -- Storage
    storage_vat_no TEXT,
    
    -- Regulatory
    evc_generated_date TEXT,
    excise_remarks TEXT,
    officer_sig_date TEXT,
    
    -- Status & Tracking
    status TEXT NOT NULL DEFAULT 'draft',
    created_at TEXT NOT NULL,
    updated_at TEXT
);
"""

# Index for faster queries
CREATE_REG76_INDEXES = """
CREATE INDEX IF NOT EXISTS idx_reg76_date_receipt ON reg76_receipts(date_receipt);
CREATE INDEX IF NOT EXISTS idx_reg76_permit_no ON reg76_receipts(permit_no);
CREATE INDEX IF NOT EXISTS idx_reg76_vehicle_no ON reg76_receipts(vehicle_no);
CREATE INDEX IF NOT EXISTS idx_reg76_storage_vat ON reg76_receipts(storage_vat_no);
CREATE INDEX IF NOT EXISTS idx_reg76_status ON reg76_receipts(status);
"""
