"""
Excise Duty Register Backend
Database operations and business logic for excise duty tracking
"""

import sqlite3
from datetime import date, datetime, timedelta
from typing import List, Dict, Optional, Tuple
from decimal import Decimal
import logging

from excise_duty_schema import (
    ExciseDutyLedger,
    ExciseDutyBottle,
    ExciseDutyDailySummary,
    CREATE_EXCISE_DUTY_LEDGER_TABLE,
    CREATE_EXCISE_DUTY_BOTTLES_TABLE,
    CREATE_EXCISE_DUTY_SUMMARY_TABLE,
    CREATE_EXCISE_DUTY_INDEXES,
    DUTY_RATES,
    get_duty_rate_for_strength
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database path
DB_PATH = "excise_registers.db"

# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================

def init_excise_duty_database():
    """Initialize Excise Duty database tables"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Create tables
        cursor.executescript(CREATE_EXCISE_DUTY_LEDGER_TABLE)
        cursor.executescript(CREATE_EXCISE_DUTY_BOTTLES_TABLE)
        cursor.executescript(CREATE_EXCISE_DUTY_SUMMARY_TABLE)
        cursor.executescript(CREATE_EXCISE_DUTY_INDEXES)
        
        conn.commit()
        conn.close()
        logger.info("✅ Excise Duty database initialized successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Error initializing Excise Duty database: {e}")
        return False


# ============================================================================
# DUTY LEDGER OPERATIONS
# ============================================================================

def save_duty_ledger(ledger: ExciseDutyLedger) -> bool:
    """Save or update duty ledger"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        
        # Check if record exists
        cursor.execute("SELECT duty_id FROM excise_duty_ledger WHERE date = ?", (str(ledger.date),))
        existing = cursor.fetchone()
        
        if existing:
            # Update existing record
            cursor.execute("""
                UPDATE excise_duty_ledger SET
                    opening_balance = ?,
                    deposit_amount = ?,
                    echallan_no = ?,
                    echallan_date = ?,
                    amount_credited = ?,
                    name_of_issue = ?,
                    warehouse_no = ?,
                    transport_permit_no = ?,
                    total_duty_amount = ?,
                    duty_debited = ?,
                    closing_balance = ?,
                    remarks = ?,
                    excise_officer_name = ?,
                    excise_officer_signature = ?,
                    status = ?,
                    updated_at = ?
                WHERE date = ?
            """, (
                float(ledger.opening_balance),
                float(ledger.deposit_amount),
                ledger.echallan_no,
                str(ledger.echallan_date) if ledger.echallan_date else None,
                float(ledger.amount_credited),
                ledger.name_of_issue,
                ledger.warehouse_no,
                ledger.transport_permit_no,
                float(ledger.total_duty_amount),
                float(ledger.duty_debited),
                float(ledger.closing_balance),
                ledger.remarks,
                ledger.excise_officer_name,
                ledger.excise_officer_signature,
                ledger.status,
                now,
                str(ledger.date)
            ))
        else:
            # Insert new record
            cursor.execute("""
                INSERT INTO excise_duty_ledger (
                    date, opening_balance, deposit_amount, echallan_no, echallan_date,
                    amount_credited, name_of_issue, warehouse_no, transport_permit_no,
                    total_duty_amount, duty_debited, closing_balance,
                    remarks, excise_officer_name, excise_officer_signature,
                    status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                str(ledger.date),
                float(ledger.opening_balance),
                float(ledger.deposit_amount),
                ledger.echallan_no,
                str(ledger.echallan_date) if ledger.echallan_date else None,
                float(ledger.amount_credited),
                ledger.name_of_issue,
                ledger.warehouse_no,
                ledger.transport_permit_no,
                float(ledger.total_duty_amount),
                float(ledger.duty_debited),
                float(ledger.closing_balance),
                ledger.remarks,
                ledger.excise_officer_name,
                ledger.excise_officer_signature,
                ledger.status,
                now,
                now
            ))
        
        conn.commit()
        conn.close()
        logger.info(f"✅ Duty ledger saved for {ledger.date}")
        return True
    except Exception as e:
        logger.error(f"❌ Error saving duty ledger: {e}")
        return False


def get_duty_ledger(target_date: date) -> Optional[ExciseDutyLedger]:
    """Get duty ledger for a specific date"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM excise_duty_ledger WHERE date = ?", (str(target_date),))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return ExciseDutyLedger(
                duty_id=row['duty_id'],
                date=datetime.strptime(row['date'], '%Y-%m-%d').date(),
                opening_balance=Decimal(str(row['opening_balance'])),
                deposit_amount=Decimal(str(row['deposit_amount'])),
                echallan_no=row['echallan_no'],
                echallan_date=datetime.strptime(row['echallan_date'], '%Y-%m-%d').date() if row['echallan_date'] else None,
                amount_credited=Decimal(str(row['amount_credited'])),
                name_of_issue=row['name_of_issue'],
                warehouse_no=row['warehouse_no'],
                transport_permit_no=row['transport_permit_no'],
                total_duty_amount=Decimal(str(row['total_duty_amount'])),
                duty_debited=Decimal(str(row['duty_debited'])),
                closing_balance=Decimal(str(row['closing_balance'])),
                remarks=row['remarks'],
                excise_officer_name=row['excise_officer_name'],
                excise_officer_signature=row['excise_officer_signature'],
                status=row['status'],
                created_at=datetime.fromisoformat(row['created_at']),
                updated_at=datetime.fromisoformat(row['updated_at'])
            )
        return None
    except Exception as e:
        logger.error(f"❌ Error getting duty ledger: {e}")
        return None


def get_previous_day_duty_closing(target_date: date) -> Decimal:
    """Get previous day's closing balance"""
    try:
        previous_date = target_date - timedelta(days=1)
        ledger = get_duty_ledger(previous_date)
        return ledger.closing_balance if ledger else Decimal("0.00")
    except Exception as e:
        logger.error(f"❌ Error getting previous closing balance: {e}")
        return Decimal("0.00")


# ============================================================================
# BOTTLE ISSUES OPERATIONS
# ============================================================================

def save_duty_bottle(bottle: ExciseDutyBottle) -> bool:
    """Save or update duty bottle issue"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        
        # Check if record exists
        cursor.execute("""
            SELECT duty_bottle_id FROM excise_duty_bottles 
            WHERE date = ? AND product_name = ? AND strength = ? AND bottle_size_ml = ?
        """, (str(bottle.date), bottle.product_name, float(bottle.strength), bottle.bottle_size_ml))
        existing = cursor.fetchone()
        
        if existing:
            # Update existing record
            cursor.execute("""
                UPDATE excise_duty_bottles SET
                    qty_issued = ?,
                    bl_issued = ?,
                    al_issued = ?,
                    duty_rate_per_bl = ?,
                    duty_amount = ?,
                    status = ?,
                    updated_at = ?
                WHERE date = ? AND product_name = ? AND strength = ? AND bottle_size_ml = ?
            """, (
                bottle.qty_issued,
                float(bottle.bl_issued),
                float(bottle.al_issued),
                float(bottle.duty_rate_per_bl),
                float(bottle.duty_amount),
                bottle.status,
                now,
                str(bottle.date),
                bottle.product_name,
                float(bottle.strength),
                bottle.bottle_size_ml
            ))
        else:
            # Insert new record
            cursor.execute("""
                INSERT INTO excise_duty_bottles (
                    duty_id, date, product_name, strength, bottle_size_ml,
                    qty_issued, bl_issued, al_issued,
                    duty_rate_per_bl, duty_amount,
                    status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                bottle.duty_id,
                str(bottle.date),
                bottle.product_name,
                float(bottle.strength),
                bottle.bottle_size_ml,
                bottle.qty_issued,
                float(bottle.bl_issued),
                float(bottle.al_issued),
                float(bottle.duty_rate_per_bl),
                float(bottle.duty_amount),
                bottle.status,
                now,
                now
            ))
        
        conn.commit()
        conn.close()
        logger.info(f"✅ Duty bottle saved for {bottle.date} - {bottle.product_name} ({bottle.bottle_size_ml}ml)")
        return True
    except Exception as e:
        logger.error(f"❌ Error saving duty bottle: {e}")
        return False


