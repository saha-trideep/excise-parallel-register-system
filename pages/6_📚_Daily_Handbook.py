"""
Daily Handbook Generator - Streamlit Interface
Professional PDF handbook generation for SIP2LIFE DISTILLERIES
"""

import streamlit as st
from datetime import date, datetime, timedelta
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from handbook_generator import EnhancedHandbookGenerator

# Page configuration
st.set_page_config(
    page_title="Daily Handbook Generator",
    page_icon="📚",
    layout="wide"
)

# Custom CSS for professional look
st.markdown("""
<style>
    /* Main container */
    .main {
        background: linear-gradient(135deg, #0a0e1a 0%, #1a1f2e 100%);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #4f9eff !important;
        font-weight: 600 !important;
    }
    
    /* Cards */
    .stCard {
        background: linear-gradient(135deg, #1a1f2e 0%, #2a2f3e 100%);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #4f9eff 100%);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(79, 158, 255, 0.4);
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(16, 185, 129, 0.4);
    }
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #1e3a5f 0%, #2a4a7f 100%);
        border-left: 4px solid #4f9eff;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        color: #e8edf5;
    }
    
    .success-box {
        background: linear-gradient(135deg, #1e5f3a 0%, #2a7f4a 100%);
        border-left: 4px solid #10b981;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        color: #e8edf5;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #5f4a1e 0%, #7f6a2a 100%);
        border-left: 4px solid #f59e0b;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        color: #e8edf5;
    }
    
    /* Metrics */
    .metric-card {
        background: linear-gradient(135deg, #1a1f2e 0%, #2a2f3e 100%);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        border: 1px solid #3b82f6;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #4f9eff;
        margin: 10px 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #cbd5e0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #1a1f2e 0%, #2a2f3e 100%); 
            border-radius: 12px; margin-bottom: 30px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);'>
    <h1 style='color: #4f9eff; margin: 0; font-size: 2.5rem;'>📚 Daily Handbook Generator</h1>
    <p style='color: #cbd5e0; margin: 10px 0 0 0; font-size: 1.1rem;'>
        Professional PDF Reports for SIP2LIFE DISTILLERIES PVT. LTD.
    </p>
</div>
""", unsafe_allow_html=True)

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📅 Select Date for Handbook")
    
    # Date selection
    handbook_date = st.date_input(
        "Choose Date",
        value=date.today(),
        max_value=date.today(),
        help="Select the date for which you want to generate the handbook"
    )
    
    # Quick date options
    st.markdown("**Quick Select:**")
    quick_col1, quick_col2, quick_col3 = st.columns(3)
    
    with quick_col1:
        if st.button("📅 Today"):
            handbook_date = date.today()
            st.rerun()
    
    with quick_col2:
        if st.button("📅 Yesterday"):
            handbook_date = date.today() - timedelta(days=1)
            st.rerun()
    
    with quick_col3:
        if st.button("📅 Last Week"):
            handbook_date = date.today() - timedelta(days=7)
            st.rerun()
    
    st.markdown("---")

    # --- SIDEBAR SYSTEM CONTROL ---
    with st.sidebar:
        st.markdown("### 🛠️ System Control")
        if st.button("🔄 System-Wide Sync", help="Pull latest data from all physical registers to update the Handbook summaries", use_container_width=True):
            with st.spinner("Synchronizing all registers..."):
                try:
                    import reg78_backend
                    import regb_backend
                    import excise_duty_backend
                    
                    # 1. Update Reg-78 Synopsis
                    synopsis = reg78_backend.generate_daily_synopsis(handbook_date)
                    if synopsis:
                        synopsis["synopsis_date"] = str(handbook_date)
                        reg78_backend.save_record(synopsis)
                    
                    # 2. Update Reg-B Statistics
                    regb_summary = regb_backend.generate_daily_summary(handbook_date)
                    if regb_summary:
                        regb_backend.save_daily_summary(regb_summary)
                    
                    # 3. Update Excise Duty Summary
                    duty_summary = excise_duty_backend.generate_duty_summary(handbook_date)
                    if duty_summary:
                        excise_duty_backend.save_duty_summary(duty_summary)
                        
                    st.success("✅ System-Wide Sync Complete!")
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"Sync Error: {e}")

        st.divider()
        st.info("""
        **Data Integration Status:**
        - Reg-76-74-A: ✅ CSV
        - Reg-78: ✅ Auto-Fill
        - Reg-B:  ✅ SQLite
        - Duty:   ✅ SQLite
        """)
    # -----------------------------
    
    # Handbook sections info
    st.markdown("### 📋 Handbook Sections")
    
    sections = [
        ("🏭 SST & BRT Details", "Current stock levels in all storage and blending tanks"),
        ("⚙️ Production Detail", "Daily production summary with opening/closing balances"),
        ("🍾 Bottling Line", "Bottle production by size and strength"),
        ("📦 Issued Bottles", "Bottle issuance and inventory tracking"),
        ("💰 Excise Duty", "Duty calculations and financial tracking"),
        ("📊 Production Fees", "Fee calculations from Reg-78")
    ]
    
    for icon_title, description in sections:
        st.markdown(f"""
        <div class='info-box'>
            <strong>{icon_title}</strong><br>
            <small>{description}</small>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("### 🎯 Generate Handbook")
    
    # Display selected date
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>Selected Date</div>
        <div class='metric-value'>{handbook_date.strftime('%d-%m-%Y')}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Generate button
    if st.button("🚀 Generate Handbook V2", type="primary", use_container_width=True):
        with st.spinner("📄 Analyzing all registers and generating professional PDF..."):
            try:
                # AUTOMATION: Sync before generation to ensure accuracy
                import reg78_backend
                syn = reg78_backend.generate_daily_synopsis(handbook_date)
                if syn:
                    syn["synopsis_date"] = str(handbook_date)
                    reg78_backend.save_record(syn)
                
                # Generate handbook
                generator = EnhancedHandbookGenerator(handbook_date)
                output_file = generator.generate_handbook()
                
                # Success message
                st.markdown(f"""
                <div class='success-box'>
                    <strong>✅ Handbook V2 Generated!</strong><br>
                    <small>File: {output_file}</small>
                </div>
                """, unsafe_allow_html=True)
                
                # Store in session state
                st.session_state['generated_file'] = output_file
                st.session_state['generated_date'] = handbook_date
                st.balloons()
                
            except Exception as e:
                st.error(f"❌ Error generating handbook: {str(e)}")
                st.exception(e)
    
    # Download section
    if 'generated_file' in st.session_state and os.path.exists(st.session_state['generated_file']):
        st.markdown("---")
        st.markdown("### 📥 Download Handbook")
        
        # Read file
        with open(st.session_state['generated_file'], 'rb') as f:
            pdf_data = f.read()
        
        # Download button
        st.download_button(
            label="📄 Download PDF",
            data=pdf_data,
            file_name=st.session_state['generated_file'],
            mime="application/pdf",
            use_container_width=True
        )
        
        # File info
        file_size = os.path.getsize(st.session_state['generated_file']) / 1024  # KB
        st.markdown(f"""
        <div class='info-box'>
            <strong>File Information</strong><br>
            <small>Size: {file_size:.2f} KB</small><br>
            <small>Date: {st.session_state['generated_date'].strftime('%d-%m-%Y')}</small>
        </div>
        """, unsafe_allow_html=True)

# Footer section
st.markdown("---")

# Statistics
st.markdown("### 📊 Quick Statistics")

stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

try:
    import pandas as pd
    import os
    
    # Get statistics
    with stat_col1:
        # Total SST/BRT vats
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-label'>Total Vats</div>
            <div class='metric-value'>13</div>
            <small style='color: #cbd5e0;'>6 SST + 7 BRT</small>
        </div>
        """, unsafe_allow_html=True)
    
    with stat_col2:
        # Production records - Read from CSV
        count = 0
        if os.path.exists("rega_data.csv"):
            rega_df = pd.read_csv("rega_data.csv")
            count = len(rega_df)
        
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Production Records</div>
            <div class='metric-value'>{count}</div>
            <small style='color: #cbd5e0;'>Reg-A (CSV)</small>
        </div>
        """, unsafe_allow_html=True)
    
    with stat_col3:
        # Reg-74 operations - Read from CSV
        count = 0
        if os.path.exists("reg74_data.csv"):
            reg74_df = pd.read_csv("reg74_data.csv")
            count = len(reg74_df)
        
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Reg-74 Operations</div>
            <div class='metric-value'>{count}</div>
            <small style='color: #cbd5e0;'>Spirit Operations</small>
        </div>
        """, unsafe_allow_html=True)
    
    with stat_col4:
        # Reg-76 receipts - Read from CSV
        count = 0
        if os.path.exists("reg76_data.csv"):
            reg76_df = pd.read_csv("reg76_data.csv")
            count = len(reg76_df)
        
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Spirit Receipts</div>
            <div class='metric-value'>{count}</div>
            <small style='color: #cbd5e0;'>Reg-76 Records</small>
        </div>
        """, unsafe_allow_html=True)
    
except Exception as e:
    st.warning("⚠️ Unable to load statistics. Database may be empty.")

# Information section
st.markdown("---")
st.markdown("### ℹ️ About Daily Handbook")

info_col1, info_col2 = st.columns(2)

with info_col1:
    st.markdown("""
    <div class='info-box'>
        <strong>📄 Format</strong><br>
        <small>
        • Professional PDF layout<br>
        • Landscape orientation for wide tables<br>
        • Color-coded sections<br>
        • Company branding<br>
        • Date-stamped footer
        </small>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='info-box'>
        <strong>🔄 Data Sources</strong><br>
        <small>
        • Reg-76: Spirit receipts<br>
        • Reg-74: SST/BRT operations<br>
        • Reg-A: Production data<br>
        • Reg-B: Bottle issues<br>
        • Excise Duty: Financial tracking
        </small>
    </div>
    """, unsafe_allow_html=True)

with info_col2:
    st.markdown("""
    <div class='info-box'>
        <strong>✨ Features</strong><br>
        <small>
        • Auto-populated from database<br>
        • Real-time calculations<br>
        • Professional formatting<br>
        • Ready for printing<br>
        • Regulatory compliant
        </small>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='warning-box'>
        <strong>⚠️ Important Notes</strong><br>
        <small>
        • Ensure all registers are updated<br>
        • Verify data before generating<br>
        • Keep PDF for records<br>
        • Review before submission
        </small>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #cbd5e0; padding: 20px;'>
    <p style='margin: 0;'>
        <strong>SIP2LIFE DISTILLERIES PVT. LTD.</strong><br>
        <small>Professional Excise Register Management System</small><br>
        <small>Generated with ❤️ for efficient compliance</small>
    </p>
</div>
""", unsafe_allow_html=True)
