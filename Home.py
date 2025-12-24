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
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 3rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        margin: 1rem 0 0 0;
        font-size: 1.3rem;
        opacity: 0.95;
    }
    
    .register-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 5px solid #667eea;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .register-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }
    
    .register-card h3 {
        color: #667eea;
        margin-top: 0;
        font-size: 1.5rem;
    }
    
    .register-card p {
        color: #666;
        margin: 0.5rem 0;
    }
    
    .feature-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        text-align: center;
    }
    
    .feature-box h4 {
        margin: 0 0 0.5rem 0;
        font-size: 1.2rem;
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

# Available Registers
st.markdown("## 📋 Available Registers")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="register-card">
        <h3>🏭 Reg-A - Production Register</h3>
        <p><strong>Purpose:</strong> Track production operations and bottling</p>
        <p><strong>Features:</strong></p>
        <ul>
            <li>Batch-wise production tracking</li>
            <li>Bottling operations management</li>
            <li>Multi-size bottle production</li>
            <li>BL/AL automatic calculations</li>
            <li>Wastage tracking</li>
            <li>Daily production summary</li>
        </ul>
        <p><strong>Status:</strong> ✅ Fully Operational</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="register-card">
        <h3>📋 Reg-74 - Vat Operations</h3>
        <p><strong>Purpose:</strong> Track vat operations and storage</p>
        <p><strong>Features:</strong></p>
        <ul>
            <li>SST/BRT vat management</li>
            <li>Transfer operations</li>
            <li>Storage wastage (0.3% threshold)</li>
            <li>Vat-wise inventory</li>
            <li>Daily operations log</li>
        </ul>
        <p><strong>Status:</strong> ✅ Fully Operational</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="register-card">
        <h3>📄 Reg-76 - SIP 2 Register</h3>
        <p><strong>Purpose:</strong> Official SIP 2 production register</p>
        <p><strong>Features:</strong></p>
        <ul>
            <li>Opening/closing stock tracking</li>
            <li>Production recording</li>
            <li>Issue tracking</li>
            <li>PDF export with official format</li>
            <li>Excise officer signatures</li>
        </ul>
        <p><strong>Status:</strong> ✅ Fully Operational</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="register-card">
        <h3>📦 Reg-B - Issue of Country Liquor in Bottles</h3>
        <p><strong>Purpose:</strong> Track production fees and bottle stock inventory</p>
        <p><strong>Features:</strong></p>
        <ul>
            <li>Production fees account (₹3 per bottle)</li>
            <li>Multi-size bottle tracking (750ml, 600ml, 500ml, 375ml, 300ml, 180ml)</li>
            <li>Multi-strength tracking (50°, 60°, 70°, 80° U.P.)</li>
            <li>Auto-fill from Reg-A production data</li>
            <li>BL/AL automatic calculations</li>
            <li>Wastage/breakage tracking</li>
        </ul>
        <p><strong>Status:</strong> ✅ Fully Operational</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="register-card">
        <h3>💵 Reg-78 - Production Fees Register</h3>
        <p><strong>Purpose:</strong> Track production fees on bulk litres</p>
        <p><strong>Features:</strong></p>
        <ul>
            <li>Production fees at ₹3/BL</li>
            <li>Opening/closing balance tracking</li>
            <li>Deposit management with E-Challan</li>
            <li>Daily summary generation</li>
            <li>Balance validation</li>
        </ul>
        <p><strong>Status:</strong> ✅ Fully Operational</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="register-card">
        <h3>💰 Excise Duty Register</h3>
        <p><strong>Purpose:</strong> Personal ledger account of excise duty for IML</p>
        <p><strong>Features:</strong></p>
        <ul>
            <li>Strength-based duty rates (₹50, ₹20, ₹17 per BL)</li>
            <li>Auto-fill from Reg-B issued bottles</li>
            <li>Financial account tracking</li>
            <li>Transport permit tracking</li>
            <li>Duty breakdown by strength</li>
            <li>Balance validation</li>
        </ul>
        <p><strong>Status:</strong> ✅ Fully Operational</p>
    </div>
    """, unsafe_allow_html=True)

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
