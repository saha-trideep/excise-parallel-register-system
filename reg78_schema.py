# Reg-78 Schema - Daily Synopsis Register
# Auto-aggregates data from Reg-76, Reg-74, and Reg-A

REG78_COLUMNS = [
    # Identity
    "reg78_id",
    "synopsis_date",
    "synopsis_hour",  # End of day hour (e.g., 18:00)
    
    # Opening Balance and Receipts & Increases (CREDIT SIDE)
    "opening_balance_bl",  # From previous day Reg-78 closing OR Reg-74 total
    "opening_balance_al",
    
    # Consignment Received (from Reg-76)
    "consignment_count",  # Number of consignments
    "consignment_pass_numbers",  # Comma-separated pass numbers
    "consignment_received_bl",  # Sum of all Reg-76 receipts
    "consignment_received_al",
    
    # Quantity Received through MFM1 (from Reg-76)
    "mfm1_total_bl",  # Sum of all MFM1 readings for the day
    "mfm1_total_al",
    
    # Operational Increase (from Reg-74)
    "operational_increase_bl",  # Any operational gains
    "operational_increase_al",
    "operational_increase_remarks",
    
    # Production Increase (from Reg-A)
    "production_increase_bl",  # Any production gains
    "production_increase_al",
    "production_increase_remarks",
    
    # Increase during Stock Audit
    "audit_increase_bl",  # Manual entry
    "audit_increase_al",
    "audit_increase_remarks",
    
    # Total Balance (Credit Side)
    "total_credit_bl",  # Sum of all increases (Col 2-7)
    "total_credit_al",
    
    # ISSUES (DEBIT SIDE)
    
    # Issues on Payment of Duty (from Reg-A)
    "production_total_bl",  # Total BL produced today (MFM2 reading)
    "production_total_al",  # Total AL produced today
    "production_fees_rate",  # ₹3/- per BL (Production Fees)
    "total_production_fees",  # ₹3 × Total BL
    "issues_on_duty_bl",  # Spirit issued for production
    "issues_on_duty_al",
    
    # Sample Drawn
    "sample_drawn_bl",  # Manual entry
    "sample_drawn_al",
    "sample_purpose",  # Testing/Quality Control/Excise
    
    # Operational Wastage (from Reg-74)
    "operational_wastage_bl",  # Storage wastage from Reg-74
    "operational_wastage_al",
    "operational_wastage_percentage",
    
    # Production Wastage (from Reg-A)
    "production_wastage_bl",  # Production wastage from Reg-A
    "production_wastage_al",
    "production_wastage_percentage",
    
    # Wastage during Stock Audit
    "audit_wastage_bl",  # Manual entry
    "audit_wastage_al",
    "audit_wastage_remarks",
    
    # Total Debit
    "total_debit_bl",  # Sum of all issues (Col 9-13)
    "total_debit_al",
    
    # Closing Balance (Spirit Left in Vats)
    "closing_balance_bl",  # Total Credit - Total Debit
    "closing_balance_al",
    
    # VAT-wise Breakdown (from Reg-74)
    "sst5_closing_bl", "sst5_closing_al",
    "sst6_closing_bl", "sst6_closing_al",
    "sst7_closing_bl", "sst7_closing_al",
    "sst8_closing_bl", "sst8_closing_al",
    "sst9_closing_bl", "sst9_closing_al",
    "sst10_closing_bl", "sst10_closing_al",
    "brt11_closing_bl", "brt11_closing_al",
    "brt12_closing_bl", "brt12_closing_al",
    "brt13_closing_bl", "brt13_closing_al",
    "brt14_closing_bl", "brt14_closing_al",
    "brt15_closing_bl", "brt15_closing_al",
    "brt16_closing_bl", "brt16_closing_al",
    "brt17_closing_bl", "brt17_closing_al",
    
    # Verification & Reconciliation
    "physical_stock_bl",  # From dip readings
    "physical_stock_al",
    "book_stock_bl",  # From register calculations
    "book_stock_al",
    "variance_bl",  # Physical - Book
    "variance_al",
    "variance_percentage",
    "variance_remarks",
    
    # Duty Calculation Summary
    "total_bottles_produced",  # From Reg-A
    "total_al_in_bottles",  # From Reg-A
    "duty_payable",  # ₹3 × Total AL
    "duty_paid",  # Manual entry
    "duty_pending",  # Payable - Paid
    
    # Officer Approval
    "prepared_by",
    "verified_by",
    "excise_officer_name",
    "excise_officer_signature",
    "approval_date",
    "remarks",
    
    # Status & Timestamps
    "status",  # Draft/Submitted/Approved/Locked
    "created_at",
    "updated_at"
]

# Production Fees Rate
PRODUCTION_FEES_RATE_PER_BL = 3.0  # ₹3/- per BL (not AL)

# VAT Lists
SST_VATS = [f"SST-{i}" for i in range(5, 11)]  # SST-5 to SST-10
BRT_VATS = [f"BRT-{i}" for i in range(11, 18)]  # BRT-11 to BRT-17
ALL_VATS = SST_VATS + BRT_VATS

# Sample Purposes
SAMPLE_PURPOSES = [
    "Quality Control Testing",
    "Excise Department Sample",
    "Laboratory Analysis",
    "Strength Verification",
    "Regulatory Compliance"
]

# Status Options
STATUS_OPTIONS = [
    "Draft",
    "Submitted",
    "Approved",
    "Locked"
]
