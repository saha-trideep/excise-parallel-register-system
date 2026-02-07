"""
Automated Maintenance Data Generator
Randomly generates maintenance activities for testing and demonstration
"""

import random
from datetime import date, datetime
from typing import List, Tuple
from maintenance_schema import MaintenanceActivity
from maintenance_backend import add_maintenance_activity

# Data buckets
eh_instruments = [
    "RLT-1", "RLT-2", "RLT-3", "RLT-4", "RLT-5", "RLT-6", "RLT-7", "RLT-8", "RLT-9", "RLT-10",
    "RLT-11", "RLT-12", "RLT-13", "RLT-14", "RLT-15", "RLT-16", "RLT-17", "RLT-18", "RLT-19", "RLT-20",
    "RLT-21", "RLT-22", "RLT-23", "RLT-24", "RLT-25", "RLT-26", "RLT-27", "RLT-28",
    "MFM-1", "MFM-2", "MFM-3", "MFM-4", "MFM-5", "MFM-6", "MFM-7", "MFM-8", "MFM-9", "MFM-10", "MFM-11", "MFM-12",
    "Valve", "Valve",
    "SWITCH_M1-1IFL", "SWITCH_M1-1IFL", "SWITCH_M1-2IML", "SWITCH_M1-2IML", "SWITCH_M2-3IFL", "SWITCH_M2-1IML", "SWITCH_M2-1IML"
]
eh_serials = [
    "SB002121133", "SB002221133", "VB016B21133", "VB016C21133", "VB017021133", "SB002021133", "SB001F251133", "VB016F21133",
    "VB016D21133", "VB016E21133", "S4001821133", "S4001121133", "SB001C21133", "SB001E21133", "SB001D21133", "S4000921133",
    "S4001721133", "S4000621133", "S4001921133", "S4001021133", "S4001B21133", "S4001A21133", "S4001521133", "S4000A21133",
    "S4000B21133", "S4001621133", "S4001221133", "S4001C21133", "T40C7A02000", "S401BB02000", "S401BF02000",
    "VA1B3802000", "N.A.", "VA1AFD02000", "N.A.", "VA1B3902000", "S401BC02000", "SA14DF02000",
    "S401BD02000", "SA14E102000", "VA017F9748A", "VA017D9748A", "S4010701026", "S4010601026", "T401F201026",
    "T401F301026", "SB027C01026", "VB01B221191", "VB01B321191"
]

