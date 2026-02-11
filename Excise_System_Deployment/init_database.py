"""
Database Initialization Script
Initializes all SQLite tables for the Excise Register System
"""

import sqlite3
from pathlib import Path
import desktop_storage

# Import all schema definitions
from reg76_sqlite_schema import CREATE_REG76_TABLE, CREATE_REG76_INDEXES
from reg74_sqlite_schema import CREATE_REG74_TABLE, CREATE_REG74_INDEXES
from rega_sqlite_schema import CREATE_REGA_TABLE, CREATE_REGA_INDEXES
from reg78_sqlite_schema import CREATE_REG78_TABLE, CREATE_REG78_INDEXES
from spirit_transaction_sqlite_schema import (
    CREATE_SPIRIT_TRANSACTION_TABLE,
    CREATE_SPIRIT_TRANSACTION_INDEXES,
)
from regb_schema import (
    CREATE_REGB_PRODUCTION_FEES_TABLE,
    CREATE_REGB_BOTTLE_STOCK_TABLE,
    CREATE_REGB_DAILY_SUMMARY_TABLE,
    CREATE_REGB_INDEXES
)
from excise_duty_schema import (
    CREATE_EXCISE_DUTY_LEDGER_TABLE,
    CREATE_EXCISE_DUTY_BOTTLES_TABLE,
    CREATE_EXCISE_DUTY_SUMMARY_TABLE,
    CREATE_EXCISE_DUTY_INDEXES
)

# Database path
DB_PATH = "excise_registers.db"

def init_all_databases():
    """
    Initialize all database tables for the Excise Register System
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        print("🔧 Initializing Excise Register Database...")
        print(f"📁 Database: {Path(DB_PATH).absolute()}")
        
        # Create Reg-76 tables
        print("\n📊 Creating Reg-76 (Spirit Receipt) tables...")
        cursor.executescript(CREATE_REG76_TABLE)
        cursor.executescript(CREATE_REG76_INDEXES)
        print("✅ Reg-76 tables created")
        
        # Create Reg-74 tables
        print("\n📊 Creating Reg-74 (Spirit Operations) tables...")
        cursor.executescript(CREATE_REG74_TABLE)
        cursor.executescript(CREATE_REG74_INDEXES)
        print("✅ Reg-74 tables created")
        
        # Create Reg-A tables
        print("\n📊 Creating Reg-A (Production) tables...")
        cursor.executescript(CREATE_REGA_TABLE)
        cursor.executescript(CREATE_REGA_INDEXES)
        print("✅ Reg-A tables created")
        
        # Create Reg-78 tables
        print("\n📊 Creating Reg-78 (Daily Synopsis) tables...")
        cursor.executescript(CREATE_REG78_TABLE)
        cursor.executescript(CREATE_REG78_INDEXES)
        print("✅ Reg-78 tables created")

        # Create Spirit Transaction tables
        print("\n📊 Creating Spirit Transaction tables...")
        cursor.executescript(CREATE_SPIRIT_TRANSACTION_TABLE)
        cursor.executescript(CREATE_SPIRIT_TRANSACTION_INDEXES)
        print("✅ Spirit Transaction tables created")
        
        # Create Reg-B tables
        print("\n📊 Creating Reg-B (Finished Goods) tables...")
        cursor.executescript(CREATE_REGB_PRODUCTION_FEES_TABLE)
        cursor.executescript(CREATE_REGB_BOTTLE_STOCK_TABLE)
        cursor.executescript(CREATE_REGB_DAILY_SUMMARY_TABLE)
        cursor.executescript(CREATE_REGB_INDEXES)
        print("✅ Reg-B tables created")
        
        # Create Excise Duty tables
        print("\n📊 Creating Excise Duty tables...")
        cursor.executescript(CREATE_EXCISE_DUTY_LEDGER_TABLE)
        cursor.executescript(CREATE_EXCISE_DUTY_BOTTLES_TABLE)
        cursor.executescript(CREATE_EXCISE_DUTY_SUMMARY_TABLE)
        cursor.executescript(CREATE_EXCISE_DUTY_INDEXES)
        print("✅ Excise Duty tables created")
        
        conn.commit()
        conn.close()
        
        # Initialize Excel files
        desktop_storage.init_all_excel_files()
        
        print("\n" + "="*60)
        print("✅ ALL TABLES INITIALIZED SUCCESSFULLY!")
        print("="*60)
        print("\n📋 Summary:")
        print("  - Reg-76 (Spirit Receipt)")
        print("  - Reg-74 (Spirit Operations)")
        print("  - Reg-A (Production)")
        print("  - Reg-78 (Daily Synopsis)")
        print("  - Spirit Transaction (Daily Summary)")
        print("  - Reg-B (Finished Goods + Production Fees)")
        print("  - Excise Duty (Ledger + Bottles)")
        print("\n🎯 Database ready for use!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error initializing database: {e}")
        import traceback
        traceback.print_exc()
        return False


def verify_tables():
    """
    Verify that all tables were created successfully
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get list of all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        tables = cursor.fetchall()
        
        print("\n📋 Tables in database:")
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
            count = cursor.fetchone()[0]
            print(f"  ✓ {table[0]}: {count} records")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error verifying tables: {e}")
        return False


if __name__ == "__main__":
    print("="*60)
    print("  EXCISE REGISTER SYSTEM - DATABASE INITIALIZATION")
    print("="*60)
    
    success = init_all_databases()
    
    if success:
        verify_tables()
        print("\n✅ Database initialization complete!")
    else:
        print("\n❌ Database initialization failed!")
