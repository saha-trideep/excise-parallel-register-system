# 🤖 Auto-Generator Quick Reference

## Quick Start (3 Steps)

### 1️⃣ Open the Auto Generate Tab
Navigate to: **Maintenance Log → 🤖 Auto Generate**

### 2️⃣ Select Parameters
```
📅 Date:  [Select date]
⏱️ Hours: [4.0 | 4.5 | 5.0 | 5.5 | 6.0 | Custom]
👤 Tech:  [Trideep Saha]
```

### 3️⃣ Click Generate
Click **🚀 Generate Random Maintenance Data**

---

## Hour Options

| Option | Entries | Example Distribution |
|--------|---------|---------------------|
| 4.0 hr | 2-3 | 1.5h + 1.5h + 1.0h |
| 4.5 hr | 3 | 1.5h + 1.5h + 1.5h |
| 5.0 hr | 3-4 | 1.8h + 1.5h + 1.7h |
| 5.5 hr | 3-4 | 1.5h + 1.8h + 1.2h + 1.0h |
| 6.0 hr | 4 | 1.5h + 1.5h + 1.5h + 1.5h |
| Custom | Variable | Based on input |

---

## What Gets Generated

✅ **Random instrument pairs** (E+H + 3rd party)  
✅ **Type-appropriate activities** (Flow/Level/Valve/Software)  
✅ **Realistic issues & resolutions**  
✅ **Proper serial numbers**  
✅ **Billing categories** (b, c, d)  
✅ **Detailed steps**  

---

## Example Output

```
Date: 2026-01-01
Total Hours: 4.5

Entry 1:
  Instruments: RLT-1 (SB002121133) and MFM-1 (T40C7A02000)
  Activity: Routine wet calibration of flowmeters
  Time: 1.5 hours
  Issue: Minor corrosion
  Resolution: Applied coating

Entry 2:
  Instruments: VALVE_UL1 (2122-03-79952) and SCADA (N/A)
  Activity: PM activity for CV
  Time: 1.5 hours
  Issue: None
  Resolution: No action needed

Entry 3:
  Instruments: RLT-15 (SB001D21133) and VALVE_ST1 (2122-03-79938)
  Activity: Sensor Cleaning
  Time: 1.5 hours
  Issue: Signal noise
  Resolution: Filtered noise
```

---

## Common Scenarios

### 📊 Testing Monthly Reports
```
Date: First day of month
Hours: 4.5
Purpose: Generate sample data for PDF testing
```

### 🎯 Demo for Client
```
Date: Today
Hours: 5.0
Purpose: Show realistic maintenance activities
```

### 📈 Populate Historical Data
```
Date: Past date
Hours: 4.0 to 6.0
Purpose: Fill in missing historical records
```

---

## Tips & Tricks

💡 **Tip 1**: Use 4.5 hours for standard daily work  
💡 **Tip 2**: Custom hours for special scenarios  
💡 **Tip 3**: Check "View Activities" tab after generation  
💡 **Tip 4**: Generated data can be deleted if needed  
💡 **Tip 5**: Use for testing, verify before production use  

---

## Instrument Types

| Type | Count | Examples |
|------|-------|----------|
| Flow (MFM) | 12 | MFM-1 to MFM-12 |
| Level (RLT) | 28 | RLT-1 to RLT-28 |
| Switches | 7 | SWITCH_M1-1IFL, etc. |
| Valves | 66 | VALVE_UL1, VALVE_ST1, etc. |
| Software | 3 | PLC, SCADA, HMI |

**Total: 116 instruments**

---

## Activity Categories

### 🌊 Flow (6 activities)
- Routine wet calibration
- Zero Point checks
- Heartbeat Verifications
- Configuration Check
- Connected Health Status
- Output Communication checks

### 📏 Level (8 activities)
- Periodic Measurement Validation
- Annual NABL calibration
- Configuration Check
- Error Troubleshooting (Hardware/Process)
- Sensor Cleaning
- Servicing of Transmitter Housing
- Communication loop checks

### 🔧 Valve (3 activities)
- PM activity for CV
- Overhauling of CV
- Maintenance of CV

### 💻 Software (20 activities)
- Voltage checks (Raw, UPS, DC)
- PLC health checks
- Communication checks
- Database tuning
- And more...

---

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Switch tabs | `Ctrl + Tab` |
| Refresh page | `F5` |
| Focus search | `Ctrl + F` |

---

## Troubleshooting

❌ **Problem**: No entries generated  
✅ **Solution**: Ensure hours ≥ 0.5

❌ **Problem**: Error message  
✅ **Solution**: Check database connection

❌ **Problem**: Wrong date  
✅ **Solution**: Date must be ≤ today

---

## Remember

⚠️ **This is for TESTING only**  
✅ Always review generated data  
✅ Use "View Activities" to verify  
✅ Can be deleted if needed  
✅ Follows same schema as manual entries  

---

**For detailed documentation, see AUTO_GENERATOR_GUIDE.md**
