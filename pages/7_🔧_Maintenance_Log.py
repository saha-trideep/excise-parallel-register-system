"""
🔧 Maintenance Log - Daily Activity Tracking & Monthly Reports
E+H Instrument Maintenance System for SIP2LIFE DISTILLERIES
"""

import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta
from maintenance_schema import MaintenanceActivity
from maintenance_backend import (
    add_maintenance_activity,
    get_maintenance_activities,
    get_monthly_summary,
    delete_activity
)
from maintenance_pdf import generate_maintenance_pdf
from maintenance_auto_generator import auto_populate_maintenance_data, generate_maintenance_with_custom_entries

# Page config
st.set_page_config(
    page_title="E+H Maintenance Log",
    page_icon="🔧",
    layout="wide"
)

# Apply custom styling
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stButton>button {
        background: linear-gradient(90deg, #00509E, #00AEEF);
        color: white;
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #003366, #00509E);
        transform: scale(1.05);
    }
    div[data-testid="stMetricValue"] {
        font-size: 28px;
        color: #00509E;
    }
    /* Executive Download Button Styling */
    .stDownloadButton > button {
        background: linear-gradient(90deg, #003366, #00509E) !important;
        color: white !important;
        border: 1px solid #00AEEF !important;
        border-radius: 5px !important;
        text-transform: uppercase;
        font-weight: bold;
        letter-spacing: 1px;
        transition: all 0.3s ease;
    }
    .stDownloadButton > button:hover {
        background: #00AEEF !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0, 80, 158, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🔧 E+H Maintenance Activity Log")
st.markdown("**SIP2LIFE DISTILLERIES PVT. LTD. | Field Service Engineer: Trideep Saha**")
st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📝 Daily Entry", "📊 View Activities", "📄 Monthly Report", "🤖 Auto Generate"])

# ========== TAB 1: DAILY ENTRY ==========
with tab1:
    st.header("Record Daily Maintenance Activity")
    
    col1, col2 = st.columns(2)
    
    with col1:
        activity_date = st.date_input("Date", value=date.today(), max_value=date.today())
        
        # Instrument selection
        st.subheader("Instruments")
        
        # E+H Instruments
        eh_instruments = {
            "RLT-1": "SB002121133", "RLT-2": "SB002221133", "RLT-3": "VB016B21133",
            "MFM-1": "T40C7A02000", "MFM-2": "S401BB02000", "MFM-3": "S401BF02000"
        }
        
        # Third Party Valves
        valves = {
            "VALVE_UL1": "2122-03-79952", "VALVE_UL2": "2122-03-79988",
            "VALVE_ST1": "2122-03-79938", "VALVE_BV1": "2122-03-79960"
        }
        
        instrument_options = list(eh_instruments.keys()) + list(valves.keys()) + ["Other"]
        
        inst1 = st.selectbox("Instrument 1", instrument_options, key="inst1")
        inst2 = st.selectbox("Instrument 2", instrument_options, key="inst2", index=1)
        
        # Get serial numbers
        all_instruments = {**eh_instruments, **valves}
        serial1 = all_instruments.get(inst1, "N/A")
        serial2 = all_instruments.get(inst2, "N/A")
        
        instruments_str = f"{inst1} ({serial1}) and {inst2} ({serial2})"
        serials_str = f"{serial1}, {serial2}"
        
        st.info(f"**Selected:** {instruments_str}")
    
    with col2:
        # Activity selection
        activity_categories = {
            "Flow Calibration": [
                "Routine wet calibration of flowmeters - Annually NABL accreditation (Mandatory)",
                "Zero Point checks",
                "Heartbeat Verifications",
                "Configuration Check",
                "Connected Health Status"
            ],
            "Level Maintenance": [
                "Periodic Measurement Validation",
                "Annual NABL accreditation Calibration (Mandatory)",
                "Configuration Check",
                "Sensor Cleaning",
                "Servicing of Transmitter Housing",
                "Communication loop checks"
            ],
            "Valve Service": [
                "PM activity for CV",
                "Overhauling of CV",
                "Maintenance of CV"
            ],
            "Software/PLC": [
                "DC voltage checkup",
                "PLC communication check",
                "Ethernet network check",
                "SCADA and HMI communication check",
                "Database tuning"
            ]
        }
        
        category = st.selectbox("Activity Category", list(activity_categories.keys()))
        activity_desc = st.selectbox("Activity Description", activity_categories[category])
        
        time_spent = st.number_input("Time Spent (Hours)", min_value=0.1, max_value=24.0, 
                                     value=1.5, step=0.1)
        
        # Issues and resolution
        issues_options = ["None", "Minor corrosion", "Signal noise", "Data mismatch", 
                         "Signal low", "Voltage fluctuation"]
        issues = st.selectbox("Issues Found", issues_options)
        
        resolution_options = ["No action needed", "Applied coating", "Filtered noise", 
                             "Resolved via tuning", "4-20 mA Check", "Supply Check"]
        resolution = st.selectbox("Resolution", resolution_options)
        
        billing_cat = st.selectbox("Billing Category", ["b", "c", "d"])
        
        notes = st.text_area("Additional Notes (Optional)", height=100)
    
    # Detailed steps (auto-generated)
    detailed_steps = f"Performed {activity_desc} on {instruments_str}; logged results."
    
    st.markdown("---")
    
    # Submit button
    if st.button("✅ Submit Activity", type="primary", use_container_width=True):
        activity = MaintenanceActivity(
            date=activity_date,
            instruments=instruments_str,
            serial_numbers=serials_str,
            activity_description=activity_desc,
            detailed_steps=detailed_steps,
            time_spent_hours=time_spent,
            technician="Trideep Saha",
            issues_found=issues,
            resolution=resolution,
            billing_category=billing_cat,
            notes=notes
        )
        
        success, message, activity_id = add_maintenance_activity(activity)
        
        if success:
            st.success(message)
            st.balloons()
        else:
            st.error(message)

# ========== TAB 2: VIEW ACTIVITIES ==========
with tab2:
    st.header("View Maintenance Activities")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        view_start = st.date_input("From Date", value=date.today() - timedelta(days=30))
    with col2:
        view_end = st.date_input("To Date", value=date.today())
    with col3:
        if st.button("🔍 Search", use_container_width=True):
            st.rerun()
    
    # Fetch data
    df = get_maintenance_activities(view_start, view_end)
    
    if not df.empty:
        # Summary metrics
        st.subheader("Summary")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Activities", len(df))
        with col2:
            st.metric("Total Hours", f"{df['time_spent_hours'].sum():.1f}")
        with col3:
            st.metric("Avg Time", f"{df['time_spent_hours'].mean():.1f}h")
        with col4:
            st.metric("Unique Days", df['date'].nunique())
        
        st.markdown("---")
        
        # Display table
        st.subheader("Activity Log")
        
        # Format dataframe
        display_df = df[[
            'date', 'instruments', 'activity_description', 
            'time_spent_hours', 'issues_found', 'resolution'
        ]].copy()
        
        display_df.columns = ['Date', 'Instruments', 'Activity', 'Hours', 'Issues', 'Resolution']
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Date": st.column_config.DateColumn(format="DD-MM-YYYY"),
                "Hours": st.column_config.NumberColumn(format="%.1f"),
            }
        )
        
        # Delete option
        st.markdown("---")
        st.subheader("Delete Activity")
        activity_ids = df['id'].tolist()
        selected_id = st.selectbox("Select Activity ID to Delete", activity_ids)
        
        if st.button("🗑️ Delete Selected", type="secondary"):
            success, message = delete_activity(selected_id)
            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)
    else:
        st.info("No activities found for the selected date range.")

