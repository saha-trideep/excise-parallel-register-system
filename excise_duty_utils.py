"""
Excise Duty Utilities - Calculation helpers for duty register
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Tuple

from excise_duty_schema import DUTY_RATES, get_duty_rate_for_strength, get_strength_label

# ============================================================================
# DUTY CALCULATIONS
# ============================================================================

def calculate_duty_for_bottles(
    qty_issued: int,
    bottle_size_ml: int,
    strength: Decimal
) -> Dict:
    """
    Calculate complete duty information for issued bottles
    
    Args:
        qty_issued: Number of bottles issued
        bottle_size_ml: Bottle size in ml
        strength: Alcohol strength in % v/v
    
    Returns:
        Dictionary with BL, AL, duty rate, and duty amount
    """
    # Calculate BL
    bl_issued = (Decimal(str(qty_issued)) * Decimal(str(bottle_size_ml))) / Decimal("1000")
    bl_issued = bl_issued.quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)
    
    # Calculate AL
    al_issued = bl_issued * (strength / Decimal("100"))
    al_issued = al_issued.quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)
    
    # Get duty rate
    duty_rate = get_duty_rate_for_strength(strength)
    
    # Calculate duty amount
    duty_amount = bl_issued * duty_rate
    duty_amount = duty_amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    
    return {
        'qty_issued': qty_issued,
        'bl_issued': bl_issued,
        'al_issued': al_issued,
        'duty_rate_per_bl': duty_rate,
        'duty_amount': duty_amount
    }


def calculate_total_duty(bottle_issues: list) -> Decimal:
    """
    Calculate total duty from multiple bottle issues
    
    Args:
        bottle_issues: List of dictionaries with 'duty_amount' key
    
    Returns:
        Total duty amount
    """
    total = sum(Decimal(str(item.get('duty_amount', 0))) for item in bottle_issues)
    return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def calculate_duty_balance(
    opening_balance: Decimal,
    deposit_amount: Decimal,
    duty_debited: Decimal
) -> Tuple[Decimal, Decimal]:
    """
    Calculate duty account balance
    
    Args:
        opening_balance: Opening balance in ₹
        deposit_amount: Deposit made in ₹
        duty_debited: Duty debited in ₹
    
    Returns:
        Tuple of (amount_credited, closing_balance)
    """
    amount_credited = opening_balance + deposit_amount
    closing_balance = amount_credited - duty_debited
    
    return (
        amount_credited.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
        closing_balance.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    )


# ============================================================================
# VALIDATION HELPERS
# ============================================================================

def validate_duty_balance(
    amount_credited: Decimal,
    duty_debited: Decimal,
    closing_balance: Decimal
) -> bool:
    """
    Validate that duty balance equation is correct
    
    Formula: Amount Credited = Duty Debited + Closing Balance
    
    Args:
        amount_credited: Total amount credited
        duty_debited: Duty debited
        closing_balance: Closing balance
    
    Returns:
        True if balance is correct, False otherwise
    """
    expected_closing = amount_credited - duty_debited
    # Allow for minor rounding differences (within 0.01)
    return abs(closing_balance - expected_closing) < Decimal("0.01")


def validate_sufficient_balance(
    amount_credited: Decimal,
    duty_debited: Decimal
) -> bool:
    """
    Validate that there is sufficient balance to cover duty
    
    Args:
        amount_credited: Total amount credited
        duty_debited: Duty to be debited
    
    Returns:
        True if sufficient balance, False otherwise
    """
    return amount_credited >= duty_debited


def validate_duty_calculation(
    bl_issued: Decimal,
    duty_rate: Decimal,
    duty_amount: Decimal
) -> bool:
    """
    Validate that duty calculation is correct
    
    Formula: Duty Amount = BL × Duty Rate
    
    Args:
        bl_issued: BL issued
        duty_rate: Duty rate per BL
        duty_amount: Calculated duty amount
    
    Returns:
        True if calculation is correct, False otherwise
    """
    expected_duty = bl_issued * duty_rate
    expected_duty = expected_duty.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return abs(duty_amount - expected_duty) < Decimal("0.01")


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


def format_duty_rate(rate: Decimal) -> str:
    """Format duty rate"""
    return f"₹{rate:.2f}/BL"


# ============================================================================
# DUTY RATE HELPERS
# ============================================================================

def get_all_duty_rates() -> Dict[str, Decimal]:
    """Get all duty rates with U.P. labels"""
    return {
        "50° U.P. (28.5% v/v)": DUTY_RATES[Decimal("28.5")],
        "60° U.P. (22.8% v/v)": DUTY_RATES[Decimal("22.8")],
        "70° U.P. (17.1% v/v)": DUTY_RATES[Decimal("17.1")],
        "80° U.P. (11.4% v/v)": DUTY_RATES[Decimal("11.4")]
    }


def get_duty_rate_display(strength: Decimal) -> str:
    """Get formatted duty rate display for a strength"""
    rate = get_duty_rate_for_strength(strength)
    label = get_strength_label(strength)
    return f"{label}: {format_duty_rate(rate)}"


# ============================================================================
# SUMMARY CALCULATIONS
# ============================================================================

def aggregate_bottle_summary(bottles: list) -> Dict:
    """
    Aggregate summary across multiple bottle issues
    
    Args:
        bottles: List of bottle issue dictionaries
    
    Returns:
        Aggregated summary dictionary
    """
    summary = {
        'total_qty': 0,
        'total_bl': Decimal("0.000"),
        'total_al': Decimal("0.000"),
        'total_duty': Decimal("0.00")
    }
    
    for bottle in bottles:
        summary['total_qty'] += bottle.get('qty_issued', 0)
        summary['total_bl'] += Decimal(str(bottle.get('bl_issued', 0)))
        summary['total_al'] += Decimal(str(bottle.get('al_issued', 0)))
        summary['total_duty'] += Decimal(str(bottle.get('duty_amount', 0)))
    
    # Round totals
    summary['total_bl'] = summary['total_bl'].quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)
    summary['total_al'] = summary['total_al'].quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)
    summary['total_duty'] = summary['total_duty'].quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    
    return summary


def calculate_duty_by_strength(bottles: list) -> Dict:
    """
    Calculate duty breakdown by strength
    
    Args:
        bottles: List of bottle issue dictionaries
    
    Returns:
        Dictionary with duty breakdown by strength
    """
    breakdown = {}
    
    for bottle in bottles:
        strength = Decimal(str(bottle.get('strength', 0)))
        label = get_strength_label(strength)
        
        if label not in breakdown:
            breakdown[label] = {
                'qty': 0,
                'bl': Decimal("0.000"),
                'al': Decimal("0.000"),
                'duty': Decimal("0.00"),
                'rate': get_duty_rate_for_strength(strength)
            }
        
        breakdown[label]['qty'] += bottle.get('qty_issued', 0)
        breakdown[label]['bl'] += Decimal(str(bottle.get('bl_issued', 0)))
        breakdown[label]['al'] += Decimal(str(bottle.get('al_issued', 0)))
        breakdown[label]['duty'] += Decimal(str(bottle.get('duty_amount', 0)))
    
    # Round all values
    for label in breakdown:
        breakdown[label]['bl'] = breakdown[label]['bl'].quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)
        breakdown[label]['al'] = breakdown[label]['al'].quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)
        breakdown[label]['duty'] = breakdown[label]['duty'].quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    
    return breakdown


def calculate_effective_duty_rate(total_duty: Decimal, total_bl: Decimal) -> Decimal:
    """
    Calculate effective duty rate per BL
    
    Args:
        total_duty: Total duty amount
        total_bl: Total BL issued
    
    Returns:
        Effective duty rate per BL
    """
    if total_bl <= 0:
        return Decimal("0.00")
    
    rate = total_duty / total_bl
    return rate.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


# ============================================================================
# COMPARISON HELPERS
# ============================================================================

def compare_duty_amounts(
    calculated_duty: Decimal,
    expected_duty: Decimal,
    tolerance: Decimal = Decimal("0.01")
) -> Tuple[bool, Decimal]:
    """
    Compare calculated duty with expected duty
    
    Args:
        calculated_duty: Calculated duty amount
        expected_duty: Expected duty amount
        tolerance: Acceptable difference
    
    Returns:
        Tuple of (is_match, difference)
    """
    difference = abs(calculated_duty - expected_duty)
    is_match = difference <= tolerance
    
    return (is_match, difference)


# ============================================================================
# EXPORT HELPERS
# ============================================================================

def format_duty_summary_for_export(summary: Dict) -> str:
    """
    Format duty summary for export/display
    
    Args:
        summary: Summary dictionary
    
    Returns:
        Formatted string
    """
    lines = []
    lines.append("=" * 60)
    lines.append("EXCISE DUTY SUMMARY")
    lines.append("=" * 60)
    lines.append(f"Total Bottles Issued: {format_bottles(summary.get('total_qty', 0))}")
    lines.append(f"Total BL Issued: {format_litres(summary.get('total_bl', Decimal('0.000')), 'BL')}")
    lines.append(f"Total AL Issued: {format_litres(summary.get('total_al', Decimal('0.000')), 'AL')}")
    lines.append(f"Total Duty: {format_currency(summary.get('total_duty', Decimal('0.00')))}")
    lines.append("=" * 60)
    
    return "\n".join(lines)