def get_duty_bottles_for_date(target_date: date) -> List[ExciseDutyBottle]:
    """Get all duty bottle issues for a specific date"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM excise_duty_bottles WHERE date = ? ORDER BY product_name, bottle_size_ml", (str(target_date),))
        rows = cursor.fetchall()
        conn.close()
        
        bottles = []
        for row in rows:
            bottles.append(ExciseDutyBottle(
                duty_bottle_id=row['duty_bottle_id'],
                duty_id=row['duty_id'],
                date=datetime.strptime(row['date'], '%Y-%m-%d').date(),
                product_name=row['product_name'],
                strength=Decimal(str(row['strength'])),
                bottle_size_ml=row['bottle_size_ml'],
                qty_issued=row['qty_issued'],
                bl_issued=Decimal(str(row['bl_issued'])),
                al_issued=Decimal(str(row['al_issued'])),
                duty_rate_per_bl=Decimal(str(row['duty_rate_per_bl'])),
                duty_amount=Decimal(str(row['duty_amount'])),
                status=row['status'],
                created_at=datetime.fromisoformat(row['created_at']),
                updated_at=datetime.fromisoformat(row['updated_at'])
            ))
        
        return bottles
    except Exception as e:
        logger.error(f"❌ Error getting duty bottles: {e}")
        return []


# ============================================================================
# REG-B INTEGRATION (Auto-fill from issued bottles)
# ============================================================================

def get_regb_issued_bottles(target_date: date) -> List[Dict]:
    """Fetch issued bottles from Reg-B for auto-filling duty register"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get issued bottles from Reg-B
        cursor.execute("""
            SELECT 
                product_name,
                strength,
                bottle_size_ml,
                issue_on_duty_bottles as qty_issued,
                issue_bl,
                issue_al
            FROM regb_bottle_stock
            WHERE date = ? AND issue_on_duty_bottles > 0
            ORDER BY product_name, strength, bottle_size_ml
        """, (str(target_date),))
        
        rows = cursor.fetchall()
        conn.close()
        
        issued_bottles = []
        total_duty = Decimal("0.00")
        
        for row in rows:
            strength = Decimal(str(row['strength']))
            duty_rate = get_duty_rate_for_strength(strength)
            bl_issued = Decimal(str(row['issue_bl']))
            duty_amount = bl_issued * duty_rate
            
            item = {
                'product_name': row['product_name'],
                'strength': strength,
                'bottle_size_ml': row['bottle_size_ml'],
                'qty_issued': row['qty_issued'],
                'bl_issued': bl_issued,
                'al_issued': Decimal(str(row['issue_al'])),
                'duty_rate_per_bl': duty_rate,
                'duty_amount': duty_amount
            }
            issued_bottles.append(item)
            total_duty += duty_amount
        
        return {
            'bottles': issued_bottles,
            'total_duty': total_duty,
            'total_bottles': sum(b['qty_issued'] for b in issued_bottles),
            'total_bl': sum(b['bl_issued'] for b in issued_bottles),
            'total_al': sum(b['al_issued'] for b in issued_bottles)
        }
        
    except Exception as e:
        logger.error(f"❌ Error fetching Reg-B issued bottles: {e}")
        return {
            'bottles': [],
            'total_duty': Decimal("0.00"),
            'total_bottles': 0,
            'total_bl': Decimal("0.000"),
            'total_al': Decimal("0.000")
        }


