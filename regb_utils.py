"""
Reg-B Utilities - Calculation helpers for bottle stock and production fees
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Tuple

# ============================================================================
# CONSTANTS
# ============================================================================

# Conversion factor: 1 Litre = 1000 ml
ML_PER_LITRE = Decimal("1000")

# ============================================================================
# BOTTLE CONTENT CALCULATIONS
# ============================================================================

def calculate_bl_from_bottles(bottles: int, bottle_size_ml: int) -> Decimal:
    """
    Calculate Bulk Litres (BL) from number of bottles
    
    Formula: BL = (bottles × bottle_size_ml) / 1000
    
    Args:
        bottles: Number of bottles
        bottle_size_ml: Size of each bottle in ml (e.g., 750, 375, 180, 90)
    
    Returns:
        Bulk Litres (BL) rounded to 3 decimal places
    """
    if bottles <= 0 or bottle_size_ml <= 0:
        return Decimal("0.000")
    
    bl = (Decimal(str(bottles)) * Decimal(str(bottle_size_ml))) / ML_PER_LITRE
    return bl.quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)


def calculate_al_from_bl(bl: Decimal, strength: Decimal) -> Decimal:
    """
    Calculate Absolute Litres (AL) from Bulk Litres (BL) and strength
    
    Formula: AL = BL × (strength / 100)
    
    Args:
        bl: Bulk Litres
        strength: Alcohol strength in % v/v (e.g., 22.81, 25.0, 30.0)
    
    Returns:
        Absolute Litres (AL) rounded to 3 decimal places
    """
    if bl <= 0 or strength <= 0:
        return Decimal("0.000")
    
    al = bl * (strength / Decimal("100"))
    return al.quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)


def calculate_al_from_bottles(bottles: int, bottle_size_ml: int, strength: Decimal) -> Decimal:
    """
    Calculate Absolute Litres (AL) directly from bottles
    
    This is a convenience function that combines BL and AL calculation
    
    Args:
        bottles: Number of bottles
        bottle_size_ml: Size of each bottle in ml
        strength: Alcohol strength in % v/v
    
    Returns:
        Absolute Litres (AL) rounded to 3 decimal places
    """
    bl = calculate_bl_from_bottles(bottles, bottle_size_ml)
    return calculate_al_from_bl(bl, strength)


def calculate_bottles_from_bl(bl: Decimal, bottle_size_ml: int) -> int:
    """
    Calculate number of bottles from Bulk Litres (reverse calculation)
    
    Formula: bottles = (BL × 1000) / bottle_size_ml
    
    Args:
        bl: Bulk Litres
        bottle_size_ml: Size of each bottle in ml
    
    Returns:
        Number of bottles (rounded down to nearest integer)
    """
    if bl <= 0 or bottle_size_ml <= 0:
        return 0
    
    bottles = (bl * ML_PER_LITRE) / Decimal(str(bottle_size_ml))
    return int(bottles)


# ============================================================================
# PRODUCTION FEES CALCULATIONS
# ============================================================================

def calculate_production_fees(total_bottles: int, fee_per_bottle: Decimal = Decimal("3.00")) -> Decimal:
    """
    Calculate production fees based on total bottles produced
    
    Formula: Total Fees = total_bottles × fee_per_bottle
    
    Args:
        total_bottles: Total number of bottles produced
        fee_per_bottle: Fee per bottle (default ₹3.00)
    
    Returns:
        Total production fees in ₹ (rounded to 2 decimal places)
    """
    if total_bottles <= 0:
        return Decimal("0.00")
    
    fees = Decimal(str(total_bottles)) * fee_per_bottle
    return fees.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def calculate_fees_balance(opening: Decimal, deposit: Decimal, fees_debited: Decimal) -> Tuple[Decimal, Decimal]:
    """
    Calculate production fees account balance
    
    Args:
        opening: Opening balance in ₹
        deposit: Deposit amount in ₹
        fees_debited: Fees debited for production in ₹
    
    Returns:
        Tuple of (total_credited, closing_balance)
    """
    total_credited = opening + deposit
    closing_balance = total_credited - fees_debited
    
    return (
        total_credited.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
        closing_balance.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    )


# ============================================================================
# BOTTLE STOCK BALANCE CALCULATIONS
# ============================================================================

def calculate_stock_totals(opening_bottles: int, received_bottles: int) -> int:
    """
    Calculate total bottles to be accounted for
    
    Formula: Total = Opening + Received
    
    Args:
        opening_bottles: Opening balance in bottles
        received_bottles: Bottles received from production
    
    Returns:
        Total bottles to be accounted
    """
    return opening_bottles + received_bottles


def calculate_closing_stock(total_accounted: int, wastage: int, issued: int) -> int:
    """
    Calculate closing stock of bottles
    
    Formula: Closing = Total Accounted - Wastage - Issued
    
    Args:
        total_accounted: Total bottles to be accounted
        wastage: Wastage/breakage in bottles
        issued: Bottles issued on payment of duty
    
    Returns:
        Closing balance in bottles
    """
    closing = total_accounted - wastage - issued
    return max(0, closing)  # Ensure non-negative


def calculate_complete_stock_movement(
    opening_bottles: int,
    received_bottles: int,
    wastage_bottles: int,
    issued_bottles: int,
    bottle_size_ml: int,
    strength: Decimal
) -> Dict:
    """
    Calculate complete stock movement with bottles, BL, and AL
    
    This is a comprehensive calculation that returns all stock metrics
    
    Args:
        opening_bottles: Opening balance in bottles
        received_bottles: Bottles received from production
        wastage_bottles: Wastage/breakage in bottles
        issued_bottles: Bottles issued on payment of duty
        bottle_size_ml: Bottle size in ml
        strength: Alcohol strength in % v/v
    
    Returns:
        Dictionary with complete stock movement data
    """
    # Bottle calculations
    total_accounted_bottles = calculate_stock_totals(opening_bottles, received_bottles)
    closing_bottles = calculate_closing_stock(total_accounted_bottles, wastage_bottles, issued_bottles)
    
    # BL calculations
    opening_bl = calculate_bl_from_bottles(opening_bottles, bottle_size_ml)
    received_bl = calculate_bl_from_bottles(received_bottles, bottle_size_ml)
    total_bl = opening_bl + received_bl
    wastage_bl = calculate_bl_from_bottles(wastage_bottles, bottle_size_ml)
    issued_bl = calculate_bl_from_bottles(issued_bottles, bottle_size_ml)
    closing_bl = total_bl - wastage_bl - issued_bl
    
    # AL calculations
    opening_al = calculate_al_from_bl(opening_bl, strength)
    received_al = calculate_al_from_bl(received_bl, strength)
    total_al = opening_al + received_al
    wastage_al = calculate_al_from_bl(wastage_bl, strength)
    issued_al = calculate_al_from_bl(issued_bl, strength)
    closing_al = total_al - wastage_al - issued_al
    
    return {
        # Bottles
        'opening_bottles': opening_bottles,
        'received_bottles': received_bottles,
        'total_accounted_bottles': total_accounted_bottles,
        'wastage_bottles': wastage_bottles,
        'issued_bottles': issued_bottles,
        'closing_bottles': closing_bottles,
        
        # BL
        'opening_bl': opening_bl,
        'received_bl': received_bl,
        'total_bl': total_bl,
        'wastage_bl': wastage_bl,
        'issued_bl': issued_bl,
        'closing_bl': max(Decimal("0.000"), closing_bl),
        
        # AL
        'opening_al': opening_al,
        'received_al': received_al,
        'total_al': total_al,
        'wastage_al': wastage_al,
        'issued_al': issued_al,
        'closing_al': max(Decimal("0.000"), closing_al)
    }


# ============================================================================
# VALIDATION HELPERS
# ============================================================================

def validate_stock_balance(total_accounted: int, wastage: int, issued: int, closing: int) -> bool:
    """
    Validate that stock balance equation is correct
    
    Formula: Total Accounted = Wastage + Issued + Closing
    
    Args:
        total_accounted: Total bottles to be accounted
        wastage: Wastage bottles
        issued: Issued bottles
        closing: Closing balance bottles
    
    Returns:
        True if balance is correct, False otherwise
    """
    return total_accounted == (wastage + issued + closing)


def validate_fees_balance(credited: Decimal, debited: Decimal, closing: Decimal) -> bool:
    """
    Validate that fees balance equation is correct
    
    Formula: Total Credited = Fees Debited + Closing Balance
    
    Args:
        credited: Total amount credited
        debited: Fees debited
        closing: Closing balance
    
    Returns:
        True if balance is correct, False otherwise
    """
    expected_closing = credited - debited
    # Allow for minor rounding differences (within 0.01)
    return abs(closing - expected_closing) < Decimal("0.01")


def calculate_wastage_percentage(wastage_bottles: int, total_accounted: int) -> Decimal:
    """
    Calculate wastage percentage
    
    Formula: Wastage % = (wastage_bottles / total_accounted) × 100
    
    Args:
        wastage_bottles: Number of bottles wasted/broken
        total_accounted: Total bottles accounted for
    
    Returns:
        Wastage percentage (rounded to 2 decimal places)
    """
    if total_accounted <= 0:
        return Decimal("0.00")
    
    percentage = (Decimal(str(wastage_bottles)) / Decimal(str(total_accounted))) * Decimal("100")
    return percentage.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


# ============================================================================
# FORMATTING HELPERS
# ============================================================================

def format_currency(amount: Decimal) -> str:
    """Format amount as Indian currency (₹)"""
    return f"₹{amount:,.2f}"


def format_litres(litres: Decimal, unit: str = "L") -> str:
    """Format litres with 3 decimal places"""
    return f"{litres:.3f} {unit}"


def format_bottles(bottles: int) -> str:
    """Format bottle count with comma separator"""
    return f"{bottles:,} bottles"


def format_percentage(percentage: Decimal) -> str:
    """Format percentage with 2 decimal places"""
    return f"{percentage:.2f}%"


# ============================================================================
# SUMMARY CALCULATIONS
# ============================================================================

def aggregate_multi_product_summary(stock_items: list) -> Dict:
    """
    Aggregate summary across multiple product variants
    
    Args:
        stock_items: List of stock movement dictionaries from calculate_complete_stock_movement
    
    Returns:
        Aggregated summary dictionary
    """
    summary = {
        'total_opening_bottles': 0,
        'total_received_bottles': 0,
        'total_accounted_bottles': 0,
        'total_wastage_bottles': 0,
        'total_issued_bottles': 0,
        'total_closing_bottles': 0,
        'total_opening_bl': Decimal("0.000"),
        'total_received_bl': Decimal("0.000"),
        'total_accounted_bl': Decimal("0.000"),
        'total_wastage_bl': Decimal("0.000"),
        'total_issued_bl': Decimal("0.000"),
        'total_closing_bl': Decimal("0.000"),
        'total_opening_al': Decimal("0.000"),
        'total_received_al': Decimal("0.000"),
        'total_accounted_al': Decimal("0.000"),
        'total_wastage_al': Decimal("0.000"),
        'total_issued_al': Decimal("0.000"),
        'total_closing_al': Decimal("0.000")
    }
    
    for item in stock_items:
        summary['total_opening_bottles'] += item['opening_bottles']
        summary['total_received_bottles'] += item['received_bottles']
        summary['total_accounted_bottles'] += item['total_accounted_bottles']
        summary['total_wastage_bottles'] += item['wastage_bottles']
        summary['total_issued_bottles'] += item['issued_bottles']
        summary['total_closing_bottles'] += item['closing_bottles']
        
        summary['total_opening_bl'] += item['opening_bl']
        summary['total_received_bl'] += item['received_bl']
        summary['total_accounted_bl'] += item['total_bl']
        summary['total_wastage_bl'] += item['wastage_bl']
        summary['total_issued_bl'] += item['issued_bl']
        summary['total_closing_bl'] += item['closing_bl']
        
        summary['total_opening_al'] += item['opening_al']
        summary['total_received_al'] += item['received_al']
        summary['total_accounted_al'] += item['total_al']
        summary['total_wastage_al'] += item['wastage_al']
        summary['total_issued_al'] += item['issued_al']
        summary['total_closing_al'] += item['closing_al']
    
    return summary