third_party_instruments = [
    "VALVE_UL1", "VALVE_UL2", "VALVE_UL3", "VALVE_ST1", "VALVE_ST2", "VALVE_ST3", "VALVE_ST4", "VALVE_ST1_T",
    "VALVE_ST2_T", "VALVE_ST3_T", "VALVE_ST4_T", "VALVE_BV1", "VALVE_BV2", "VALVE_BV3", "VALVE_BV4", "VALVE_BV5",
    "VALVE_BV6", "VALVE_BV7", "VALVE_BV8", "VALVE_BV9", "VALVE_BV10", "VALVE_BV1", "VALVE_BV2", "VALVE_BV3",
    "VALVE_BV4", "VALVE_BV5", "VALVE_BV6", "VALVE_BV7", "VALVE_BV8", "VALVE_BV9", "VALVE_BV10", "VALVE_BT1",
    "VALVE_ST5", "VALVE_ST6", "VALVE_ST7", "VALVE_ST8", "VALVE_ST9", "VALVE_ST10", "VALVE_ST5_T", "VALVE_ST6_T",
    "VALVE_ST7_T", "VALVE_ST8_T", "VALVE_ST9_T", "VALVE_ST10_T", "VALVE_BV11", "VALVE_BV12", "VALVE_BV13",
    "VALVE_BV14", "VALVE_BV15", "VALVE_BV16", "VALVE_BV17", "VALVE_BV11", "VALVE_BV12", "VALVE_BV13", "VALVE_BV14",
    "VALVE_BV15", "VALVE_BV16", "VALVE_BV17", "VALVE_BT2", "VALVE_BT3", "VALVE_BT4", "VALVE_Trans_MALT",
    "VALVE_Trans_IMFL", "VALVE_Trans_IML", "VALVE_PSSure", "VALVE_PSSure", "VALVE_DM_IMFL", "VALVE_DM_IML"
]
third_party_serials = [
    "2122-03-79952", "2122-03-79988", "2122-03-79974", "2122-03-79938", "2122-03-79951", "2122-03-79975", "2122-03-79969",
    "2122-03-79947", "2122-03-79963", "2122-03-79965", "2023-12-117074", "2122-03-79960", "2122-03-79948", "2122-03-79984",
    "2122-03-79985", "2122-03-79983", "2122-03-79957", "2122-03-79958", "2122-03-79966", "2122-03-79959", "2122-03-79981",
    "2023-12-117077", "2023-12-117076", "2023-12-117071", "2023-12-117075", "2023-12-117067", "2023-12-117072", "2023-12-117079",
    "2023-12-117070", "2023-12-117069", "2023-12-117068", "2023-12-117073", "2122-03-79962", "2122-03-79955", "2122-03-79956",
    "2122-03-79940", "2122-03-79982", "2021-04-58001", "2122-03-79989", "2122-03-79979", "2122-03-79942", "2122-03-79987",
    "2122-03-79991", "2122-03-79954", "2122-03-79976", "2122-03-79967", "2122-03-79937", "2122-03-79941", "2122-03-79971",
    "2122-03-79970", "2122-03-79973", "2122-03-79977", "2122-03-79978", "2122-03-79992", "2122-03-79968", "2122-03-79990",
    "2122-03-79980", "2122-03-79946", "2023-12-117066", "2023-12-117081", "2023-12-117078", "2122-03-79944", "2122-03-79961",
    "2122-03-79986", "VA017E9748A", "71135285", "2122-03-79974", "2122-03-79939"
]
third_party_serials = third_party_serials[:len(third_party_instruments)]

extra_instruments = ["PLC (Emerson)", "SCADA", "HMI"]
extra_serials = ["N/A", "N/A", "N/A"]

all_instruments = (
    list(zip(eh_instruments, eh_serials)) +
    list(zip(third_party_instruments, third_party_serials)) +
    list(zip(extra_instruments, extra_serials))
)

# Categorize activities
flow_activities = [
    "Routine wet calibration of flowmeters- Annually NABL accreditation (Mandatory)",
    "Zero Point checks",
    "Heartbeat Verifications – Run on Demand between Calibration Intervals",
    "Configuration Check",
    "Connected Health Status",
    "Output Communication checks (Pulse integrity)"
]
level_activities = [
    "Periodic Measurement Validation",
    "Annual NABL accreditation Calibration (Mandatory)",
    "Configuration Check",
    "Error Troubleshooting - Hardware related issues",
    "Error Troubleshooting - Process related issues",
    "Sensor Cleaning",
    "Servicing of Transmitter Housing",
    "Communication loop checks"
]
software_activities = [
    "Check outer conditions of plc panel",
    "Raw line voltage measure",
    "Raw neutral to earth voltage measure",
    "Ups line voltage measure",
    "Ups neutral to earth voltage measure",
    "Cleaning of plc panel",
    "Plc module healthiness check",
    "Random IO healthiness check",
    "Individual barrier healthiness check",
    "Dc voltage checkup",
    "Plc communication check",
    "Ethernet network check",
    "Logic response time check",
    "Plc CPU battery condition check",
    "Temporary file clearance from pc",
    "Scada and HMI communication check",
    "Level adjustment between LT and Scada mismatch data (if any)",
    "Backup taken logic and Scada",
    "Database tuning",
    "Periodic performance monitoring and rectification of Historian/SQL"
]
valve_activities = [
    "PM activity for CV",
    "Overhauling of CV",
    "Maintenance of CV"
]

category_to_activities = {
    'flow': flow_activities,
    'level': level_activities,
    'software': software_activities,
    'valve': valve_activities
}