# ============================================================================
# DAILY SUMMARY OPERATIONS
# ============================================================================

def generate_duty_summary(target_date: date) -> Optional[ExciseDutyDailySummary]:
    """Generate daily summary for excise duty"""
    try:
        # Get ledger
        ledger = get_duty_ledger(target_date)
        
        # Get bottles
        bottles = get_duty_bottles_for_date(target_date)
        
        # Calculate totals
        total_bottles = sum(b.qty_issued for b in bottles)
        total_bl = sum(b.bl_issued for b in bottles)
        total_al = sum(b.al_issued for b in bottles)
        total_duty = sum(b.duty_amount for b in bottles)
        
        summary = ExciseDutyDailySummary(
            date=target_date,
            opening_balance=ledger.opening_balance if ledger else Decimal("0.00"),
            deposit_amount=ledger.deposit_amount if ledger else Decimal("0.00"),
            amount_credited=ledger.amount_credited if ledger else Decimal("0.00"),
            total_duty=total_duty,
            duty_debited=ledger.duty_debited if ledger else Decimal("0.00"),
            closing_balance=ledger.closing_balance if ledger else Decimal("0.00"),
            total_bottles_issued=total_bottles,
            total_bl_issued=total_bl,
            total_al_issued=total_al,
            number_of_issues=1 if ledger and ledger.name_of_issue else 0,
            status=ledger.status if ledger else "draft"
        )
        
        return summary
        
    except Exception as e:
        logger.error(f"❌ Error generating duty summary: {e}")
        return None


