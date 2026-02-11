"""
Spirit Transaction SQLite Schema - Daily Summary of Spirit Movements
"""

CREATE_SPIRIT_TRANSACTION_TABLE = """
CREATE TABLE IF NOT EXISTS spirit_transaction_daily (
    txn_date TEXT PRIMARY KEY,

    strong_spirit_opening_balance REAL DEFAULT 0.0,
    strong_spirit_received_unloaded REAL DEFAULT 0.0,
    in_transit_unloading_increase REAL DEFAULT 0.0,
    in_transit_unloading_wastage REAL DEFAULT 0.0,
    strong_spirit_transferred_to_blending REAL DEFAULT 0.0,
    operational_increase_strong_spirit REAL DEFAULT 0.0,
    strong_spirit_closing_balance REAL DEFAULT 0.0,

    blended_spirit_opening_balance REAL DEFAULT 0.0,
    blended_spirit_received_from_strong REAL DEFAULT 0.0,
    operational_increase_blended_spirit REAL DEFAULT 0.0,
    operational_wastage_blended_spirit REAL DEFAULT 0.0,
    sample_drawn REAL DEFAULT 0.0,
    spirit_passed_to_bottling REAL DEFAULT 0.0,
    blended_spirit_closing_balance REAL DEFAULT 0.0,

    production_increase REAL DEFAULT 0.0,
    production_wastage REAL DEFAULT 0.0,
    total_bottles_produced INTEGER DEFAULT 0,
    total_cases_produced INTEGER DEFAULT 0,
    spirit_accounted_in_bottled_production REAL DEFAULT 0.0,

    net_difference REAL DEFAULT 0.0,
    total_allowable_wastage REAL DEFAULT 0.0,
    chargeable_excess_wastage REAL DEFAULT 0.0,

    recon_status TEXT,
    recon_note TEXT,

    status TEXT NOT NULL DEFAULT 'draft',
    created_at TEXT NOT NULL,
    updated_at TEXT
);
"""

CREATE_SPIRIT_TRANSACTION_INDEXES = """
CREATE INDEX IF NOT EXISTS idx_spirit_txn_date ON spirit_transaction_daily(txn_date);
CREATE INDEX IF NOT EXISTS idx_spirit_txn_status ON spirit_transaction_daily(status);
"""
