# Reg-A Schema - Production Register (Bottling Operations)
# Tracks: MFM2 readings, Bottle production, Production wastage (0.1% limit)

REGA_COLUMNS = [
    # Identity & Reference
    "rega_id",
    "production_date",
    "production_shift",  # Morning/Evening/Night
    "session_number",  # For multi-day production (e.g., 1, 2, 3)
    "batch_no",  # Links to Reg-74 batch
    "ref_reg74_id",  # Reference to Reg-74 reduction record
    
    # Source BRT Details
    "source_brt_vat",  # BRT-11 to BRT-17
    "brt_opening_bl",
    "brt_opening_al",
    "brt_opening_strength",
    "brt_available_bl",  # Available for this session
    "brt_available_al",
    
    # MFM2 Readings (Production Mass Flow Meter)
    "mfm2_reading_bl",  # Total volume passed through MFM2
    "mfm2_reading_al",  # MFM2 BL × Strength / 100
    "mfm2_strength",  # Spirit strength % v/v
    "mfm2_temperature",  # Temperature at measurement
    "mfm2_density",  # Density at measurement
    "mfm2_start_reading",  # Meter start reading
    "mfm2_end_reading",  # Meter end reading
    "mfm2_total_passed",  # End - Start
    
    # Bottle Production (Bottle-Centric Entry)
    "bottles_180ml",  # Count of 180ml bottles
    "bottles_300ml",  # Count of 300ml bottles (NEW)
    "bottles_375ml",  # Count of 375ml bottles
    "bottles_500ml",  # Count of 500ml bottles (NEW)
    "bottles_600ml",  # Count of 600ml bottles (NEW)
    "bottles_750ml",  # Count of 750ml bottles
    "bottles_1000ml",  # Count of 1000ml bottles
    "total_bottles",  # Sum of all bottles
    
    # Calculated Bottle Volumes
    "bottles_bl_180ml",  # bottles_180ml × 0.180
    "bottles_bl_300ml",  # bottles_300ml × 0.300 (NEW)
    "bottles_bl_375ml",  # bottles_375ml × 0.375
    "bottles_bl_500ml",  # bottles_500ml × 0.500 (NEW)
    "bottles_bl_600ml",  # bottles_600ml × 0.600 (NEW)
    "bottles_bl_750ml",  # bottles_750ml × 0.750
    "bottles_bl_1000ml",  # bottles_1000ml × 1.000
    "bottles_total_bl",  # Sum of all bottle BL
    "bottles_total_al",  # Bottles BL × Strength / 100
    
    # Production Wastage (MFM2 vs Bottles)
    "wastage_bl",  # MFM2 BL - Bottles BL
    "wastage_al",  # MFM2 AL - Bottles AL
    "wastage_percentage",  # (Wastage AL / MFM2 AL) × 100
    "allowable_limit",  # 0.1% constant
    "wastage_status",  # Within/Exceeds
    "wastage_note",  # Mandatory if exceeds 0.1%
    "production_increase_al", # NEW: Negative wastage
    "chargeable_wastage_al", # NEW: Calculated chargeable
    
    # BRT Closing Balance (After Production)
    "brt_issue_bl",  # Spirit issued from BRT (= MFM2 reading)
    "brt_issue_al",
    "brt_closing_bl",  # Opening - Issue
    "brt_closing_al",
    "brt_closing_strength",
    
    # Dispatch Details
    "dispatch_type",  # Warehouse/Direct Sale/Godown
    "warehouse_location",
    "godown_number",
    "dispatch_challan_no",
    "dispatch_date",
    "dispatch_vehicle_no",
    "dispatch_destination",
    
    # Case Packing (Optional - for reference)
    "cases_180ml",  # Number of cases (12 bottles/case)
    "cases_300ml",  # (NEW)
    "cases_375ml",  # Number of cases (12 bottles/case)
    "cases_500ml",  # (NEW)
    "cases_600ml",  # (NEW)
    "cases_750ml",  # Number of cases (12 bottles/case)
    "cases_1000ml",  # Number of cases (12 bottles/case)
    "total_cases",
    
    # Brand & Product Details
    "brand_name",
    "product_type",  # IMFL/Country Liquor/Beer
    "label_registration_no",
    "mrp_per_bottle",
    
    # Regulatory & Approval
    "production_officer_name",
    "production_officer_signature",
    "excise_officer_name",
    "excise_officer_signature",
    "approval_date",
    "operation_remarks",
    
    # Multi-Session Tracking
    "is_batch_complete",  # True if batch fully consumed
    "remaining_in_brt_bl",
    "remaining_in_brt_al",
    "next_session_planned",
    
    # Status & Timestamps
    "status",  # Draft/Submitted/Approved/Locked
    "created_at",
    "updated_at"
]

# Production Shifts
PRODUCTION_SHIFTS = [
    "Morning (6 AM - 2 PM)",
    "Evening (2 PM - 10 PM)",
    "Night (10 PM - 6 AM)"
]

# Bottle Sizes (in Litres)
BOTTLE_SIZES = {
    "180ml": 0.180,
    "300ml": 0.300, # NEW
    "375ml": 0.375,
    "500ml": 0.500, # NEW
    "600ml": 0.600, # NEW
    "750ml": 0.750,
    "1000ml": 1.000
}

# Bottles per Case (Standard)
BOTTLES_PER_CASE = {
    "180ml": 48,  # 48 bottles per case
    "300ml": 24,  # Assumed 24
    "375ml": 24,  # 24 bottles per case
    "500ml": 12,  # Assumed 12
    "600ml": 12,  # Assumed 12
    "750ml": 12,  # 12 bottles per case
    "1000ml": 12   # 12 bottles per case
}

# BRT VAT List
BRT_VATS = [f"BRT-{i}" for i in range(11, 18)]  # BRT-11 to BRT-17

# Dispatch Types
DISPATCH_TYPES = [
    "Warehouse Storage",
    "Direct Sale",
    "Godown Transfer",
    "Export",
    "Sample/Testing"
]

# Product Types
PRODUCT_TYPES = [
    "IMFL (Indian Made Foreign Liquor)",
    "Country Liquor",
    "Beer",
    "Wine",
    "RTD (Ready to Drink)"
]

# Wastage Thresholds
PRODUCTION_WASTAGE_LIMIT = 0.1  # 0.1% of MFM2 AL
CRITICAL_WASTAGE_THRESHOLD = 1.0  # 1.0% triggers critical alert

# Status Options
STATUS_OPTIONS = [
    "Draft",
    "Submitted",
    "Approved",
    "Locked"
]