def save_duty_summary(summary: ExciseDutyDailySummary) -> bool:
    """Save daily summary to database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        
        # Check if exists
        cursor.execute("SELECT summary_id FROM excise_duty_summary WHERE date = ?", (str(summary.date),))
        existing = cursor.fetchone()
        
        if existing:
            cursor.execute("""
                UPDATE excise_duty_summary SET
                    opening_balance = ?, deposit_amount = ?, amount_credited = ?,
                    total_duty = ?, duty_debited = ?, closing_balance = ?,
                    total_bottles_issued = ?, total_bl_issued = ?, total_al_issued = ?,
                    number_of_issues = ?, status = ?, updated_at = ?
                WHERE date = ?
            """, (
                float(summary.opening_balance), float(summary.deposit_amount), float(summary.amount_credited),
                float(summary.total_duty), float(summary.duty_debited), float(summary.closing_balance),
                summary.total_bottles_issued, float(summary.total_bl_issued), float(summary.total_al_issued),
                summary.number_of_issues, summary.status, now, str(summary.date)
            ))
        else:
            cursor.execute("""
                INSERT INTO excise_duty_summary (
                    date, opening_balance, deposit_amount, amount_credited,
                    total_duty, duty_debited, closing_balance,
                    total_bottles_issued, total_bl_issued, total_al_issued,
                    number_of_issues, status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                str(summary.date),
                float(summary.opening_balance), float(summary.deposit_amount), float(summary.amount_credited),
                float(summary.total_duty), float(summary.duty_debited), float(summary.closing_balance),
                summary.total_bottles_issued, float(summary.total_bl_issued), float(summary.total_al_issued),
                summary.number_of_issues, summary.status, now, now
            ))
        
        conn.commit()
        conn.close()
        logger.info(f"✅ Duty summary saved for {summary.date}")
        return True
    except Exception as e:
        logger.error(f"❌ Error saving duty summary: {e}")
        return False


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def delete_duty_entry(target_date: date) -> bool:
    """Delete all duty entries for a specific date"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM excise_duty_ledger WHERE date = ?", (str(target_date),))
        cursor.execute("DELETE FROM excise_duty_bottles WHERE date = ?", (str(target_date),))
        cursor.execute("DELETE FROM excise_duty_summary WHERE date = ?", (str(target_date),))
        
        conn.commit()
        conn.close()
        logger.info(f"✅ Deleted duty entries for {target_date}")
        return True
    except Exception as e:
        logger.error(f"❌ Error deleting duty entry: {e}")
        return False
