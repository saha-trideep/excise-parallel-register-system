"""
Excise Duty Register Schema
Pydantic models and database schema for excise duty tracking on issued bottles
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict
from datetime import date, datetime
from decimal import Decimal

# ============================================================================
# CONSTANTS
# ============================================================================

# Duty rates per BL based on strength (U.P. degrees)
DUTY_RATES = {
    Decimal("28.5"): Decimal("50.00"),  # 50° U.P. → ₹50/BL
    Decimal("22.8"): Decimal("50.00"),  # 60° U.P. → ₹50/BL
    Decimal("17.1"): Decimal("20.00"),  # 70° U.P. → ₹20/BL
    Decimal("11.4"): Decimal("17.00")   # 80° U.P. → ₹17/BL
}

BOTTLE_SIZES_ML = [750, 600, 500, 375, 300, 180]

STRENGTH_OPTIONS = [
    Decimal("28.5"),  # 50° U.P.
    Decimal("22.8"),  # 60° U.P.
    Decimal("17.1"),  # 70° U.P.
    Decimal("11.4")   # 80° U.P.
]

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class ExciseDutyLedger(BaseModel):
    """Model for Excise Duty Ledger (Financial Account)"""
    
    duty_id: Optional[int] = None
    date: date
    
    # Financial Account
    opening_balance: Decimal = Field(default=Decimal("0.00"), ge=0, description="Opening balance in ₹")
    deposit_amount: Decimal = Field(default=Decimal("0.00"), ge=0, description="Deposit made today in ₹")
    echallan_no: Optional[str] = Field(default=None, description="E-Challan number for deposit")
    echallan_date: Optional[date] = Field(default=None, description="E-Challan date")
    amount_credited: Decimal = Field(default=Decimal("0.00"), ge=0, description="Total amount credited")
    
    # Issue Details
    name_of_issue: Optional[str] = Field(default=None, description="Name of customer/distributor")
    warehouse_no: Optional[str] = Field(default=None, description="Warehouse number")
    transport_permit_no: Optional[str] = Field(default=None, description="Transport permit number")
    
    # Duty Calculation
    total_duty_amount: Decimal = Field(default=Decimal("0.00"), ge=0, description="Total duty amount")
    duty_debited: Decimal = Field(default=Decimal("0.00"), ge=0, description="Duty debited for issue")
    closing_balance: Decimal = Field(default=Decimal("0.00"), description="Closing balance")
    
    # Administrative
    remarks: Optional[str] = Field(default=None, description="Remarks")
    excise_officer_name: Optional[str] = Field(default=None, description="Name of excise officer")
    excise_officer_signature: Optional[str] = Field(default=None, description="Digital signature path")
    
    status: str = Field(default="draft", description="Status: draft/submitted")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @field_validator('amount_credited', mode='before')
    @classmethod
    def calculate_amount_credited(cls, v, info):
        """Auto-calculate amount credited"""
        if info.data.get('opening_balance') is not None and info.data.get('deposit_amount') is not None:
            return info.data['opening_balance'] + info.data['deposit_amount']
        return v
    
    @field_validator('closing_balance', mode='before')
    @classmethod
    def calculate_closing_balance(cls, v, info):
        """Auto-calculate closing balance"""
        if info.data.get('amount_credited') is not None and info.data.get('duty_debited') is not None:
            return info.data['amount_credited'] - info.data['duty_debited']
        return v
    
    class Config:
        from_attributes = True


class ExciseDutyBottle(BaseModel):
    """Model for Bottle Issues in Excise Duty Register"""
    
    duty_bottle_id: Optional[int] = None
    duty_id: Optional[int] = None
    date: date
    
    # Product Details
    product_name: str = Field(description="Product name")
    strength: Decimal = Field(description="Strength in % v/v")
    bottle_size_ml: int = Field(description="Bottle size in ml")
    
    # Quantities Issued
    qty_issued: int = Field(default=0, ge=0, description="Quantity of bottles issued")
    bl_issued: Decimal = Field(default=Decimal("0.000"), ge=0, description="BL issued")
    al_issued: Decimal = Field(default=Decimal("0.000"), ge=0, description="AL issued")
    
    # Duty Calculation
    duty_rate_per_bl: Decimal = Field(description="Duty rate per BL in ₹")
    duty_amount: Decimal = Field(default=Decimal("0.00"), ge=0, description="Total duty amount for this product")
    
    status: str = Field(default="draft", description="Status: draft/submitted")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @field_validator('duty_rate_per_bl', mode='before')
    @classmethod
    def get_duty_rate(cls, v, info):
        """Auto-get duty rate based on strength"""
        if v is not None:
            return v
        strength = info.data.get('strength')
        if strength is not None:
            return DUTY_RATES.get(Decimal(str(strength)), Decimal("0.00"))
        return Decimal("0.00")
    
    @field_validator('duty_amount', mode='before')
    @classmethod
    def calculate_duty_amount(cls, v, info):
        """Auto-calculate duty amount"""
        if info.data.get('bl_issued') is not None and info.data.get('duty_rate_per_bl') is not None:
            return info.data['bl_issued'] * info.data['duty_rate_per_bl']
        return v
    
    class Config:
        from_attributes = True


class ExciseDutyDailySummary(BaseModel):
    """Model for Daily Summary of Excise Duty"""
    
    summary_id: Optional[int] = None
    date: date
    
    # Financial Summary
    opening_balance: Decimal = Field(default=Decimal("0.00"), ge=0)
    deposit_amount: Decimal = Field(default=Decimal("0.00"), ge=0)
    amount_credited: Decimal = Field(default=Decimal("0.00"), ge=0)
    total_duty: Decimal = Field(default=Decimal("0.00"), ge=0)
    duty_debited: Decimal = Field(default=Decimal("0.00"), ge=0)
    closing_balance: Decimal = Field(default=Decimal("0.00"))
    
    # Bottle Summary
    total_bottles_issued: int = Field(default=0, ge=0)
    total_bl_issued: Decimal = Field(default=Decimal("0.000"), ge=0)
    total_al_issued: Decimal = Field(default=Decimal("0.000"), ge=0)
    
    # Issue Details
    number_of_issues: int = Field(default=0, ge=0, description="Number of separate issues")
    
    status: str = Field(default="draft")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ============================================================================
# DATABASE SCHEMA (SQLite)
# ============================================================================

CREATE_EXCISE_DUTY_LEDGER_TABLE = """
CREATE TABLE IF NOT EXISTS excise_duty_ledger (
    duty_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL UNIQUE,
    
    -- Financial Account
    opening_balance REAL NOT NULL DEFAULT 0.00,
    deposit_amount REAL NOT NULL DEFAULT 0.00,
    echallan_no TEXT,
    echallan_date TEXT,
    amount_credited REAL NOT NULL DEFAULT 0.00,
    
    -- Issue Details
    name_of_issue TEXT,
    warehouse_no TEXT,
    transport_permit_no TEXT,
    
    -- Duty Calculation
    total_duty_amount REAL NOT NULL DEFAULT 0.00,
    duty_debited REAL NOT NULL DEFAULT 0.00,
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

CREATE_EXCISE_DUTY_BOTTLES_TABLE = """
CREATE TABLE IF NOT EXISTS excise_duty_bottles (
    duty_bottle_id INTEGER PRIMARY KEY AUTOINCREMENT,
    duty_id INTEGER,
    date TEXT NOT NULL,
    
    -- Product Details
    product_name TEXT NOT NULL,
    strength REAL NOT NULL,
    bottle_size_ml INTEGER NOT NULL,
    
    -- Quantities Issued
    qty_issued INTEGER NOT NULL DEFAULT 0,
    bl_issued REAL NOT NULL DEFAULT 0.000,
    al_issued REAL NOT NULL DEFAULT 0.000,
    
    -- Duty Calculation
    duty_rate_per_bl REAL NOT NULL,
    duty_amount REAL NOT NULL DEFAULT 0.00,
    
    status TEXT NOT NULL DEFAULT 'draft',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    
    FOREIGN KEY (duty_id) REFERENCES excise_duty_ledger(duty_id)
);
"""

CREATE_EXCISE_DUTY_SUMMARY_TABLE = """
CREATE TABLE IF NOT EXISTS excise_duty_summary (
    summary_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL UNIQUE,
    
    -- Financial Summary
    opening_balance REAL NOT NULL DEFAULT 0.00,
    deposit_amount REAL NOT NULL DEFAULT 0.00,
    amount_credited REAL NOT NULL DEFAULT 0.00,
    total_duty REAL NOT NULL DEFAULT 0.00,
    duty_debited REAL NOT NULL DEFAULT 0.00,
    closing_balance REAL NOT NULL DEFAULT 0.00,
    
    -- Bottle Summary
    total_bottles_issued INTEGER NOT NULL DEFAULT 0,
    total_bl_issued REAL NOT NULL DEFAULT 0.000,
    total_al_issued REAL NOT NULL DEFAULT 0.000,
    
    -- Issue Details
    number_of_issues INTEGER NOT NULL DEFAULT 0,
    
    status TEXT NOT NULL DEFAULT 'draft',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
"""

# Indexes for faster queries
CREATE_EXCISE_DUTY_INDEXES = """
CREATE INDEX IF NOT EXISTS idx_duty_ledger_date ON excise_duty_ledger(date);
CREATE INDEX IF NOT EXISTS idx_duty_bottles_date ON excise_duty_bottles(date);
CREATE INDEX IF NOT EXISTS idx_duty_bottles_duty_id ON excise_duty_bottles(duty_id);
CREATE INDEX IF NOT EXISTS idx_duty_summary_date ON excise_duty_summary(date);
"""


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_duty_rate_for_strength(strength: Decimal) -> Decimal:
    """Get duty rate per BL for a given strength"""
    return DUTY_RATES.get(strength, Decimal("0.00"))


def get_strength_label(strength: Decimal) -> str:
    """Get U.P. degree label for strength"""
    labels = {
        Decimal("28.5"): "50° U.P.",
        Decimal("22.8"): "60° U.P.",
        Decimal("17.1"): "70° U.P.",
        Decimal("11.4"): "80° U.P."
    }
    return labels.get(strength, f"{strength}% v/v")
