import pandas as pd

def calculate_bl(weight_kg, density_gm_cc):
    """Calculate Bulk Liters from Weight (kg) and Density (gm/cc)"""
    if density_gm_cc and density_gm_cc > 0:
        return weight_kg / density_gm_cc
    return 0.0

def calculate_al(bl, strength_perc):
    """Calculate Alcohol Liters from BL and Strength (% v/v)"""
    return bl * (strength_perc / 100)

def calculate_transit_days(dispatch_date, receipt_date):
    """Calculate days in transit"""
    if dispatch_date and receipt_date:
        return (receipt_date - dispatch_date).days
    return 0

def calculate_wastage(advised_al, received_al, allowable_limit=0.0):
    """Calculate transit wastage and chargeable wastage"""
    wastage = max(0.0, advised_al - received_al)
    chargeable = max(0.0, wastage - allowable_limit)
    return wastage, chargeable

def validate_wb(laden, unladen, claimed_net=None):
    """Validate weighbridge data consistency"""
    if laden and unladen:
        net = laden - unladen
        if claimed_net and abs(net - claimed_net) > 50: # Example threshold 50kg
            return False, f"Net weight deviation ({net:.2f}) from claimed ({claimed_net:.2f}) is high."
        return True, "Consistent"
    return True, ""
