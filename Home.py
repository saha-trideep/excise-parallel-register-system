import streamlit as st
from auth import login_required

# Page configuration
st.set_page_config(
    page_title="SIP 2 LIFE | Excise System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Password Protection
login_required()

# Custom CSS for Premium Landing Page
st.markdown("""
<style>
    /* Global Styles */
    .main {
        background-color: #0f172a;
    }
    
    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 4rem 2rem;
        border-radius: 20px;
        border-bottom: 5px solid #f4b942;
        text-align: center;
        margin-bottom: 3rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.5);
    }
    
    .hero-title {
        color: #f4b942;
        font-size: 3.5rem;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 0.5rem;
    }
    
    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.2rem;
        font-weight: 400;
    }
    
    /* Portal Cards */
    .portal-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid rgba(244, 185, 66, 0.2);
        transition: all 0.3s ease;
        text-align: center;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .portal-card:hover {
        border: 1px solid #f4b942;
        transform: translateY(-10px);
        box-shadow: 0 15px 30px rgba(244, 185, 66, 0.1);
    }
    
    .portal-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .portal-name {
        color: #f4b942;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .portal-desc {
        color: #94a3b8;
        font-size: 0.9rem;
    }
    
    /* Stats Bar */
    .stats-container {
        display: flex;
        justify-content: space-around;
        background: #1e293b;
        padding: 2rem;
        border-radius: 15px;
        margin-top: 3rem;
    }
    
    .stat-item {
        text-align: center;
    }
    
    .stat-value {
        color: #f4b942;
        font-size: 2rem;
        font-weight: 800;
    }
    
    .stat-label {
        color: #64748b;
        text-transform: uppercase;
        font-size: 0.7rem;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

# Hero Header
st.markdown("""
<div class="hero-section">
    <div class="hero-title">SIP 2 LIFE DISTILLERIES</div>
    <div class="hero-subtitle">Premium Parallel Excise Register Management System</div>
</div>
""", unsafe_allow_html=True)

# Main Navigation Portal
st.markdown("### 🚪 Strategic Register Access")
col1, col2, col3 = st.columns(3)

registers = [
    {"icon": "📋", "name": "Reg-74", "desc": "Spirit Storage & Base Operations", "path": "Reg_74"},
    {"icon": "🏭", "name": "Reg-A", "desc": "Daily Production & MFM2 Tracking", "path": "Reg_A"},
    {"icon": "📦", "name": "Reg-B", "desc": "Finished Stock & Production Fees", "path": "Reg_B"},
    {"icon": "📄", "name": "Reg-76", "desc": "Spirit Receipts & Tanker Logs", "path": "Reg_76"},
    {"icon": "💰", "name": "Excise Duty", "desc": "Financial Ledger & Duty Debits", "path": "Excise_Duty"},
    {"icon": "📚", "name": "Handbook", "desc": "Automated Daily Handbook V2", "path": "Daily_Handbook"}
]

for i in range(0, 3):
    with [col1, col2, col3][i]:
        reg = registers[i]
        st.markdown(f"""
        <div class="portal-card">
            <div class="portal-icon">{reg['icon']}</div>
            <div class="portal-name">{reg['name']}</div>
            <div class="portal-desc">{reg['desc']}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)
for i in range(3, 6):
    with [col4, col5, col6][i-3]:
        reg = registers[i]
        st.markdown(f"""
        <div class="portal-card">
            <div class="portal-icon">{reg['icon']}</div>
            <div class="portal-name">{reg['name']}</div>
            <div class="portal-desc">{reg['desc']}</div>
        </div>
        """, unsafe_allow_html=True)

# System Summary
st.markdown("""
<div class="stats-container">
    <div class="stat-item">
        <div class="stat-value">13</div>
        <div class="stat-label">Tanks Tracked</div>
    </div>
    <div class="stat-item">
        <div class="stat-value">100%</div>
        <div class="stat-label">Data Integration</div>
    </div>
    <div class="stat-item">
        <div class="stat-value">SECURE</div>
        <div class="stat-label">Access Level</div>
    </div>
    <div class="stat-item">
        <div class="stat-value">V2.0</div>
        <div class="stat-label">System Version</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar Info
with st.sidebar:
    st.markdown("### 🛡️ Administration")
    st.success("✅ Logged in as Administrator")
    st.divider()
    st.info("Select a register from the left menu to start operations.")
    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.rerun()

# Footer
st.markdown("""
<div style="text-align: center; color: #475569; padding: 4rem 0 2rem 0;">
    <p style="margin:0;"><strong>SIP 2 LIFE DISTILLERIES PVT. LTD.</strong></p>
    <p style="margin:0; font-size: 0.8rem;">Regulatory Compliance & Parallel Accounting Module</p>
</div>
""", unsafe_allow_html=True)