# ========== TAB 3: MONTHLY REPORT ==========
with tab3:
    st.header("Generate Monthly PDF Report")
    
    col1, col2 = st.columns(2)
    
    with col1:
        report_start = st.date_input("Report Start Date", 
                                     value=date.today().replace(day=1))
    with col2:
        report_end = st.date_input("Report End Date", value=date.today())
    
    # Preview metrics
    df_preview = get_maintenance_activities(report_start, report_end)
    
    # Debug info
    st.caption(f"Debug: Fetching data from {report_start} to {report_end} - Found {len(df_preview)} records")
    
    if not df_preview.empty:
        st.subheader("Report Preview")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Activities", len(df_preview))
        with col2:
            st.metric("Total Hours", f"{df_preview['time_spent_hours'].sum():.1f}")
        with col3:
            st.metric("Avg Time", f"{df_preview['time_spent_hours'].mean():.1f}h")
        
        st.markdown("---")
        
        # Generate PDF button
        if st.button("📄 Generate PDF Report", type="primary", use_container_width=True):
            with st.spinner("Generating professional PDF report..."):
                output_path = f"maintenance_report_{report_start}_{report_end}.pdf"
                success, message, pdf_path = generate_maintenance_pdf(
                    report_start, 
                    report_end, 
                    output_path
                )
                
                if success:
                    st.success(message)
                    
                    # Provide download button
                    with open(pdf_path, "rb") as file:
                        st.download_button(
                            label="📥 Download Report",
                            data=file,
                            file_name=output_path,
                            mime="application/pdf",
                            use_container_width=True
                        )
                else:
                    st.error(message)
    else:
        st.warning("No data available for the selected period. Please add activities first.")

