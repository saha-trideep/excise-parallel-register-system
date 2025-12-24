"""
Reg-B Backend - Issue of Country Liquor in Bottles
Database operations and business logic for finished goods inventory and production fees
"""

import sqlite3
from datetime import date, datetime, timedelta
from typing import List, Dict, Optional, Tuple
from decimal import Decimal
import logging

from regb_schema import (
    ProductionFeesAccount,
    BottleStockInventory,
    RegBDailySummary,
    CREATE_REGB_PRODUCTION_FEES_TABLE,
    CREATE_REGB_BOTTLE_STOCK_TABLE,
    CREATE_REGB_DAILY_SUMMARY_TABLE,
    CREATE_REGB_INDEXES,
    FEE_PER_BOTTLE
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database path
DB_PATH = "excise_registers.db"

# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================

def init_regb_database():
    """Initialize Reg-B database tables"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Create tables
        cursor.executescript(CREATE_REGB_PRODUCTION_FEES_TABLE)
        cursor.executescript(CREATE_REGB_BOTTLE_STOCK_TABLE)
        cursor.executescript(CREATE_REGB_DAILY_SUMMARY_TABLE)
        cursor.executescript(CREATE_REGB_INDEXES)
        
        conn.commit()
        conn.close()
        logger.info("✅ Reg-B database initialized successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Error initializing Reg-B database: {e}")
        return False


# ============================================================================
# PRODUCTION FEES ACCOUNT OPERATIONS
# ============================================================================

def save_production_fees(fees_data: ProductionFeesAccount) -> bool:
    """Save or update production fees account"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        
        # Check if record exists
        cursor.execute("SELECT regb_fees_id FROM regb_production_fees WHERE date = ?", (str(fees_data.date),))
        existing = cursor.fetchone()
        
        if existing:
            # Update existing record
            cursor.execute("""
                UPDATE regb_production_fees SET
                    opening_balance = ?,
                    deposit_amount = ?,
                    echallan_no = ?,
                    echallan_date = ?,
                    total_credited = ?,
                    iml_bottles_qty = ?,
                    total_bottles_produced = ?,
                    fee_per_bottle = ?,
                    total_fees_debited = ?,
                    closing_balance = ?,
                    remarks = ?,
                    excise_officer_name = ?,
                    excise_officer_signature = ?,
                    status = ?,
                    updated_at = ?
                WHERE date = ?
            """, (
                float(fees_data.opening_balance),
                float(fees_data.deposit_amount),
                fees_data.echallan_no,
                str(fees_data.echallan_date) if fees_data.echallan_date else None,
                float(fees_data.total_credited),
                fees_data.iml_bottles_qty,
                fees_data.total_bottles_produced,
                float(fees_data.fee_per_bottle),
                float(fees_data.total_fees_debited),
                float(fees_data.closing_balance),
                fees_data.remarks,
                fees_data.excise_officer_name,
                fees_data.excise_officer_signature,
                fees_data.status,
                now,
                str(fees_data.date)
            ))
        else:
            # Insert new record
            cursor.execute("""
                INSERT INTO regb_production_fees (
                    date, opening_balance, deposit_amount, echallan_no, echallan_date,
                    total_credited, iml_bottles_qty, total_bottles_produced,
                    fee_per_bottle, total_fees_debited, closing_balance,
                    remarks, excise_officer_name, excise_officer_signature,
                    status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                str(fees_data.date),
                float(fees_data.opening_balance),
                float(fees_data.deposit_amount),
                fees_data.echallan_no,
                str(fees_data.echallan_date) if fees_data.echallan_date else None,
                float(fees_data.total_credited),
                fees_data.iml_bottles_qty,
                fees_data.total_bottles_produced,
                float(fees_data.fee_per_bottle),
                float(fees_data.total_fees_debited),
                float(fees_data.closing_balance),
                fees_data.remarks,
                fees_data.excise_officer_name,
                fees_data.excise_officer_signature,
                fees_data.status,
                now,
                now
            ))
        
        conn.commit()
        conn.close()
        logger.info(f"✅ Production fees saved for {fees_data.date}")
        return True
    except Exception as e:
        logger.error(f"❌ Error saving production fees: {e}")
        return False


def get_production_fees(target_date: date) -> Optional[ProductionFeesAccount]:
    """Get production fees account for a specific date"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM regb_production_fees WHERE date = ?", (str(target_date),))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return ProductionFeesAccount(
                regb_fees_id=row['regb_fees_id'],
                date=datetime.strptime(row['date'], '%Y-%m-%d').date(),
                opening_balance=Decimal(str(row['opening_balance'])),
                deposit_amount=Decimal(str(row['deposit_amount'])),
                echallan_no=row['echallan_no'],
                echallan_date=datetime.strptime(row['echallan_date'], '%Y-%m-%d').date() if row['echallan_date'] else None,
                total_credited=Decimal(str(row['total_credited'])),
                iml_bottles_qty=row['iml_bottles_qty'],
                total_bottles_produced=row['total_bottles_produced'],
                fee_per_bottle=Decimal(str(row['fee_per_bottle'])),
                total_fees_debited=Decimal(str(row['total_fees_debited'])),
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
        logger.error(f"❌ Error getting production fees: {e}")
        return None


def get_previous_day_closing_balance(target_date: date) -> Decimal:
    """Get previous day's closing balance for production fees"""
    try:
        previous_date = target_date - timedelta(days=1)
        fees = get_production_fees(previous_date)
        return fees.closing_balance if fees else Decimal("0.00")
    except Exception as e:
        logger.error(f"❌ Error getting previous closing balance: {e}")
        return Decimal("0.00")


# ============================================================================
# BOTTLE STOCK INVENTORY OPERATIONS
# ============================================================================

def save_bottle_stock(stock_data: BottleStockInventory) -> bool:
    """Save or update bottle stock inventory"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        
        # Check if record exists
        cursor.execute("""
            SELECT regb_stock_id FROM regb_bottle_stock 
            WHERE date = ? AND product_name = ? AND strength = ? AND bottle_size_ml = ?
        """, (str(stock_data.date), stock_data.product_name, float(stock_data.strength), stock_data.bottle_size_ml))
        existing = cursor.fetchone()
        
        if existing:
            # Update existing record
            cursor.execute("""
                UPDATE regb_bottle_stock SET
                    opening_balance_bottles = ?,
                    quantity_received_bottles = ?,
                    total_accounted_bottles = ?,
                    wastage_breakage_bottles = ?,
                    issue_on_duty_bottles = ?,
                    closing_balance_bottles = ?,
                    opening_balance_bl = ?,
                    received_bl = ?,
                    total_bl = ?,
                    wastage_bl = ?,
                    issue_bl = ?,
                    closing_bl = ?,
                    opening_balance_al = ?,
                    received_al = ?,
                    total_al = ?,
                    wastage_al = ?,
                    issue_al = ?,
                    closing_al = ?,
                    status = ?,
                    updated_at = ?
                WHERE date = ? AND product_name = ? AND strength = ? AND bottle_size_ml = ?
            """, (
                stock_data.opening_balance_bottles,
                stock_data.quantity_received_bottles,
                stock_data.total_accounted_bottles,
                stock_data.wastage_breakage_bottles,
                stock_data.issue_on_duty_bottles,
                stock_data.closing_balance_bottles,
                float(stock_data.opening_balance_bl),
                float(stock_data.received_bl),
                float(stock_data.total_bl),
                float(stock_data.wastage_bl),
                float(stock_data.issue_bl),
                float(stock_data.closing_bl),
                float(stock_data.opening_balance_al),
                float(stock_data.received_al),
                float(stock_data.total_al),
                float(stock_data.wastage_al),
                float(stock_data.issue_al),
                float(stock_data.closing_al),
                stock_data.status,
                now,
                str(stock_data.date),
                stock_data.product_name,
                float(stock_data.strength),
                stock_data.bottle_size_ml
            ))
        else:
            # Insert new record
            cursor.execute("""
                INSERT INTO regb_bottle_stock (
                    date, product_name, strength, bottle_size_ml,
                    opening_balance_bottles, quantity_received_bottles, total_accounted_bottles,
                    wastage_breakage_bottles, issue_on_duty_bottles, closing_balance_bottles,
                    opening_balance_bl, received_bl, total_bl, wastage_bl, issue_bl, closing_bl,
                    opening_balance_al, received_al, total_al, wastage_al, issue_al, closing_al,
                    status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                str(stock_data.date),
                stock_data.product_name,
                float(stock_data.strength),
                stock_data.bottle_size_ml,
                stock_data.opening_balance_bottles,
                stock_data.quantity_received_bottles,
                stock_data.total_accounted_bottles,
                stock_data.wastage_breakage_bottles,
                stock_data.issue_on_duty_bottles,
                stock_data.closing_balance_bottles,
                float(stock_data.opening_balance_bl),
                float(stock_data.received_bl),
                float(stock_data.total_bl),
                float(stock_data.wastage_bl),
                float(stock_data.issue_bl),
                float(stock_data.closing_bl),
                float(stock_data.opening_balance_al),
                float(stock_data.received_al),
                float(stock_data.total_al),
                float(stock_data.wastage_al),
                float(stock_data.issue_al),
                float(stock_data.closing_al),
                stock_data.status,
                now,
                now
            ))
        
        conn.commit()
        conn.close()
        logger.info(f"✅ Bottle stock saved for {stock_data.date} - {stock_data.product_name} ({stock_data.bottle_size_ml}ml)")
        return True
    except Exception as e:
        logger.error(f"❌ Error saving bottle stock: {e}")
        return False


def get_bottle_stock_for_date(target_date: date) -> List[BottleStockInventory]:
    """Get all bottle stock entries for a specific date"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM regb_bottle_stock WHERE date = ? ORDER BY product_name, bottle_size_ml", (str(target_date),))
        rows = cursor.fetchall()
        conn.close()
        
        stocks = []
        for row in rows:
            stocks.append(BottleStockInventory(
                regb_stock_id=row['regb_stock_id'],
                date=datetime.strptime(row['date'], '%Y-%m-%d').date(),
                product_name=row['product_name'],
                strength=Decimal(str(row['strength'])),
                bottle_size_ml=row['bottle_size_ml'],
                opening_balance_bottles=row['opening_balance_bottles'],
                quantity_received_bottles=row['quantity_received_bottles'],
                total_accounted_bottles=row['total_accounted_bottles'],
                wastage_breakage_bottles=row['wastage_breakage_bottles'],
                issue_on_duty_bottles=row['issue_on_duty_bottles'],
                closing_balance_bottles=row['closing_balance_bottles'],
                opening_balance_bl=Decimal(str(row['opening_balance_bl'])),
                received_bl=Decimal(str(row['received_bl'])),
                total_bl=Decimal(str(row['total_bl'])),
                wastage_bl=Decimal(str(row['wastage_bl'])),
                issue_bl=Decimal(str(row['issue_bl'])),
                closing_bl=Decimal(str(row['closing_bl'])),
                opening_balance_al=Decimal(str(row['opening_balance_al'])),
                received_al=Decimal(str(row['received_al'])),
                total_al=Decimal(str(row['total_al'])),
                wastage_al=Decimal(str(row['wastage_al'])),
                issue_al=Decimal(str(row['issue_al'])),
                closing_al=Decimal(str(row['closing_al'])),
                status=row['status'],
                created_at=datetime.fromisoformat(row['created_at']),
                updated_at=datetime.fromisoformat(row['updated_at'])
            ))
        
        return stocks
    except Exception as e:
        logger.error(f"❌ Error getting bottle stock: {e}")
        return []


def get_previous_day_stock(target_date: date, product_name: str, strength: Decimal, bottle_size_ml: int) -> Optional[BottleStockInventory]:
    """Get previous day's stock for a specific product variant"""
    try:
        previous_date = target_date - timedelta(days=1)
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM regb_bottle_stock 
            WHERE date = ? AND product_name = ? AND strength = ? AND bottle_size_ml = ?
        """, (str(previous_date), product_name, float(strength), bottle_size_ml))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return BottleStockInventory(
                regb_stock_id=row['regb_stock_id'],
                date=datetime.strptime(row['date'], '%Y-%m-%d').date(),
                product_name=row['product_name'],
                strength=Decimal(str(row['strength'])),
                bottle_size_ml=row['bottle_size_ml'],
                opening_balance_bottles=row['opening_balance_bottles'],
                quantity_received_bottles=row['quantity_received_bottles'],
                total_accounted_bottles=row['total_accounted_bottles'],
                wastage_breakage_bottles=row['wastage_breakage_bottles'],
                issue_on_duty_bottles=row['issue_on_duty_bottles'],
                closing_balance_bottles=row['closing_balance_bottles'],
                opening_balance_bl=Decimal(str(row['opening_balance_bl'])),
                received_bl=Decimal(str(row['received_bl'])),
                total_bl=Decimal(str(row['total_bl'])),
                wastage_bl=Decimal(str(row['wastage_bl'])),
                issue_bl=Decimal(str(row['issue_bl'])),
                closing_bl=Decimal(str(row['closing_bl'])),
                opening_balance_al=Decimal(str(row['opening_balance_al'])),
                received_al=Decimal(str(row['received_al'])),
                total_al=Decimal(str(row['total_al'])),
                wastage_al=Decimal(str(row['wastage_al'])),
                issue_al=Decimal(str(row['issue_al'])),
                closing_al=Decimal(str(row['closing_al'])),
                status=row['status']
            )
        return None
    except Exception as e:
        logger.error(f"❌ Error getting previous day stock: {e}")
        return None


# ============================================================================
# REG-A INTEGRATION (Auto-fill from production data)
# ============================================================================

def get_rega_production_data(target_date: date) -> Dict:
    """Fetch production data from Reg-A for auto-filling Reg-B"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get bottling data from Reg-A
        cursor.execute("""
            SELECT 
                product_name,
                strength,
                bottle_size_ml,
                SUM(bottles_produced) as total_bottles,
                SUM(bl_in_bottles) as total_bl,
                SUM(al_in_bottles) as total_al
            FROM rega_bottling_operations
            WHERE date = ?
            GROUP BY product_name, strength, bottle_size_ml
        """, (str(target_date),))
        
        bottling_data = cursor.fetchall()
        conn.close()
        
        production_summary = []
        total_bottles = 0
        
        for row in bottling_data:
            item = {
                'product_name': row['product_name'],
                'strength': Decimal(str(row['strength'])),
                'bottle_size_ml': row['bottle_size_ml'],
                'bottles': row['total_bottles'] or 0,
                'bl': Decimal(str(row['total_bl'] or 0)),
                'al': Decimal(str(row['total_al'] or 0))
            }
            production_summary.append(item)
            total_bottles += item['bottles']
        
        return {
            'production_items': production_summary,
            'total_bottles_produced': total_bottles,
            'production_fees': Decimal(str(total_bottles)) * FEE_PER_BOTTLE
        }
        
    except Exception as e:
        logger.error(f"❌ Error fetching Reg-A production data: {e}")
        return {
            'production_items': [],
            'total_bottles_produced': 0,
            'production_fees': Decimal("0.00")
        }


# ============================================================================
# DAILY SUMMARY OPERATIONS
# ============================================================================

def generate_daily_summary(target_date: date) -> Optional[RegBDailySummary]:
    """Generate consolidated daily summary for Reg-B"""
    try:
        # Get production fees
        fees = get_production_fees(target_date)
        
        # Get all bottle stocks
        stocks = get_bottle_stock_for_date(target_date)
        
        # Aggregate stock data
        summary = RegBDailySummary(
            date=target_date,
            status='draft'
        )
        
        for stock in stocks:
            summary.total_opening_bottles += stock.opening_balance_bottles
            summary.total_received_bottles += stock.quantity_received_bottles
            summary.total_accounted_bottles += stock.total_accounted_bottles
            summary.total_wastage_bottles += stock.wastage_breakage_bottles
            summary.total_issued_bottles += stock.issue_on_duty_bottles
            summary.total_closing_bottles += stock.closing_balance_bottles
            
            summary.total_opening_bl += stock.opening_balance_bl
            summary.total_received_bl += stock.received_bl
            summary.total_accounted_bl += stock.total_bl
            summary.total_wastage_bl += stock.wastage_bl
            summary.total_issued_bl += stock.issue_bl
            summary.total_closing_bl += stock.closing_bl
            
            summary.total_opening_al += stock.opening_balance_al
            summary.total_received_al += stock.received_al
            summary.total_accounted_al += stock.total_al
            summary.total_wastage_al += stock.wastage_al
            summary.total_issued_al += stock.issue_al
            summary.total_closing_al += stock.closing_al
        
        # Add production fees data
        if fees:
            summary.production_fees_opening = fees.opening_balance
            summary.production_fees_deposit = fees.deposit_amount
            summary.production_fees_credited = fees.total_credited
            summary.production_fees_debited = fees.total_fees_debited
            summary.production_fees_closing = fees.closing_balance
            summary.status = fees.status
        
        return summary
        
    except Exception as e:
        logger.error(f"❌ Error generating daily summary: {e}")
        return None


def save_daily_summary(summary: RegBDailySummary) -> bool:
    """Save daily summary to database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        
        # Check if exists
        cursor.execute("SELECT regb_summary_id FROM regb_daily_summary WHERE date = ?", (str(summary.date),))
        existing = cursor.fetchone()
        
        if existing:
            cursor.execute("""
                UPDATE regb_daily_summary SET
                    total_opening_bottles = ?, total_received_bottles = ?, total_accounted_bottles = ?,
                    total_wastage_bottles = ?, total_issued_bottles = ?, total_closing_bottles = ?,
                    total_opening_bl = ?, total_received_bl = ?, total_accounted_bl = ?,
                    total_wastage_bl = ?, total_issued_bl = ?, total_closing_bl = ?,
                    total_opening_al = ?, total_received_al = ?, total_accounted_al = ?,
                    total_wastage_al = ?, total_issued_al = ?, total_closing_al = ?,
                    production_fees_opening = ?, production_fees_deposit = ?, production_fees_credited = ?,
                    production_fees_debited = ?, production_fees_closing = ?,
                    status = ?, updated_at = ?
                WHERE date = ?
            """, (
                summary.total_opening_bottles, summary.total_received_bottles, summary.total_accounted_bottles,
                summary.total_wastage_bottles, summary.total_issued_bottles, summary.total_closing_bottles,
                float(summary.total_opening_bl), float(summary.total_received_bl), float(summary.total_accounted_bl),
                float(summary.total_wastage_bl), float(summary.total_issued_bl), float(summary.total_closing_bl),
                float(summary.total_opening_al), float(summary.total_received_al), float(summary.total_accounted_al),
                float(summary.total_wastage_al), float(summary.total_issued_al), float(summary.total_closing_al),
                float(summary.production_fees_opening), float(summary.production_fees_deposit), float(summary.production_fees_credited),
                float(summary.production_fees_debited), float(summary.production_fees_closing),
                summary.status, now, str(summary.date)
            ))
        else:
            cursor.execute("""
                INSERT INTO regb_daily_summary (
                    date, total_opening_bottles, total_received_bottles, total_accounted_bottles,
                    total_wastage_bottles, total_issued_bottles, total_closing_bottles,
                    total_opening_bl, total_received_bl, total_accounted_bl,
                    total_wastage_bl, total_issued_bl, total_closing_bl,
                    total_opening_al, total_received_al, total_accounted_al,
                    total_wastage_al, total_issued_al, total_closing_al,
                    production_fees_opening, production_fees_deposit, production_fees_credited,
                    production_fees_debited, production_fees_closing,
                    status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                str(summary.date),
                summary.total_opening_bottles, summary.total_received_bottles, summary.total_accounted_bottles,
                summary.total_wastage_bottles, summary.total_issued_bottles, summary.total_closing_bottles,
                float(summary.total_opening_bl), float(summary.total_received_bl), float(summary.total_accounted_bl),
                float(summary.total_wastage_bl), float(summary.total_issued_bl), float(summary.total_closing_bl),
                float(summary.total_opening_al), float(summary.total_received_al), float(summary.total_accounted_al),
                float(summary.total_wastage_al), float(summary.total_issued_al), float(summary.total_closing_al),
                float(summary.production_fees_opening), float(summary.production_fees_deposit), float(summary.production_fees_credited),
                float(summary.production_fees_debited), float(summary.production_fees_closing),
                summary.status, now, now
            ))
        
        conn.commit()
        conn.close()
        logger.info(f"✅ Daily summary saved for {summary.date}")
        return True
    except Exception as e:
        logger.error(f"❌ Error saving daily summary: {e}")
        return False


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_all_product_variants() -> List[Dict]:
    """Get all unique product variants from bottle stock"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT DISTINCT product_name, strength, bottle_size_ml
            FROM regb_bottle_stock
            ORDER BY product_name, strength, bottle_size_ml
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        variants = []
        for row in rows:
            variants.append({
                'product_name': row['product_name'],
                'strength': Decimal(str(row['strength'])),
                'bottle_size_ml': row['bottle_size_ml']
            })
        
        return variants
    except Exception as e:
        logger.error(f"❌ Error getting product variants: {e}")
        return []


def delete_regb_entry(target_date: date) -> bool:
    """Delete all Reg-B entries for a specific date"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM regb_production_fees WHERE date = ?", (str(target_date),))
        cursor.execute("DELETE FROM regb_bottle_stock WHERE date = ?", (str(target_date),))
        cursor.execute("DELETE FROM regb_daily_summary WHERE date = ?", (str(target_date),))
        
        conn.commit()
        conn.close()
        logger.info(f"✅ Deleted Reg-B entries for {target_date}")
        return True
    except Exception as e:
        logger.error(f"❌ Error deleting Reg-B entry: {e}")
        return False
