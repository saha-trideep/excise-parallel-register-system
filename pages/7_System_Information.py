import streamlit as st
from auth import login_required

# Apply Authentication
login_required()

import os
import base64

# Page Configuration
st.set_page_config(
    page_title="System Information & Documentation",
    page_icon="ℹ️",
    layout="wide"
)

# Custom CSS for Premium Look
st.markdown("""
<style>
    .documentation-card {
        background: linear-gradient(135deg, #1a1f2e 0%, #2a2f3e 100%);
        padding: 25px;
        border-radius: 15px;
        border-left: 5px solid #f4b942;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .doc-title {
        color: #f4b942;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 10px;
    }
    .doc-description {
        color: #cbd5e0;
        margin-bottom: 20px;
    }
    .stDownloadButton button {
        background: linear-gradient(135deg, #f4b942 0%, #d4a017 100%) !important;
        color: #1a1f2e !important;
        font-weight: 700 !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #1a1f2e 0%, #2a2f3e 100%); 
            border-radius: 12px; margin-bottom: 30px; border-bottom: 4px solid #f4b942;'>
    <h1 style='color: #f4b942; margin: 0;'>ℹ️ System Documentation</h1>
    <p style='color: #cbd5e0; margin: 10px 0 0 0;'>Technical Flowcharts & Database Architecture</p>
</div>
""", unsafe_allow_html=True)

# System Flowchart Card
st.markdown('<div class="documentation-card">', unsafe_allow_html=True)
st.markdown('<div class="doc-title">🗺️ System Automation Flowchart</div>', unsafe_allow_html=True)
st.markdown("""
<p class="doc-description">
    Visualize the <b>"Ripple Effect"</b> automation. See how data moves from 
    Reg-74 (Base Source) through Production, Inventory, and finally to the 
    Excise Duty financials.
</p>
""", unsafe_allow_html=True)

file_path = "System_Flowchart.pdf"
if os.path.exists(file_path):
    with open(file_path, "rb") as f:
        pdf_bytes = f.read()
    st.download_button(
        label="📥 Download System Flowchart PDF",
        data=pdf_bytes,
        file_name="System_Flowchart_Automation.pdf",
        mime="application/pdf",
        use_container_width=True
    )
else:
    st.error("⚠️ System Flowchart PDF not found. Please generate it first.")
st.markdown('</div>', unsafe_allow_html=True)

# Full System Overview Text
st.markdown("---")
st.markdown("### 💡 About the Integrated System")
st.info("""
The Excise Parallel Register System is designed as a **Cohesive Ecosystem** engineered by **Endress+Hauser**. 
- **Digitalization:** Powered by E+H flow measurement technology and automation expertise.
- **Business Partnership:** Developed in close collaboration with **SIP 2 LIFE Distilleries Pvt. Ltd.**
- **Base Register (Reg-74):** The starting point for all spirit movement.
- **Automation Chain:** Entry in one register triggers placeholders and updates in the next.
- **Data Integrity:** Combines the speed of CSV for operations with the security of SQLite for financial records.
""")

# Footer
st.markdown("""
<div style='text-align: center; color: #718096; padding: 20px; font-size: 0.8rem;'>
    SIP2LIFE DISTILLERIES PVT. LTD. • System Documentation v2.0 • Antigravity AI
</div>
""", unsafe_allow_html=True)
