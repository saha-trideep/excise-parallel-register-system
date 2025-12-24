# Reg-74 Schema - Spirit Storage and Operations Register
# Handles: Unloading, Transfer (SST to BRT), Inter-transfer, Reduction/Blending, Production Issue

REG74_COLUMNS = [
    # Identity & Reference
    "reg74_id",
    "operation_type",  # Unloading, SST-to-BRT, Inter-Transfer, Reduction, Production-Issue
    "operation_date",
    "batch_no",  # For reduction/blending operations
    "ref_reg76_id",  # Reference to Reg-76 if unloading operation
    
    # Source Details (Opening Balance / Receipt)
    "source_vat",  # SST-5 to SST-10, BRT-11 to BRT-17, or "Reg-76 Receipt"
    "source_opening_bl",
    "source_opening_al",
    "source_opening_strength",
    
    # Storage Wastage (Before Operation)
    "expected_opening_bl",  # From previous closing
    "expected_opening_al",  # From previous closing
    "actual_opening_bl",  # Physical verification/dip
    "actual_opening_al",  # Calculated from dip
    "storage_wastage_bl",  # Expected - Actual
    "storage_wastage_al",  # Expected - Actual
    "storage_wastage_percentage",  # (Wastage / Expected) * 100
    "storage_days",  # Days since last operation
    "storage_wastage_note",  # Explanation for wastage
    
    # Receipt/Transfer In Details
    "receipt_date",
    "receipt_bl",
    "receipt_al",
    "receipt_strength",
    "receipt_temp",
    "receipt_density",
    
    # Water Addition (for Reduction)
    "water_added_bl",
    "water_temp",
    "target_strength",  # Desired strength after reduction (e.g., 22.81%, 17.4%)
    
    # Total After Receipt/Addition
    "total_bl",
    "total_al",
    "total_strength",
    
    # Issue/Transfer Out Details
    "issue_date",
    "issue_bl",
    "issue_al",
    "issue_strength",
    "issue_temp",
    "issue_density",
    "destination_vat",  # Destination VAT or "Production (Reg-A)"
    
    # Closing Balance
    "closing_bl",
    "closing_al",
    "closing_strength",
    
    # Wastage/Variance
    "wastage_bl",
    "wastage_al",
    "wastage_percentage",
    "wastage_remarks",
    
    # Dip Measurements (Physical Verification)
    "dip_reading_cm",
    "dip_temp",
    "dip_calculated_bl",
    "dip_variance_bl",
    
    # Regulatory & Tracking
    "permit_no",
    "pass_no",
    "pass_date",
    "evc_no",
    "evc_date",
    
    # Remarks & Approval
    "operation_remarks",
    "officer_name",
    "officer_signature_date",
    "status",  # Draft, Submitted, Approved, Locked
    "created_at",
    "updated_at"
]

# Operation Types
OPERATION_TYPES = [
    "Unloading from Reg-76",
    "Transfer SST to BRT",
    "Inter-Transfer SST",
    "Inter-Transfer BRT",
    "Reduction/Blending",
    "Issue for Production"
]

# VAT Lists
SST_VATS = [f"SST-{i}" for i in range(5, 11)]  # SST-5 to SST-10
BRT_VATS = [f"BRT-{i}" for i in range(11, 18)]  # BRT-11 to BRT-17
ALL_VATS = SST_VATS + BRT_VATS

# Target Strengths for Reduction
TARGET_STRENGTHS = [
    "96.1% v/v (Raw Spirit)",
    "22.81% v/v",
    "17.4% v/v",
    "Custom"
]
