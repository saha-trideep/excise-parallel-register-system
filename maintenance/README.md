# Maintenance Automation System

This module handles daily maintenance tracking and monthly PDF report generation for E+H instruments.

## Files:
- maintenance_schema.py - Database models
- maintenance_backend.py - Database operations
- maintenance_pdf.py - PDF generation
- maintenance_auto_generator.py - Automated random data generation
- ../pages/7_🔧_Maintenance_Log.py - Streamlit UI
- AUTO_GENERATOR_GUIDE.md - User guide for auto-generator feature

## Features:
- ✅ Manual daily activity logging
- ✅ Activity viewing and filtering
- ✅ Monthly PDF report generation
- ✅ **NEW: Automated random data generation for testing**

## Auto-Generator:
The automated maintenance data generator allows you to:
- Select a date and total hours (e.g., 4hr, 4.5hr, 5hr, etc.)
- Automatically generate realistic maintenance activities
- Distribute hours across multiple entries
- Match activities to instrument types
- Perfect for testing and demonstrations

See AUTO_GENERATOR_GUIDE.md for detailed usage instructions.