billing_categories = ["b", "c", "d"]
issues = ["None", "Minor corrosion", "Signal noise", "Data mismatch", "Signal low", "Voltage fluctuation"]
resolutions = ["No action needed", "Applied coating", "Filtered noise", "Resolved via tuning", "4-20 mA Check", "Supply Check"]


def get_categories(instrument_name: str) -> List[str]:
    """Get activity categories for an instrument"""
    categories = []
    if 'MFM' in instrument_name:
        categories.append('flow')
    if 'RLT' in instrument_name or 'SWITCH' in instrument_name:
        categories.append('level')
    if 'VALVE' in instrument_name or 'Valve' in instrument_name:
        categories.append('valve')
    if 'PLC' in instrument_name or 'SCADA' in instrument_name or 'HMI' in instrument_name:
        categories.append('software')
    return categories


def generate_random_maintenance_entries(
    target_date: date,
    total_hours: float,
    technician: str = "Trideep Saha"
) -> Tuple[List[MaintenanceActivity], str]:
    """
    Generate random maintenance entries for a given date and total hours
    
    Args:
        target_date: Date for the maintenance activities
        total_hours: Total hours to distribute across activities (e.g., 4.0, 4.5)
        technician: Name of the technician
    
    Returns:
        Tuple of (list of MaintenanceActivity objects, summary message)
    """
    activities = []
    used_pairs = []
    remaining_hours = total_hours
    
    # Calculate number of entries (each 1-2 hours)
    num_entries = max(1, int(total_hours / 1.5))
    
    # Distribute hours across entries
    hours_per_entry = []
    for i in range(num_entries):
        if i == num_entries - 1:
            # Last entry gets remaining hours
            hours_per_entry.append(round(remaining_hours, 1))
        else:
            # Random hours between 1-2
            hours = round(random.uniform(1.0, min(2.0, remaining_hours - (num_entries - i - 1))), 1)
            hours_per_entry.append(hours)
            remaining_hours -= hours
    
    for time_spent in hours_per_entry:
        # Select unique instrument pair
        while True:
            pair = random.sample(all_instruments, 2)
            pair_tuple = (pair[0][0], pair[0][1], pair[1][0], pair[1][1])
            if pair_tuple not in used_pairs:
                break
        used_pairs.append(pair_tuple)
        
        inst1, ser1 = pair[0]
        inst2, ser2 = pair[1]
        instruments_str = f"{inst1} ({ser1}) and {inst2} ({ser2})"
        serials_str = f"{ser1}, {ser2}"
        
        # Get compatible activities based on instrument types
        cats1 = get_categories(inst1)
        cats2 = get_categories(inst2)
        all_cats = set(cats1 + cats2)
        
        possible_activities = []
        for cat in all_cats:
            possible_activities.extend(category_to_activities.get(cat, []))
        
        if not possible_activities:
            # Fallback to all activities
            possible_activities = (flow_activities + level_activities + 
                                 software_activities + valve_activities)
        
        activity_desc = random.choice(possible_activities)
        detailed_steps = f"Performed {activity_desc} on {instruments_str}; logged results."
        
        # Random other fields
        issue = random.choice(issues)
        resolution = random.choice(resolutions)
        billing_cat = random.choice(billing_categories)
        notes = random.choice(["", "Attached logs", "No downtime"])
        
        # Create MaintenanceActivity object
        activity = MaintenanceActivity(
            date=target_date,
            instruments=instruments_str,
            serial_numbers=serials_str,
            activity_description=activity_desc,
            detailed_steps=detailed_steps,
            time_spent_hours=time_spent,
            technician=technician,
            issues_found=issue,
            resolution=resolution,
            billing_category=billing_cat,
            notes=notes
        )
        
        activities.append(activity)
    
    summary = f"Generated {len(activities)} maintenance entries for {target_date} totaling {total_hours} hours"
    return activities, summary