# ========== TAB 4: AUTO GENERATE ==========
with tab4:
    st.header("🤖 Automated Maintenance Data Generator")
    
    st.info("""  
    **Auto-populate maintenance data for testing and demonstration purposes.**  
    This feature randomly generates realistic maintenance activities based on actual instruments and SOPs.
    """)
    
    # Mode selection
    generation_mode = st.radio(
        "**Generation Mode:**",
        options=["📊 Total Hours Mode", "🎯 Custom Entries Mode"],
        horizontal=True
    )
    
    st.markdown("---")
    
    if generation_mode == "📊 Total Hours Mode":
        # TOTAL HOURS MODE
        col1, col2 = st.columns(2)
        
        with col1:
            auto_date = st.date_input(
                "Select Date",
                value=date.today(),
                max_value=date.today(),
                key="auto_date_hours"
            )
            
            st.markdown("**Select Total Hours:**")
            
            # Predefined hour options
            hour_options = [
                ("4.0 hours", 4.0),
                ("4.5 hours", 4.5),
                ("5.0 hours", 5.0),
                ("5.5 hours", 5.5),
                ("6.0 hours", 6.0),
                ("Custom", 0)
            ]
            
            hour_choice = st.radio(
                "Hour Selection",
                options=[opt[0] for opt in hour_options],
                index=0,
                label_visibility="collapsed"
            )
            
            # Get selected hours
            selected_hours = next((opt[1] for opt in hour_options if opt[0] == hour_choice), 0)
            
            if hour_choice == "Custom":
                selected_hours = st.number_input(
                    "Enter Custom Hours",
                    min_value=0.5,
                    max_value=24.0,
                    value=4.0,
                    step=0.5
                )
        
        with col2:
            technician_name = st.text_input(
                "Technician Name",
                value="Trideep Saha",
                key="tech_hours"
            )
            
            st.markdown("**Preview:**")
            estimated_entries = max(1, int(selected_hours / 1.5))
            st.info(f"""
            - **Date:** {auto_date.strftime('%d-%m-%Y')}  
            - **Total Hours:** {selected_hours}  
            - **Technician:** {technician_name}  
            - **Estimated Entries:** {estimated_entries}  
            - **Avg Time/Entry:** ~{selected_hours/estimated_entries:.1f}h  
            """)
            
            st.warning("⚠️ This will add random maintenance entries to the database. Use for testing only.")
        
        st.markdown("---")
        
        # Generate button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(
                "🚀 Generate Random Maintenance Data",
                type="primary",
                use_container_width=True,
                key="gen_hours"
            ):
                with st.spinner(f"Generating {selected_hours} hours of maintenance data..."):
                    success, message, count = auto_populate_maintenance_data(
                        auto_date,
                        selected_hours,
                        technician_name
                    )
                    
                    if success:
                        st.success(message)
                        st.balloons()
                        
                        # Show what was generated
                        st.markdown("### Generated Entries:")
                        df_generated = get_maintenance_activities(auto_date, auto_date)
                        
                        if not df_generated.empty:
                            display_df = df_generated[[
                                'instruments', 'activity_description', 
                                'time_spent_hours', 'issues_found'
                            ]].copy()
                            
                            display_df.columns = ['Instruments', 'Activity', 'Hours', 'Issues']
                            
                            st.dataframe(
                                display_df,
                                use_container_width=True,
                                hide_index=True
                            )
                    else:
                        st.error(message)
    
    else:
        # CUSTOM ENTRIES MODE
        col1, col2 = st.columns(2)
        
        with col1:
            auto_date_custom = st.date_input(
                "Select Date",
                value=date.today(),
                max_value=date.today(),
                key="auto_date_custom"
            )
            
            st.markdown("**Number of Entries:**")
            num_entries = st.number_input(
                "How many maintenance entries?",
                min_value=1,
                max_value=20,
                value=3,
                step=1,
                label_visibility="collapsed"
            )
            
            st.markdown("**Time per Entry (Hours):**")
            time_per_entry = st.number_input(
                "Hours for each entry",
                min_value=0.5,
                max_value=8.0,
                value=1.5,
                step=0.5,
                label_visibility="collapsed"
            )
        
        with col2:
            technician_name_custom = st.text_input(
                "Technician Name",
                value="Trideep Saha",
                key="tech_custom"
            )
            
            st.markdown("**Preview:**")
            total_hours_custom = num_entries * time_per_entry
            st.info(f"""
            - **Date:** {auto_date_custom.strftime('%d-%m-%Y')}  
            - **Number of Entries:** {num_entries}  
            - **Time per Entry:** {time_per_entry}h  
            - **Total Hours:** {total_hours_custom}h  
            - **Technician:** {technician_name_custom}  
            """)
            
            st.warning("⚠️ This will add random maintenance entries to the database. Use for testing only.")
        
        st.markdown("---")
        
        # Generate button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(
                "🚀 Generate Custom Maintenance Data",
                type="primary",
                use_container_width=True,
                key="gen_custom"
            ):
                with st.spinner(f"Generating {num_entries} entries..."):
                    success, message, count = generate_maintenance_with_custom_entries(
                        auto_date_custom,
                        num_entries,
                        time_per_entry,
                        technician_name_custom
                    )
                    
                    if success:
                        st.success(message)
                        st.balloons()
                        
                        # Show what was generated
                        st.markdown("### Generated Entries:")
                        df_generated = get_maintenance_activities(auto_date_custom, auto_date_custom)
                        
                        if not df_generated.empty:
                            display_df = df_generated[[
                                'instruments', 'activity_description', 
                                'time_spent_hours', 'issues_found'
                            ]].copy()
                            
                            display_df.columns = ['Instruments', 'Activity', 'Hours', 'Issues']
                            
                            st.dataframe(
                                display_df,
                                use_container_width=True,
                                hide_index=True
                            )
                    else:
                        st.error(message)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p><b>Endress+Hauser (India) Pvt Ltd.</b></p>
        <p>Field Service Engineer: Trideep Saha | Contact: trideep.s@primetech-solutions.in</p>
        <p>CIN: U24110MH1999PTC121643 | Confidential/Internal</p>
    </div>
""", unsafe_allow_html=True)
