"""
Excise Parallel Register System - Main Application
Landing page with navigation to all registers
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Excise Parallel Register System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    /* Main header */
    .main-header {
        background: linear-gradient(135deg, #7c3aed 0%, #2563eb 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(124, 58, 237, 0.4);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.95;
    }
    
    /* Section headers */
    .section-header {
        background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%);
        padding: 1rem 1.5rem;
        border-radius: 8px;
        color: white;
        margin: 1.5rem 0 1rem 0;
        font-size: 1.3rem;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(124, 58, 237, 0.3);
    }
    
    /* Info boxes */
    .info-box {
        background: rgba(59, 130, 246, 0.1);
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
        color: #e0e7ff;
    }
    
    .success-box {
        background: rgba(34, 197, 94, 0.1);
        border-left: 4px solid #22c55e;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
        color: #d1fae5;
    }
    
    .warning-box {
        background: rgba(251, 146, 60, 0.1);
        border-left: 4px solid #fb923c;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
        color: #fed7aa;
    }
    
    .feature-box {
        background: linear-gradient(135deg, #7c3aed 0%, #2563eb 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
    }
    
    .feature-box h4 {
        margin: 0 0 0.5rem 0;
        font-size: 1.2rem;
    }
    
    .feature-box p {
        margin: 0;
        opacity: 0.9;
    }
    
    /* Register cards (if needed for navigation) */
    .register-card {
        background: #2d3748; /* Darker background for cards */
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        margin: 1rem 0;
        border-left: 5px solid #7c3aed; /* Accent color */
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        color: #e2e8f0; /* Light text for dark background */
    }
    
    .register-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.4);
    }
    
    .register-card h3 {
        color: #a78bfa; /* Lighter accent for headers */
        margin-top: 0;
        font-size: 1.5rem;
    }
    
    .register-card p {
        color: #cbd5e0; /* Slightly darker light text */
        margin: 0.5rem 0;
    }
    
    
    .feature-box p {
        margin: 0;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>📊 EXCISE PARALLEL REGISTER SYSTEM</h1>
    <p>SIP 2 LIFE DISTILLERIES</p>
    <p style="font-size: 1rem; margin-top: 0.5rem;">Comprehensive Digital Register Management</p>
</div>
""", unsafe_allow_html=True)

# Welcome message
st.markdown("## 🎯 Welcome to the Excise Register System")
st.markdown("""
This comprehensive system manages all excise-related registers for distillery operations. 
Select a register from the sidebar to begin.
""")

st.markdown("---")

# Key Features
st.markdown("## ✨ System Features")

col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    st.markdown("""
    <div class="feature-box">
        <h4>🔄 Auto-Integration</h4>
        <p>Seamless data flow between registers</p>
    </div>
    """, unsafe_allow_html=True)

with col_f2:
    st.markdown("""
    <div class="feature-box" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
        <h4>🧮 Auto-Calculations</h4>
        <p>Automatic BL, AL, fees, and duty calculations</p>
    </div>
    """, unsafe_allow_html=True)

with col_f3:
    st.markdown("""
    <div class="feature-box" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
        <h4>✅ Validation</h4>
        <p>Real-time balance and data validation</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Quick Stats
st.markdown("## 📊 System Overview")

col_s1, col_s2, col_s3, col_s4 = st.columns(4)

with col_s1:
    st.metric("Total Registers", "6", help="Number of active registers")

with col_s2:
    st.metric("Bottle Sizes", "6", help="Supported bottle measurements")

with col_s3:
    st.metric("Strength Options", "4", help="U.P. degree options")

with col_s4:
    st.metric("Integration Points", "5", help="Cross-register integrations")

st.markdown("---")

# Instructions
st.markdown("## 📖 Getting Started")

st.markdown("""
### 📝 Daily Workflow:

1. **Reg-A (Production)** → Record production and bottling operations
2. **Reg-78** → Track production fees on bulk litres
3. **Reg-B** → Record bottle issues and production fees
4. **Excise Duty Register** → Calculate and track excise duty on issued bottles

### 🎯 Navigation:

Use the **sidebar** to navigate between different registers. Each register has:
- **Data Entry View** - For daily entries
- **Summary View** - For consolidated reports
- **Auto-fill Options** - For streamlined data entry

### 💡 Tips:

- ✅ Enable auto-fill options for faster entry
- ✅ Verify auto-filled data before saving
- ✅ Generate summaries after completing entries
- ✅ Use validation warnings to ensure data accuracy
""")

st.markdown("---")

# Footer
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p><strong>Excise Parallel Register System</strong></p>
    <p>SIP 2 LIFE DISTILLERIES | Digital Register Management</p>
    <p style="font-size: 0.9rem; margin-top: 1rem;">
        Built with Streamlit | Version 1.0
    </p>
</div>
""", unsafe_allow_html=True)
