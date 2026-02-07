# Automated Maintenance Data Generator - User Guide

## Overview

The **Automated Maintenance Data Generator** is a powerful feature that automatically creates realistic maintenance activity records for testing and demonstration purposes. This tool is integrated into the Maintenance Log system and can be accessed via the "🤖 Auto Generate" tab.

## Features

### 1. **Smart Data Generation**
- Randomly selects instrument pairs from the complete inventory (E+H instruments, 3rd party valves, PLC/SCADA/HMI)
- Automatically matches activities to instrument types:
  - **Flow instruments (MFM)**: Calibration, zero point checks, heartbeat verifications
  - **Level instruments (RLT, SWITCH)**: Measurement validation, sensor cleaning, troubleshooting
  - **Valves**: PM activities, overhauling, maintenance
  - **Software (PLC, SCADA, HMI)**: Voltage checks, communication checks, database tuning

### 2. **Time Distribution**
- Specify total hours (e.g., 4.0, 4.5, 5.0, 5.5, 6.0, or custom)
- Automatically distributes hours across multiple entries (1-2 hours each)
- Realistic time allocation based on activity complexity

### 3. **Realistic Data**
- Random but appropriate issues and resolutions
- Billing categories (b, c, d)
- Detailed steps for each activity
- Serial numbers for all instruments

## How to Use

### Step 1: Access the Auto Generate Tab
1. Open the Maintenance Log page
2. Click on the "🤖 Auto Generate" tab

### Step 2: Configure Generation Parameters

**Left Column:**
- **Select Date**: Choose the date for maintenance activities (max: today)
- **Select Total Hours**: Choose from predefined options:
  - 4.0 hours
  - 4.5 hours
  - 5.0 hours
  - 5.5 hours
  - 6.0 hours
  - Custom (enter any value between 0.5 and 24.0 hours)

**Right Column:**
- **Technician Name**: Enter the technician name (default: "Trideep Saha")
- **Preview**: See estimated number of entries before generation

### Step 3: Generate Data
1. Review the preview information
2. Click the "🚀 Generate Random Maintenance Data" button
3. Wait for the generation process to complete
4. View the generated entries in the table below

### Step 4: Verify Generated Data
- The system will display all generated entries
- You can switch to the "📊 View Activities" tab to see all maintenance records
- Generated data is stored in the same database as manual entries

## Example Use Cases

### Use Case 1: Testing Monthly Reports
```
Date: 2026-01-01
Hours: 4.5
Technician: Trideep Saha
Result: 3 entries created (1.5h + 1.5h + 1.5h)
```

### Use Case 2: Populating Historical Data
```
Date: 2025-12-15
Hours: 6.0
Technician: Trideep Saha
Result: 4 entries created (1.8h + 1.5h + 1.4h + 1.3h)
```

### Use Case 3: Custom Duration
```
Date: 2026-01-02
Hours: 7.5 (Custom)
Technician: Trideep Saha
Result: 5 entries created
```

## Data Structure

Each generated entry includes:

| Field | Description | Example |
|-------|-------------|---------|
| Date | Selected date | 2026-01-01 |
| Instruments | Random pair with serials | RLT-1 (SB002121133) and MFM-1 (T40C7A02000) |
| Serial Numbers | Comma-separated serials | SB002121133, T40C7A02000 |
| Activity Description | Type-appropriate activity | Routine wet calibration of flowmeters |
| Detailed Steps | Auto-generated description | Performed [activity] on [instruments]; logged results. |
| Time Spent | Distributed hours | 1.5 |
| Technician | Specified technician | Trideep Saha |
| Issues Found | Random issue | Minor corrosion |
| Resolution | Random resolution | Applied coating |
| Billing Category | Random category | b |
| Notes | Random note | Attached logs |

## Technical Details

### Algorithm
1. **Calculate Entries**: `num_entries = max(1, int(total_hours / 1.5))`
2. **Distribute Hours**: Randomly allocate 1-2 hours per entry
3. **Select Instruments**: Random unique pairs from all instruments
4. **Match Activities**: Filter activities by instrument category
5. **Generate Details**: Random issues, resolutions, and notes
6. **Insert to Database**: Use standard `add_maintenance_activity()` function

### Instrument Categories
```python
Flow: MFM-1 to MFM-12
Level: RLT-1 to RLT-28, SWITCH_M1-1IFL, SWITCH_M1-2IML, SWITCH_M2-3IFL, SWITCH_M2-1IML
Valve: Valve (E+H), VALVE_UL1-3, VALVE_ST1-10, VALVE_BV1-17, VALVE_BT1-4, etc.
Software: PLC (Emerson), SCADA, HMI
```

### Activity Pools
- **Flow**: 6 activities (calibration, zero point, heartbeat, etc.)
- **Level**: 8 activities (validation, troubleshooting, cleaning, etc.)
- **Software**: 20 activities (voltage checks, communication, database, etc.)
- **Valve**: 3 activities (PM, overhauling, maintenance)

## Best Practices

### ✅ DO:
- Use for testing PDF generation
- Use for demonstrating the system to clients
- Use for populating historical data during setup
- Verify generated data before using in production

### ❌ DON'T:
- Use in production without review
- Generate data for future dates
- Generate excessive data (keep total hours reasonable)
- Rely solely on auto-generated data for billing

## Troubleshooting

### Issue: "No entries generated"
**Solution**: Check if total hours is at least 0.5

### Issue: "Error generating data"
**Solution**: Verify database connection and permissions

### Issue: "Duplicate instrument pairs"
**Solution**: The system automatically avoids duplicates within the same generation session

## Integration with Existing Features

The auto-generated data:
- ✅ Appears in "View Activities" tab
- ✅ Included in monthly PDF reports
- ✅ Can be deleted using the standard delete function
- ✅ Follows the same schema as manual entries
- ✅ Supports all existing filters and searches

## API Reference

### Function: `auto_populate_maintenance_data()`

```python
def auto_populate_maintenance_data(
    target_date: date,
    total_hours: float,
    technician: str = "Trideep Saha"
) -> Tuple[bool, str, int]:
    """
    Automatically generate and insert random maintenance data
    
    Args:
        target_date: Date for the maintenance activities
        total_hours: Total hours to distribute (e.g., 4.0, 4.5)
        technician: Name of the technician
    
    Returns:
        Tuple of (success, message, number of entries added)
    """
```

### Function: `generate_random_maintenance_entries()`

```python
def generate_random_maintenance_entries(
    target_date: date,
    total_hours: float,
    technician: str = "Trideep Saha"
) -> Tuple[List[MaintenanceActivity], str]:
    """
    Generate random maintenance entries (without inserting to DB)
    
    Args:
        target_date: Date for the maintenance activities
        total_hours: Total hours to distribute
        technician: Name of the technician
    
    Returns:
        Tuple of (list of MaintenanceActivity objects, summary message)
    """
```

## Version History

- **v1.0** (2026-01-01): Initial release
  - Basic random generation
  - Hour distribution
  - Instrument pairing
  - Activity matching

## Support

For issues or questions:
- **Email**: trideep.s@primetech-solutions.in
- **Company**: Endress+Hauser (India) Pvt Ltd.
- **CIN**: U24110MH1999PTC121643

---

**Note**: This feature is designed for testing and demonstration purposes. Always review auto-generated data before using it for official reporting or billing.
