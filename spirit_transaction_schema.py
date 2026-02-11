# Spirit Transaction Schema - Daily Summary of Spirit Movements

SPIRIT_TRANSACTION_COLUMNS = [
    "txn_date",
    "strong_spirit_opening_balance",
    "strong_spirit_received_unloaded",
    "in_transit_unloading_increase",
    "in_transit_unloading_wastage",
    "strong_spirit_transferred_to_blending",
    "operational_increase_strong_spirit",
    "strong_spirit_closing_balance",
    "blended_spirit_opening_balance",
    "blended_spirit_received_from_strong",
    "operational_increase_blended_spirit",
    "operational_wastage_blended_spirit",
    "sample_drawn",
    "spirit_passed_to_bottling",
    "blended_spirit_closing_balance",
    "production_increase",
    "production_wastage",
    "total_bottles_produced",
    "total_cases_produced",
    "spirit_accounted_in_bottled_production",
    "net_difference",
    "total_allowable_wastage",
    "chargeable_excess_wastage",
    "recon_status",
    "recon_note",
    "status",
    "created_at",
    "updated_at",
]

DEFAULT_RECON_TOLERANCE_AL = 0.01

STATUS_OPTIONS = [
    "Draft",
    "Submitted",
    "Approved",
    "Locked",
]