def auto_populate_maintenance_data(
    target_date: date,
    total_hours: float,
    technician: str = "Trideep Saha"
) -> Tuple[bool, str, int]:
    """
    Automatically generate and insert random maintenance data into database
    
    Args:
        target_date: Date for the maintenance activities
        total_hours: Total hours to distribute (e.g., 4.0, 4.5)
        technician: Name of the technician
    
    Returns:
        Tuple of (success, message, number of entries added)
    """
    try:
        activities, summary = generate_random_maintenance_entries(
            target_date, total_hours, technician
        )
        
        success_count = 0
        for activity in activities:
            success, msg, activity_id = add_maintenance_activity(activity)
            if success:
                success_count += 1
        
        if success_count == len(activities):
            return True, f"✅ {summary}. All entries added successfully!", success_count
        else:
            return False, f"⚠️ Only {success_count}/{len(activities)} entries added successfully", success_count
            
    except Exception as e:
        return False, f"Error generating data: {str(e)}", 0


def generate_maintenance_with_custom_entries(
    target_date: date,
    num_entries: int,
    time_per_entry: float,
    technician: str = "Trideep Saha"
) -> Tuple[bool, str, int]:
    """
    Generate maintenance entries with specific number of entries and time per entry
    
    Args:
        target_date: Date for the maintenance activities
        num_entries: Number of entries to generate (e.g., 3, 4, 5)
        time_per_entry: Hours per entry (e.g., 1.0, 1.5, 2.0)
        technician: Name of the technician
    
    Returns:
        Tuple of (success, message, number of entries added)
    """
    try:
        activities = []
        used_pairs = []
        
        for i in range(num_entries):
            # Select unique instrument pair
            while True:
                pair = random.sample(all_instruments, 2)
                pair_tuple = (pair[0][0], pair[0][1], pair[1][0], pair[1][1])
                if pair_tuple not in used_pairs:
                    break
            used_pairs.append(pair_tuple)
            
            inst1, ser1 = pair[0]
            inst2, ser2 = pair[1]
            instruments_str = f"{inst1} ({ser1}) and {inst2} ({ser2})"
            serials_str = f"{ser1}, {ser2}"
            
            # Get compatible activities based on instrument types
            cats1 = get_categories(inst1)
            cats2 = get_categories(inst2)
            all_cats = set(cats1 + cats2)
            
            possible_activities = []
            for cat in all_cats:
                possible_activities.extend(category_to_activities.get(cat, []))
            
            if not possible_activities:
                # Fallback to all activities
                possible_activities = (flow_activities + level_activities + 
                                     software_activities + valve_activities)
            
            activity_desc = random.choice(possible_activities)
            detailed_steps = f"Performed {activity_desc} on {instruments_str}; logged results."
            
            # Random other fields
            issue = random.choice(issues)
            resolution = random.choice(resolutions)
            billing_cat = random.choice(billing_categories)
            notes = random.choice(["", "Attached logs", "No downtime"])
            
            # Create MaintenanceActivity object
            activity = MaintenanceActivity(
                date=target_date,
                instruments=instruments_str,
                serial_numbers=serials_str,
                activity_description=activity_desc,
                detailed_steps=detailed_steps,
                time_spent_hours=time_per_entry,
                technician=technician,
                issues_found=issue,
                resolution=resolution,
                billing_category=billing_cat,
                notes=notes
            )
            
            activities.append(activity)
        
        # Insert to database
        success_count = 0
        for activity in activities:
            success, msg, activity_id = add_maintenance_activity(activity)
            if success:
                success_count += 1
        
        total_hours = num_entries * time_per_entry
        
        if success_count == len(activities):
            return True, f"Generated {num_entries} entries ({time_per_entry}h each, {total_hours}h total). All added successfully!", success_count
        else:
            return False, f"Only {success_count}/{num_entries} entries added successfully", success_count
            
    except Exception as e:
        return False, f"Error generating data: {str(e)}", 0



if __name__ == "__main__":
    # Test the generator
    test_date = date.today()
    test_hours = 4.5
    
    success, message, count = auto_populate_maintenance_data(test_date, test_hours)
    print(message)
