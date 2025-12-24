"""
Reg-B Schema - Issue of Country Liquor in Bottles
Pydantic models and database schema for finished goods inventory and production fees
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal

# ============================================================================
# CONSTANTS
# ============================================================================

FEE_PER_BOTTLE = Decimal("3.00")  # ₹3 per bottle production fee
BOTTLE_SIZES_ML = [750, 600, 500, 375, 300, 180]  # Standard bottle sizes in ml
STRENGTH_OPTIONS = [
    Decimal("28.5"),  # 50 degree U.P.
    Decimal("22.8"),  # 60 degree U.P.
    Decimal("17.1"),  # 70 degree U.P.
    Decimal("11.4")   # 80 degree U.P.
]  # % v/v

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class ProductionFeesAccount(BaseModel):
    """Model for Production Fees Financial Account (Section 1)"""
    
    regb_fees_id: Optional[int] = None
    date: date
    
    # Opening & Deposits
    opening_balance: Decimal = Field(default=Decimal("0.00"), ge=0, description="Opening balance in ₹")
    deposit_amount: Decimal = Field(default=Decimal("0.00"), ge=0, description="Deposit made today in ₹")
    echallan_no: Optional[str] = Field(default=None, description="E-Challan number for deposit")
    echallan_date: Optional[date] = Field(default=None, description="E-Challan date")
    
    # Auto-calculated Credits
    total_credited: Decimal = Field(default=Decimal("0.00"), ge=0, description="Total amount credited (opening + deposit)")
    
    # Production Data (from Reg-A)
    iml_bottles_qty: int = Field(default=0, ge=0, description="IML bottles produced")
    total_bottles_produced: int = Field(default=0, ge=0, description="Total bottles produced")
    
    # Fee Calculation
    fee_per_bottle: Decimal = Field(default=FEE_PER_BOTTLE, description="Fee per bottle (₹3)")
    total_fees_debited: Decimal = Field(default=Decimal("0.00"), ge=0, description="Total fees debited")
    
    # Closing Balance
    closing_balance: Decimal = Field(default=Decimal("0.00"), description="Closing balance (credited - debited)")
    
    # Administrative
    remarks: Optional[str] = Field(default=None, description="Remarks")
    excise_officer_name: Optional[str] = Field(default=None, description="Name of excise officer")
    excise_officer_signature: Optional[str] = Field(default=None, description="Digital signature path")
    
    status: str = Field(default="draft", description="Status: draft/submitted")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @field_validator('total_credited', mode='before')
    @classmethod
    def calculate_total_credited(cls, v, info):
        """Auto-calculate total credited"""
        if info.data.get('opening_balance') is not None and info.data.get('deposit_amount') is not None:
            return info.data['opening_balance'] + info.data['deposit_amount']
        return v
    
    @field_validator('total_fees_debited', mode='before')
    @classmethod
    def calculate_fees_debited(cls, v, info):
        """Auto-calculate total fees debited"""
        if info.data.get('total_bottles_produced') is not None and info.data.get('fee_per_bottle') is not None:
            return Decimal(info.data['total_bottles_produced']) * info.data['fee_per_bottle']
        return v
    
    @field_validator('closing_balance', mode='before')
    @classmethod
    def calculate_closing_balance(cls, v, info):
        """Auto-calculate closing balance"""
        if info.data.get('total_credited') is not None and info.data.get('total_fees_debited') is not None:
            return info.data['total_credited'] - info.data['total_fees_debited']
        return v
    
    class Config:
        from_attributes = True


class BottleStockInventory(BaseModel):
    """Model for Bottle Stock Inventory (Section 2)"""
    
    regb_stock_id: Optional[int] = None
    date: date
    
    # Product Details
    product_name: str = Field(description="Product name (e.g., 'Country Liquor 22.81%')")
    strength: Decimal = Field(description="Strength in % v/v")
    bottle_size_ml: int = Field(description="Bottle size in ml (750, 375, 180, 90)")
    
    # Bottle Quantities
    opening_balance_bottles: int = Field(default=0, ge=0, description="Opening balance in bottles")
    quantity_received_bottles: int = Field(default=0, ge=0, description="Bottles received from production")
    total_accounted_bottles: int = Field(default=0, ge=0, description="Total bottles to be accounted")
    wastage_breakage_bottles: int = Field(default=0, ge=0, description="Wastage/breakage in bottles")
    issue_on_duty_bottles: int = Field(default=0, ge=0, description="Bottles issued on payment of duty")
    closing_balance_bottles: int = Field(default=0, ge=0, description="Closing balance in bottles")
    
    # BL (Bulk Litres) Quantities
    opening_balance_bl: Decimal = Field(default=Decimal("0.000"), ge=0, description="Opening balance in BL")
    received_bl: Decimal = Field(default=Decimal("0.000"), ge=0, description="BL received from production")
    total_bl: Decimal = Field(default=Decimal("0.000"), ge=0, description="Total BL to be accounted")
    wastage_bl: Decimal = Field(default=Decimal("0.000"), ge=0, description="Wastage in BL")
    issue_bl: Decimal = Field(default=Decimal("0.000"), ge=0, description="BL issued on duty")
    closing_bl: Decimal = Field(default=Decimal("0.000"), ge=0, description="Closing balance in BL")
    
    # AL (Absolute Litres) Quantities
    opening_balance_al: Decimal = Field(default=Decimal("0.000"), ge=0, description="Opening balance in AL")
    received_al: Decimal = Field(default=Decimal("0.000"), ge=0, description="AL received from production")
    total_al: Decimal = Field(default=Decimal("0.000"), ge=0, description="Total AL to be accounted")
    wastage_al: Decimal = Field(default=Decimal("0.000"), ge=0, description="Wastage in AL")
    issue_al: Decimal = Field(default=Decimal("0.000"), ge=0, description="AL issued on duty")
    closing_al: Decimal = Field(default=Decimal("0.000"), ge=0, description="Closing balance in AL")
    
    status: str = Field(default="draft", description="Status: draft/submitted")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @field_validator('total_accounted_bottles', mode='before')
    @classmethod
    def calculate_total_accounted(cls, v, info):
        """Auto-calculate total bottles to be accounted"""
        if info.data.get('opening_balance_bottles') is not None and info.data.get('quantity_received_bottles') is not None:
            return info.data['opening_balance_bottles'] + info.data['quantity_received_bottles']
        return v
    
    @field_validator('closing_balance_bottles', mode='before')
    @classmethod
    def calculate_closing_bottles(cls, v, info):
        """Auto-calculate closing balance in bottles"""
        if all(k in info.data for k in ['total_accounted_bottles', 'wastage_breakage_bottles', 'issue_on_duty_bottles']):
            return info.data['total_accounted_bottles'] - info.data['wastage_breakage_bottles'] - info.data['issue_on_duty_bottles']
        return v
    
    @field_validator('total_bl', mode='before')
    @classmethod
    def calculate_total_bl(cls, v, info):
        """Auto-calculate total BL"""
        if info.data.get('opening_balance_bl') is not None and info.data.get('received_bl') is not None:
            return info.data['opening_balance_bl'] + info.data['received_bl']
        return v
    
    @field_validator('closing_bl', mode='before')
    @classmethod
    def calculate_closing_bl(cls, v, info):
        """Auto-calculate closing BL"""
        if all(k in info.data for k in ['total_bl', 'wastage_bl', 'issue_bl']):
            return info.data['total_bl'] - info.data['wastage_bl'] - info.data['issue_bl']
        return v
    
    @field_validator('total_al', mode='before')
    @classmethod
    def calculate_total_al(cls, v, info):
        """Auto-calculate total AL"""
        if info.data.get('opening_balance_al') is not None and info.data.get('received_al') is not None:
            return info.data['opening_balance_al'] + info.data['received_al']
        return v
    
    @field_validator('closing_al', mode='before')
    @classmethod
    def calculate_closing_al(cls, v, info):
        """Auto-calculate closing AL"""
        if all(k in info.data for k in ['total_al', 'wastage_al', 'issue_al']):
            return info.data['total_al'] - info.data['wastage_al'] - info.data['issue_al']
        return v
    
    class Config:
        from_attributes = True


class RegBDailySummary(BaseModel):
    """Model for Reg-B Daily Summary (Consolidated View)"""
    
    regb_summary_id: Optional[int] = None
    date: date
    
    # Bottle Totals (all sizes/strengths combined)
    total_opening_bottles: int = Field(default=0, ge=0)
    total_received_bottles: int = Field(default=0, ge=0)
    total_accounted_bottles: int = Field(default=0, ge=0)
    total_wastage_bottles: int = Field(default=0, ge=0)
    total_issued_bottles: int = Field(default=0, ge=0)
    total_closing_bottles: int = Field(default=0, ge=0)
    
    # BL Totals
    total_opening_bl: Decimal = Field(default=Decimal("0.000"), ge=0)
    total_received_bl: Decimal = Field(default=Decimal("0.000"), ge=0)
    total_accounted_bl: Decimal = Field(default=Decimal("0.000"), ge=0)
    total_wastage_bl: Decimal = Field(default=Decimal("0.000"), ge=0)
    total_issued_bl: Decimal = Field(default=Decimal("0.000"), ge=0)
    total_closing_bl: Decimal = Field(default=Decimal("0.000"), ge=0)
    
    # AL Totals
    total_opening_al: Decimal = Field(default=Decimal("0.000"), ge=0)
    total_received_al: Decimal = Field(default=Decimal("0.000"), ge=0)
    total_accounted_al: Decimal = Field(default=Decimal("0.000"), ge=0)
    total_wastage_al: Decimal = Field(default=Decimal("0.000"), ge=0)
    total_issued_al: Decimal = Field(default=Decimal("0.000"), ge=0)
    total_closing_al: Decimal = Field(default=Decimal("0.000"), ge=0)
    
    # Production Fees Summary
    production_fees_opening: Decimal = Field(default=Decimal("0.00"), ge=0)
    production_fees_deposit: Decimal = Field(default=Decimal("0.00"), ge=0)
    production_fees_credited: Decimal = Field(default=Decimal("0.00"), ge=0)
    production_fees_debited: Decimal = Field(default=Decimal("0.00"), ge=0)
    production_fees_closing: Decimal = Field(default=Decimal("0.00"))
    
    status: str = Field(default="draft")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ============================================================================
# DATABASE SCHEMA (SQLite)
# ============================================================================

CREATE_REGB_PRODUCTION_FEES_TABLE = """
CREATE TABLE IF NOT EXISTS regb_production_fees (
    regb_fees_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL UNIQUE,
    
    -- Opening & Deposits
    opening_balance REAL NOT NULL DEFAULT 0.00,
    deposit_amount REAL NOT NULL DEFAULT 0.00,
    echallan_no TEXT,
    echallan_date TEXT,
    
    -- Credits
    total_credited REAL NOT NULL DEFAULT 0.00,
    
    -- Production Data
    iml_bottles_qty INTEGER NOT NULL DEFAULT 0,
    total_bottles_produced INTEGER NOT NULL DEFAULT 0,
    
    -- Fee Calculation
    fee_per_bottle REAL NOT NULL DEFAULT 3.00,
    total_fees_debited REAL NOT NULL DEFAULT 0.00,
    
    -- Closing
    closing_balance REAL NOT NULL DEFAULT 0.00,
    
    -- Administrative
    remarks TEXT,
    excise_officer_name TEXT,
    excise_officer_signature TEXT,
    
    status TEXT NOT NULL DEFAULT 'draft',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
"""

CREATE_REGB_BOTTLE_STOCK_TABLE = """
CREATE TABLE IF NOT EXISTS regb_bottle_stock (
    regb_stock_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    
    -- Product Details
    product_name TEXT NOT NULL,
    strength REAL NOT NULL,
    bottle_size_ml INTEGER NOT NULL,
    
    -- Bottle Quantities
    opening_balance_bottles INTEGER NOT NULL DEFAULT 0,
    quantity_received_bottles INTEGER NOT NULL DEFAULT 0,
    total_accounted_bottles INTEGER NOT NULL DEFAULT 0,
    wastage_breakage_bottles INTEGER NOT NULL DEFAULT 0,
    issue_on_duty_bottles INTEGER NOT NULL DEFAULT 0,
    closing_balance_bottles INTEGER NOT NULL DEFAULT 0,
    
    -- BL Quantities
    opening_balance_bl REAL NOT NULL DEFAULT 0.000,
    received_bl REAL NOT NULL DEFAULT 0.000,
    total_bl REAL NOT NULL DEFAULT 0.000,
    wastage_bl REAL NOT NULL DEFAULT 0.000,
    issue_bl REAL NOT NULL DEFAULT 0.000,
    closing_bl REAL NOT NULL DEFAULT 0.000,
    
    -- AL Quantities
    opening_balance_al REAL NOT NULL DEFAULT 0.000,
    received_al REAL NOT NULL DEFAULT 0.000,
    total_al REAL NOT NULL DEFAULT 0.000,
    wastage_al REAL NOT NULL DEFAULT 0.000,
    issue_al REAL NOT NULL DEFAULT 0.000,
    closing_al REAL NOT NULL DEFAULT 0.000,
    
    status TEXT NOT NULL DEFAULT 'draft',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    
    UNIQUE(date, product_name, strength, bottle_size_ml)
);
"""

CREATE_REGB_DAILY_SUMMARY_TABLE = """
CREATE TABLE IF NOT EXISTS regb_daily_summary (
    regb_summary_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL UNIQUE,
    
    -- Bottle Totals
    total_opening_bottles INTEGER NOT NULL DEFAULT 0,
    total_received_bottles INTEGER NOT NULL DEFAULT 0,
    total_accounted_bottles INTEGER NOT NULL DEFAULT 0,
    total_wastage_bottles INTEGER NOT NULL DEFAULT 0,
    total_issued_bottles INTEGER NOT NULL DEFAULT 0,
    total_closing_bottles INTEGER NOT NULL DEFAULT 0,
    
    -- BL Totals
    total_opening_bl REAL NOT NULL DEFAULT 0.000,
    total_received_bl REAL NOT NULL DEFAULT 0.000,
    total_accounted_bl REAL NOT NULL DEFAULT 0.000,
    total_wastage_bl REAL NOT NULL DEFAULT 0.000,
    total_issued_bl REAL NOT NULL DEFAULT 0.000,
    total_closing_bl REAL NOT NULL DEFAULT 0.000,
    
    -- AL Totals
    total_opening_al REAL NOT NULL DEFAULT 0.000,
    total_received_al REAL NOT NULL DEFAULT 0.000,
    total_accounted_al REAL NOT NULL DEFAULT 0.000,
    total_wastage_al REAL NOT NULL DEFAULT 0.000,
    total_issued_al REAL NOT NULL DEFAULT 0.000,
    total_closing_al REAL NOT NULL DEFAULT 0.000,
    
    -- Production Fees
    production_fees_opening REAL NOT NULL DEFAULT 0.00,
    production_fees_deposit REAL NOT NULL DEFAULT 0.00,
    production_fees_credited REAL NOT NULL DEFAULT 0.00,
    production_fees_debited REAL NOT NULL DEFAULT 0.00,
    production_fees_closing REAL NOT NULL DEFAULT 0.00,
    
    status TEXT NOT NULL DEFAULT 'draft',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
"""

# Index for faster queries
CREATE_REGB_INDEXES = """
CREATE INDEX IF NOT EXISTS idx_regb_fees_date ON regb_production_fees(date);
CREATE INDEX IF NOT EXISTS idx_regb_stock_date ON regb_bottle_stock(date);
CREATE INDEX IF NOT EXISTS idx_regb_summary_date ON regb_daily_summary(date);
CREATE INDEX IF NOT EXISTS idx_regb_stock_product ON regb_bottle_stock(product_name, strength, bottle_size_ml);
"""
