"""
Maintenance Activity Backend
Database operations for maintenance tracking
"""

import sqlite3
from datetime import datetime, date
from typing import List, Optional, Tuple
import pandas as pd
from maintenance_schema import MaintenanceActivity

import os

# Use absolute path to ensure database is found regardless of working directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "excise_registers.db")

def init_maintenance_db():
    """Initialize maintenance tables"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS maintenance_activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            instruments TEXT NOT NULL,
            serial_numbers TEXT NOT NULL,
            activity_description TEXT NOT NULL,
            detailed_steps TEXT NOT NULL,
            time_spent_hours REAL NOT NULL,
            technician TEXT NOT NULL,
            issues_found TEXT,
            resolution TEXT,
            billing_category TEXT NOT NULL,
            billing_section TEXT NOT NULL,
            notes TEXT,
            created_at TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()
    return True

def add_maintenance_activity(activity: MaintenanceActivity) -> Tuple[bool, str, int]:
    """Add new maintenance activity"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        created_at = datetime.now().isoformat()
        
        cursor.execute("""
            INSERT INTO maintenance_activities 
            (date, instruments, serial_numbers, activity_description, detailed_steps,
             time_spent_hours, technician, issues_found, resolution, billing_category,
             billing_section, notes, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            activity.date.isoformat(),
            activity.instruments,
            activity.serial_numbers,
            activity.activity_description,
            activity.detailed_steps,
            activity.time_spent_hours,
            activity.technician,
            activity.issues_found,
            activity.resolution,
            activity.billing_category,
            activity.billing_section,
            activity.notes,
            created_at
        ))
        
        activity_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return True, f"✅ Activity recorded successfully! ID: {activity_id}", activity_id
        
    except Exception as e:
        return False, f"❌ Error: {str(e)}", 0

def get_maintenance_activities(start_date: Optional[date] = None, 
                               end_date: Optional[date] = None) -> pd.DataFrame:
    """Get maintenance activities with optional date filtering"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        
        query = "SELECT * FROM maintenance_activities"
        params = []
        
        if start_date and end_date:
            query += " WHERE date BETWEEN ? AND ?"
            params = [start_date.isoformat(), end_date.isoformat()]
        
        query += " ORDER BY date DESC"
        
        df = pd.read_sql_query(query, conn, params=params if params else None)
        conn.close()
        
        if not df.empty:
            df['date'] = pd.to_datetime(df['date']).dt.date
            df['created_at'] = pd.to_datetime(df['created_at'])
        
        return df
        
    except Exception as e:
        print(f"Error fetching activities: {e}")
        return pd.DataFrame()

def get_monthly_summary(year: int, month: int) -> dict:
    """Get monthly maintenance summary statistics"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        
        # Get date range for the month
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)
        
        df = pd.read_sql_query(
            "SELECT * FROM maintenance_activities WHERE date >= ? AND date < ?",
            conn,
            params=[start_date.isoformat(), end_date.isoformat()]
        )
        
        conn.close()
        
        if df.empty:
            return {
                'total_activities': 0,
                'total_hours': 0.0,
                'avg_time': 0.0,
                'unique_days': 0
            }
        
        return {
            'total_activities': len(df),
            'total_hours': df['time_spent_hours'].sum(),
            'avg_time': df['time_spent_hours'].mean(),
            'unique_days': df['date'].nunique()
        }
        
    except Exception as e:
        print(f"Error getting monthly summary: {e}")
        return {'total_activities': 0, 'total_hours': 0.0, 'avg_time': 0.0, 'unique_days': 0}

def delete_activity(activity_id: int) -> Tuple[bool, str]:
    """Delete a maintenance activity"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM maintenance_activities WHERE id = ?", (activity_id,))
        
        if cursor.rowcount == 0:
            conn.close()
            return False, "❌ Activity not found"
        
        conn.commit()
        conn.close()
        return True, "✅ Activity deleted successfully"
        
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

# Initialize on import
print(f"Maintenance Backend: Using database at {DATABASE_PATH}")
init_maintenance_db()
