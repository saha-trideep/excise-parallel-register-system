"""
Maintenance Activity Database Schema
Database models for E+H maintenance tracking system
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date

class MaintenanceActivity(BaseModel):
    """Single maintenance activity record"""
    id: Optional[int] = None
    date: date
    instruments: str  # e.g., "RLT-1 (SB002121133) and MFM-1 (T40C7A02000)"
    serial_numbers: str  # e.g., "SB002121133, T40C7A02000"
    activity_description: str
    detailed_steps: str
    time_spent_hours: float = Field(gt=0, le=24)
    technician: str = "Trideep Saha"
    issues_found: Optional[str] = "None"
    resolution: Optional[str] = "No action needed"
    billing_category: str = Field(pattern='^[a-d]$')  # a, b, c, or d
    billing_section: str = "Confidential/Internal"
    notes: Optional[str] = ""
    created_at: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "date": "2026-01-01",
                "instruments": "RLT-1 (SB002121133) and MFM-1 (T40C7A02000)",
                "serial_numbers": "SB002121133, T40C7A02000",
                "activity_description": "Routine wet calibration of flowmeters",
                "detailed_steps": "Performed wet calibration on both instruments; logged results",
                "time_spent_hours": 1.5,
                "technician": "Trideep Saha",
                "issues_found": "Minor corrosion",
                "resolution": "Applied coating",
                "billing_category": "b",
                "notes": "Attached logs"
            }
        }

class MonthlyReport(BaseModel):
    """Monthly maintenance report parameters"""
    start_date: date
    end_date: date
    customer_name: str = "SIP2LIFE DISTILLERIES PVT. LTD."
    customer_hr: str = "Samrat Chatterjee"
    technician: str = "Trideep Saha"
    
