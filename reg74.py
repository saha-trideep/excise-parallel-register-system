import streamlit as st
import pandas as pd
from datetime import datetime
import time
import importlib
from utils import calculate_bl, calculate_al
import reg74_backend
from reg74_schema import OPERATION_TYPES, SST_VATS, BRT_VATS, ALL_VATS, TARGET_STRENGTHS

# Reload backend to get latest changes
importlib.reload(reg74_backend)

# Page Configuration
st.set_page_config(
    page_title="Reg-74 Spirit Operations",
    page_icon="🏭",
    layout="wide",
)

# Custom CSS for Ultra-Compact Dark Mode Design
st.markdown("""
    <style>
    /* Global Dark Mode */
    .stApp {
        background-color: #0a0e1a;
    }
    
    /* Compact Input Fields */
    .stTextInput input, .stNumberInput input, .stSelectbox select, .stDateInput input {
        background-color: #1a1f2e !important;
        border: 1.5px solid #3d4a5c !important;
        color: #e8edf5 !important;
        font-weight: 500;
        padding: 0.4rem 0.6rem !important;
        font-size: 0.9rem !important;
        height: 38px !important;
    }
    
    .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox select:focus {
        border-color: #4f9eff !important;
        box-shadow: 0 0 0 1px #4f9eff !important;
    }
    
    /* Ultra-Compact Section Containers */
    .section-container {
        background: linear-gradient(145deg, #141824 0%, #1a1f2e 100%);
        padding: 15px 18px;
        border-radius: 8px;
        margin-bottom: 12px;
        border: 1px solid #2a3441;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
    }
    
    .section-header {
        font-size: 0.95rem;
        font-weight: 700;
        color: #4f9eff;
        margin-bottom: 12px;
        border-bottom: 2px solid #2563eb;
        padding-bottom: 6px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Compact Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d4a6f 100%);
        padding: 10px 12px;
        border-radius: 6px;
        border: 1.5px solid #3b82f6;
        text-align: center;
        box-shadow: 0 2px 6px rgba(59, 130, 246, 0.25);
    }
    
    .metric-card small {
        color: #93c5fd !important;
        font-weight: 600;
        font-size: 0.75rem !important;
        display: block;
        margin-bottom: 4px;
    }
    
    .metric-card span {
        color: #e0f2fe !important;
        font-size: 1.1rem !important;
        font-weight: 700;
    }
    
    /* Compact Labels */
    label, .stMarkdown p, label p {
        color: #cbd5e0 !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        margin-bottom: 4px !important;
    }
    
    /* Enhanced Buttons */
    .stButton button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
        font-size: 0.9rem;
    }
    
    .stButton button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
        transform: translateY(-1px);
    }
    
    /* Compact Column Spacing */
    [data-testid="column"] {
        padding: 0 6px !important;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0d1117;
        border-right: 1px solid #2a3441;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: #141824;
        padding: 8px;
        border-radius: 6px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #1e2530;
        color: #94a3b8;
        border-radius: 5px;
        padding: 8px 16px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
    }
    
    /* Info/Alert Boxes */
    .stAlert {
        background-color: #1a1f2e !important;
        border-left: 3px solid #3b82f6 !important;
        color: #cbd5e0 !important;
        padding: 10px 12px !important;
        font-size: 0.85rem !important;
    }
    
    /* Dataframe */
    .stDataFrame {
        background-color: #141824;
        border-radius: 6px;
        font-size: 0.85rem;
    }
    
    /* Metric Override */
    [data-testid="stMetricValue"] {
        color: #4f9eff !important;
        font-size: 1.3rem !important;
    }
    
    /* Reduce vertical spacing */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 1rem !important;
    }
    
    /* Operation Type Badge */
    .op-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 700;
        margin-right: 8px;
    }
    
    .op-unload { background: #10b981; color: white; }
    .op-transfer { background: #f59e0b; color: white; }
    .op-reduction { background: #8b5cf6; color: white; }
    .op-production { background: #ef4444; color: white; }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 15px 0;'>
            <div style='font-size: 3.5rem; margin-bottom: 8px;'>🏭</div>
            <h2 style='color: #4f9eff; margin: 0; font-weight: 800;'>Excise Register</h2>
            <p style='color: #94a3b8; font-size: 0.8rem; margin-top: 4px;'>Reg-74 Spirit Operations</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sync Status
    gs_client = reg74_backend.get_google_client()
    if gs_client:
        st.success("🟢 Connected to Google Sheets")
    else:
        st.warning("🟡 Using Local Storage (CSV)")
    
    st.divider()
    register = st.radio(
        "Register Selection",
        ["▶ Reg-74 – Spirit Operations", 
         "Reg-76 – Spirit Receipt", 
         "⏸ Reg-A – (Disabled)"],
        index=0
    )
    
    if "Reg-76" in register:
        st.info("💡 To access Reg-76, run: `streamlit run reg76.py`")
        st.stop()

# Helper Functions
def display_calc_result(label, value, unit=""):
    st.markdown(f"""
        <div class="metric-card">
            <small>{label}</small>
            <span>{value:.3f} {unit}</span>
        </div>
    """, unsafe_allow_html=True)

def calculate_reduction(initial_bl, initial_strength, water_bl, target_strength):
    """Calculate reduction parameters"""
    total_bl = initial_bl + water_bl
    # AL remains constant during dilution
    initial_al = calculate_al(initial_bl, initial_strength)
    final_strength = (initial_al / total_bl) * 100 if total_bl > 0 else 0
    return {
        "total_bl": total_bl,
        "total_al": initial_al,
        "final_strength": final_strength,
        "achieved_target": abs(final_strength - target_strength) < 0.5
    }

def calculate_storage_wastage(expected_bl, expected_al, actual_bl, actual_al):
    """Calculate storage wastage before operation starts"""
    wastage_bl = expected_bl - actual_bl
    wastage_al = expected_al - actual_al
    wastage_percentage = (wastage_al / expected_al * 100) if expected_al > 0 else 0
    
    return {
        "wastage_bl": wastage_bl,
        "wastage_al": wastage_al,
        "wastage_percentage": wastage_percentage,
        "has_wastage": wastage_al > 0.1  # Threshold 0.1L
    }

def display_storage_wastage_section(vat_no, vat_type="SST/BRT"):
    """Display storage wastage verification section"""
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-header">⚠️ STORAGE WASTAGE VERIFICATION - {vat_no}</div>', unsafe_allow_html=True)
    
    # Get expected values from last closing
    current_stock = reg74_backend.get_vat_current_stock(vat_no)
    expected_bl = current_stock['bl']
    expected_al = current_stock['al']
    
    # Get last operation date with error handling
    try:
        if hasattr(reg74_backend, 'get_last_operation_date'):
            last_date = reg74_backend.get_last_operation_date(vat_no)
        else:
            last_date = None
    except Exception:
        last_date = None
    
    storage_days = (datetime.now().date() - last_date).days if last_date else 0
    
    # Check if VAT appears empty
    if expected_bl == 0 and expected_al == 0:
        st.warning(f"""
        ⚠️ **VAT {vat_no} appears to be empty** (no previous records found).  
        This is the first operation for this VAT. Enter the actual stock below.
        """)
        last_date_display = "N/A (First Operation)"
    else:
        last_date_display = str(last_date) if last_date else 'N/A'
    
    st.info(f"""
    📋 **Expected Stock** (from last closing on {last_date_display}):  
    **BL:** {expected_bl:.3f} L | **AL:** {expected_al:.3f} L | **Storage Days:** {storage_days}
    """)
    
    st.markdown("**Physical Verification (Dip Reading)**")
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        actual_bl = st.number_input(f"Actual BL (L)*", min_value=0.0, step=0.001, format="%.3f", key=f"actual_bl_{vat_no}")
    with c2:
        actual_al = st.number_input(f"Actual AL (L)*", min_value=0.0, step=0.001, format="%.3f", key=f"actual_al_{vat_no}")
    with c3:
        dip_reading = st.number_input(f"Dip (cm)", min_value=0.0, step=0.1, key=f"dip_{vat_no}")
    with c4:
        dip_temp = st.number_input(f"Temp (°C)", value=20.0, step=0.1, key=f"dip_temp_{vat_no}")
    with c5:
        dip_indication = st.text_input(f"Indication", key=f"dip_ind_{vat_no}", help="Alcoholmeter Indication")
    
    # Calculate wastage
    if actual_bl > 0 or actual_al > 0:
        wastage_result = calculate_storage_wastage(expected_bl, expected_al, actual_bl, actual_al)
        
        st.markdown("**Storage Wastage Calculation**")
        w1, w2, w3, w4 = st.columns(4)
        with w1: 
            st.metric("Wastage BL", f"{wastage_result['wastage_bl']:.3f} L", 
                     delta=f"-{wastage_result['wastage_bl']:.3f}" if wastage_result['wastage_bl'] > 0 else None,
                     delta_color="inverse")
        with w2: 
            st.metric("Wastage AL", f"{wastage_result['wastage_al']:.3f} L",
                     delta=f"-{wastage_result['wastage_al']:.3f}" if wastage_result['wastage_al'] > 0 else None,
                     delta_color="inverse")
        with w3: 
            st.metric("Wastage %", f"{wastage_result['wastage_percentage']:.3f}%")
        with w4:
            if wastage_result['has_wastage']:
                st.error("⚠️ Wastage Detected")
            else:
                st.success("✅ No Wastage")
        
        if wastage_result['has_wastage']:
            st.warning(f"""
            ⚠️ **EXCISE NOTE**: Storage wastage of **{wastage_result['wastage_al']:.3f} AL** detected.  
            **No allowable wastage** for storage. This wastage must be accounted for and documented.  
            **Storage Period:** {storage_days} days
            """)
            wastage_note = st.text_area("Wastage Explanation/Note*", 
                                       placeholder="Explain reason for storage wastage...",
                                       key=f"wastage_note_{vat_no}")
        else:
            wastage_note = ""
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        return {
            "expected_bl": expected_bl,
            "expected_al": expected_al,
            "actual_bl": actual_bl,
            "actual_al": actual_al,
            "opening_dip": dip_reading,
            "opening_temp": dip_temp,
            "opening_indication": dip_indication,
            "wastage_bl": wastage_result['wastage_bl'],
            "wastage_al": wastage_result['wastage_al'],
            "wastage_percentage": wastage_result['wastage_percentage'],
            "storage_days": storage_days,
            "wastage_note": wastage_note,
            "has_wastage": wastage_result['has_wastage']
        }
    else:
        st.markdown('</div>', unsafe_allow_html=True)
        return None


# Main Content
tab_entry, tab_admin = st.tabs(["🔒 SECURE DATA ENTRY", "📋 ADMINISTRATIVE VIEW"])

with tab_entry:
    st.subheader("Reg-74 Spirit Operations Form")
    
    # SECTION 1: OPERATION TYPE SELECTION
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">SECTION 1 – OPERATION TYPE</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        operation_type = st.selectbox("Select Operation Type*", OPERATION_TYPES, key="op_type")
    with col2:
        operation_date = st.date_input("Operation Date*", value=datetime.now())
    with col3:
        if operation_type in ["Reduction/Blending", "Transfer SST to BRT"]:
            batch_no = st.text_input("Batch No.*", placeholder="BATCH-001", 
                                    help="Required for reduction and SST→BRT transfers")
        else:
            batch_no = st.text_input("Batch No.", disabled=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Dynamic form based on operation type
    if operation_type == "Unloading from Reg-76":
        # SECTION 2: REG-76 REFERENCE
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">SECTION 2 – REG-76 REFERENCE</div>', unsafe_allow_html=True)
        
        available_reg76 = reg74_backend.get_available_reg76_records()
        
        if available_reg76.empty:
            st.warning("⚠️ No unprocessed Reg-76 records available. Please complete a Reg-76 entry first.")
            ref_reg76_id = None
        else:
            col_r1, col_r2 = st.columns(2)
            with col_r1:
                reg76_options = ["Select Reg-76 Record"] + available_reg76['reg76_id'].tolist()
                selected_reg76 = st.selectbox("Select Reg-76 Record*", reg76_options)
                ref_reg76_id = selected_reg76 if selected_reg76 != "Select Reg-76 Record" else None
            
            if ref_reg76_id:
                reg76_data = available_reg76[available_reg76['reg76_id'] == ref_reg76_id].iloc[0]
                with col_r2:
                    st.info(f"""
                    **Vehicle:** {reg76_data.get('vehicle_no', 'N/A')}  
                    **Spirit:** {reg76_data.get('spirit_nature', 'N/A')}  
                    **Received AL:** {reg76_data.get('rec_al', 0):.2f} L
                    """)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # SECTION 3: DESTINATION VAT
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">SECTION 3 – UNLOADING DETAILS</div>', unsafe_allow_html=True)
        
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            destination_vat = st.selectbox("Destination VAT*", ["Select VAT"] + SST_VATS)
        with c2:
            receipt_bl = st.number_input("Receipt BL (L)", min_value=0.0, step=0.001, format="%.3f")
        with c3:
            receipt_al = st.number_input("Receipt AL (L)", min_value=0.0, step=0.001, format="%.3f")
        with c4:
            receipt_strength = st.number_input("Strength (% v/v)", min_value=0.0, max_value=100.0, step=0.01)
        
        c5, c6, c7, c8 = st.columns(4)
        with c5:
            receipt_temp = st.number_input("Temperature (°C)", value=20.0, step=0.1)
        with c6:
            receipt_density = st.number_input("Density (gm/cc)", min_value=0.0, step=0.0001, format="%.4f")
        with c7:
            permit_no = st.text_input("Permit No.")
        with c8:
            evc_no = st.text_input("EVC No.")
        
        # Auto-populate from Reg-76 if selected
        if ref_reg76_id and 'reg76_data' in locals():
            if receipt_bl == 0.0:
                receipt_bl = float(reg76_data.get('rec_bl', 0))
            if receipt_al == 0.0:
                receipt_al = float(reg76_data.get('rec_al', 0))
            if receipt_strength == 0.0:
                receipt_strength = float(reg76_data.get('rec_strength', 0))
        
        # Get current VAT stock
        if destination_vat != "Select VAT":
            current_stock = reg74_backend.get_vat_current_stock(destination_vat)
            opening_bl = current_stock['bl']
            opening_al = current_stock['al']
            opening_strength = current_stock['strength']
            
            # Calculate closing
            closing_bl = opening_bl + receipt_bl
            closing_al = opening_al + receipt_al
            closing_strength = (closing_al / closing_bl * 100) if closing_bl > 0 else 0
            
            st.markdown("**Stock Summary**")
            m1, m2, m3, m4 = st.columns(4)
            with m1: display_calc_result("Opening BL", opening_bl, "L")
            with m2: display_calc_result("Receipt BL", receipt_bl, "L")
            with m3: display_calc_result("Closing BL", closing_bl, "L")
            with m4: display_calc_result("Closing Strength", closing_strength, "%")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        source_vat = "Reg-76 Receipt"
        issue_bl = issue_al = issue_strength = 0.0
        water_added_bl = target_strength_val = 0.0
        
    elif operation_type in ["Transfer SST to BRT", "Inter-Transfer SST", "Inter-Transfer BRT"]:
        # STORAGE WASTAGE VERIFICATION (Before Transfer)
        st.markdown("---")
        st.markdown("### 📊 Step 1: Storage Wastage Verification")
        st.info("⚠️ **IMPORTANT**: Verify actual stock before starting transfer operation. Any storage wastage must be documented.")
        
        # Select source VAT first for wastage check
        if operation_type == "Transfer SST to BRT":
            temp_source_vat = st.selectbox("Select Source VAT (SST) for Verification*", ["Select VAT"] + SST_VATS, key="temp_source")
        elif operation_type == "Inter-Transfer SST":
            temp_source_vat = st.selectbox("Select Source VAT (SST) for Verification*", ["Select VAT"] + SST_VATS, key="temp_source")
        else:  # Inter-Transfer BRT
            temp_source_vat = st.selectbox("Select Source VAT (BRT) for Verification*", ["Select VAT"] + BRT_VATS, key="temp_source")
        
        storage_wastage_data = None
        if temp_source_vat != "Select VAT":
            storage_wastage_data = display_storage_wastage_section(temp_source_vat)
        
        st.markdown("---")
        st.markdown("### 🔄 Step 2: Transfer Operation Details")
        
        # SECTION 2: TRANSFER DETAILS
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">SECTION 2 – TRANSFER DETAILS</div>', unsafe_allow_html=True)
        
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            if operation_type == "Transfer SST to BRT":
                source_vat = st.selectbox("Source VAT (SST)*", ["Select VAT"] + SST_VATS)
            elif operation_type == "Inter-Transfer SST":
                source_vat = st.selectbox("Source VAT (SST)*", ["Select VAT"] + SST_VATS)
            else:  # Inter-Transfer BRT
                source_vat = st.selectbox("Source VAT (BRT)*", ["Select VAT"] + BRT_VATS)
        
        with c2:
            if operation_type == "Transfer SST to BRT":
                destination_vat = st.selectbox("Destination VAT (BRT)*", ["Select VAT"] + BRT_VATS)
            elif operation_type == "Inter-Transfer SST":
                destination_vat = st.selectbox("Destination VAT (SST)*", ["Select VAT"] + SST_VATS)
            else:  # Inter-Transfer BRT
                destination_vat = st.selectbox("Destination VAT (BRT)*", ["Select VAT"] + BRT_VATS)
        
        with c3:
            issue_bl = st.number_input("Transfer BL (L)*", min_value=0.0, step=0.001, format="%.3f")
        with c4:
            issue_al = st.number_input("Transfer AL (L)*", min_value=0.0, step=0.001, format="%.3f")
        
        c5, c6, c7, c8 = st.columns(4)
        with c5:
            issue_strength = st.number_input("Strength (% v/v)*", min_value=0.0, max_value=100.0, step=0.01)
        with c6:
            issue_temp = st.number_input("Temperature (°C)", value=20.0, step=0.1)
        with c7:
            permit_no = st.text_input("Pass No.")
        with c8:
            evc_no = st.text_input("EVC No.")
        
        # Stock calculations
        if source_vat != "Select VAT":
            source_stock = reg74_backend.get_vat_current_stock(source_vat)
            source_opening_bl = source_stock['bl']
            source_opening_al = source_stock['al']
            source_closing_bl = source_opening_bl - issue_bl
            source_closing_al = source_opening_al - issue_al
            
            st.markdown("**Source VAT Stock**")
            m1, m2, m3 = st.columns(3)
            with m1: display_calc_result("Opening BL", source_opening_bl, "L")
            with m2: display_calc_result("Issue BL", issue_bl, "L")
            with m3: display_calc_result("Closing BL", source_closing_bl, "L")
            
            if source_closing_bl < 0:
                st.error("❌ Insufficient stock in source VAT!")
        
        if destination_vat != "Select VAT":
            dest_stock = reg74_backend.get_vat_current_stock(destination_vat)
            dest_opening_bl = dest_stock['bl']
            dest_opening_al = dest_stock['al']
            dest_closing_bl = dest_opening_bl + issue_bl
            dest_closing_al = dest_opening_al + issue_al
            
            st.markdown("**Destination VAT Stock**")
            m4, m5, m6 = st.columns(3)
            with m4: display_calc_result("Opening BL", dest_opening_bl, "L")
            with m5: display_calc_result("Receipt BL", issue_bl, "L")
            with m6: display_calc_result("Closing BL", dest_closing_bl, "L")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        ref_reg76_id = None
        receipt_bl = issue_bl
        receipt_al = issue_al
        receipt_strength = issue_strength
        receipt_temp = issue_temp
        receipt_density = 0.0
        water_added_bl = target_strength_val = 0.0
        opening_bl = dest_opening_bl if 'dest_opening_bl' in locals() else 0.0
        opening_al = dest_opening_al if 'dest_opening_al' in locals() else 0.0
        closing_bl = dest_closing_bl if 'dest_closing_bl' in locals() else 0.0
        closing_al = dest_closing_al if 'dest_closing_al' in locals() else 0.0
        
    elif operation_type == "Reduction/Blending":
        # STORAGE WASTAGE VERIFICATION (Before Reduction)
        st.markdown("---")
        st.markdown("### 📊 Step 1: Storage Wastage Verification")
        st.info("⚠️ **IMPORTANT**: Verify actual stock before starting reduction. Any storage wastage must be documented.")
        
        temp_reduction_vat = st.selectbox("Select BRT VAT for Verification*", ["Select VAT"] + BRT_VATS, key="temp_reduction")
        
        storage_wastage_data = None
        if temp_reduction_vat != "Select VAT":
            storage_wastage_data = display_storage_wastage_section(temp_reduction_vat)
        
        st.markdown("---")
        st.markdown("### ⚗️ Step 2: Reduction/Blending Operation")
        
        # SECTION 2: REDUCTION DETAILS
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">SECTION 2 – REDUCTION/BLENDING DETAILS</div>', unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            source_vat = st.selectbox("Source VAT (BRT)*", ["Select VAT"] + BRT_VATS)
        with c2:
            destination_vat = source_vat  # Same VAT for reduction
            st.info(f"Destination: {source_vat}")
        with c3:
            target_strength_select = st.selectbox("Target Strength*", TARGET_STRENGTHS)
        
        if target_strength_select == "Custom":
            target_strength_val = st.number_input("Custom Target Strength (% v/v)*", min_value=0.0, max_value=100.0, step=0.01)
        else:
            target_strength_val = float(target_strength_select.split('%')[0])
        
        # Initialize default values
        opening_bl = opening_al = opening_strength = 0.0
        water_added_bl = 0.0
        water_temp = 20.0
        closing_bl = closing_al = closing_strength = 0.0
        permit_no = ""
        
        # Get current stock
        if source_vat != "Select VAT":
            current_stock = reg74_backend.get_vat_current_stock(source_vat)
            opening_bl = current_stock['bl']
            opening_al = current_stock['al']
            opening_strength = current_stock['strength']
            
            st.markdown("**Current Stock**")
            m1, m2, m3 = st.columns(3)
            with m1: display_calc_result("Current BL", opening_bl, "L")
            with m2: display_calc_result("Current AL", opening_al, "L")
            with m3: display_calc_result("Current Strength", opening_strength, "%")
            
            # Water calculation
            c4, c5, c6 = st.columns(3)
            with c4:
                water_added_bl = st.number_input("Water Added (BL)*", min_value=0.0, step=0.001, format="%.3f")
            with c5:
                water_temp = st.number_input("Water Temp (°C)", value=20.0, step=0.1)
            with c6:
                permit_no = st.text_input("Batch Permit No.")
            
            # Calculate reduction
            if water_added_bl > 0:
                reduction_result = calculate_reduction(opening_bl, opening_strength, water_added_bl, target_strength_val)
                
                st.markdown("**After Reduction**")
                m4, m5, m6, m7 = st.columns(4)
                with m4: display_calc_result("Total BL", reduction_result['total_bl'], "L")
                with m5: display_calc_result("Total AL", reduction_result['total_al'], "L")
                with m6: display_calc_result("Achieved Strength", reduction_result['final_strength'], "%")
                with m7:
                    if reduction_result['achieved_target']:
                        st.success("✅ Target Achieved")
                    else:
                        st.warning(f"⚠️ Variance: {abs(reduction_result['final_strength'] - target_strength_val):.2f}%")
                
                closing_bl = reduction_result['total_bl']
                closing_al = reduction_result['total_al']
                closing_strength = reduction_result['final_strength']
            else:
                closing_bl = opening_bl
                closing_al = opening_al
                closing_strength = opening_strength
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        ref_reg76_id = None
        receipt_bl = water_added_bl
        receipt_al = 0.0
        receipt_strength = 0.0
        receipt_temp = water_temp
        receipt_density = 1.0
        issue_bl = issue_al = issue_strength = 0.0
        evc_no = ""

        
    elif operation_type == "Issue for Production":
        # SECTION 2: PRODUCTION ISSUE
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">SECTION 2 – PRODUCTION ISSUE DETAILS</div>', unsafe_allow_html=True)
        
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            source_vat = st.selectbox("Source VAT (BRT)*", ["Select VAT"] + BRT_VATS)
        with c2:
            destination_vat = "Production (Reg-A)"
            st.info("Destination: Reg-A")
        with c3:
            issue_bl = st.number_input("Issue BL (L)*", min_value=0.0, step=0.001, format="%.3f")
        with c4:
            issue_al = st.number_input("Issue AL (L)*", min_value=0.0, step=0.001, format="%.3f")
        
        c5, c6, c7, c8 = st.columns(4)
        with c5:
            issue_strength = st.number_input("Strength (% v/v)*", min_value=0.0, max_value=100.0, step=0.01)
        with c6:
            issue_temp = st.number_input("Temperature (°C)", value=20.0, step=0.1)
        with c7:
            permit_no = st.text_input("Production Order No.")
        with c8:
            evc_no = st.text_input("EVC No.")
        
        # Stock calculations
        if source_vat != "Select VAT":
            current_stock = reg74_backend.get_vat_current_stock(source_vat)
            opening_bl = current_stock['bl']
            opening_al = current_stock['al']
            opening_strength = current_stock['strength']
            closing_bl = opening_bl - issue_bl
            closing_al = opening_al - issue_al
            closing_strength = (closing_al / closing_bl * 100) if closing_bl > 0 else 0
            
            st.markdown("**Stock Movement**")
            m1, m2, m3, m4 = st.columns(4)
            with m1: display_calc_result("Opening BL", opening_bl, "L")
            with m2: display_calc_result("Issue BL", issue_bl, "L")
            with m3: display_calc_result("Closing BL", closing_bl, "L")
            with m4: display_calc_result("Closing Strength", closing_strength, "%")
            
            if closing_bl < 0:
                st.error("❌ Insufficient stock in source VAT!")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        ref_reg76_id = None
        receipt_bl = receipt_al = receipt_strength = 0.0
        receipt_temp = receipt_density = 0.0
        water_added_bl = target_strength_val = 0.0
    
    # SECTION: REMARKS & APPROVAL
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">SECTION 3 – REMARKS & APPROVAL</div>', unsafe_allow_html=True)
    
    c_r1, c_r2, c_r3 = st.columns(3)
    with c_r1:
        operation_remarks = st.text_area("Operation Remarks", height=80)
    with c_r2:
        officer_name = st.text_input("Officer Name")
        officer_sig_date = st.date_input("Signature Date", value=datetime.now())
    with c_r3:
        dip_reading = st.number_input("Dip Reading (cm)", min_value=0.0, step=0.1)
        dip_temp = st.number_input("Dip Temp (°C)", value=20.0, step=0.1)
        dip_ind = st.text_input("Dip Indication", help="Alcoholmeter Indication")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # SUBMISSION
    if st.button("🚀 FINAL SUBMIT & LOCK RECORD", use_container_width=True, type="primary"):
        # Validation
        errors = []
        if operation_type == "Unloading from Reg-76" and not ref_reg76_id:
            errors.append("Please select a Reg-76 record")
        if 'source_vat' in locals() and source_vat == "Select VAT":
            errors.append("Please select source VAT")
        if 'destination_vat' in locals() and destination_vat == "Select VAT" and operation_type != "Issue for Production":
            errors.append("Please select destination VAT")
        if operation_type in ["Reduction/Blending", "Transfer SST to BRT"] and not batch_no:
            errors.append("Batch number is required for reduction and SST→BRT transfers")
        
        # Check storage wastage note if wastage detected
        if 'storage_wastage_data' in locals() and storage_wastage_data:
            if storage_wastage_data.get('has_wastage') and not storage_wastage_data.get('wastage_note'):
                errors.append("Wastage explanation/note is required when storage wastage is detected")
        
        if errors:
            for error in errors:
                st.error(f"❌ {error}")
        else:
            with st.spinner("Writing to Register..."):
                # Prepare storage wastage data
                if 'storage_wastage_data' in locals() and storage_wastage_data:
                    swdata = storage_wastage_data
                else:
                    swdata = {
                        "expected_bl": 0.0, "expected_al": 0.0,
                        "actual_bl": 0.0, "actual_al": 0.0,
                        "wastage_bl": 0.0, "wastage_al": 0.0,
                        "wastage_percentage": 0.0, "storage_days": 0,
                        "wastage_note": ""
                    }
                
                payload = {
                    "operation_type": operation_type,
                    "operation_date": str(operation_date),
                    "batch_no": batch_no if batch_no else "",
                    "ref_reg76_id": ref_reg76_id if 'ref_reg76_id' in locals() else "",
                    "source_vat": source_vat if 'source_vat' in locals() else "",
                    "source_opening_bl": opening_bl if 'opening_bl' in locals() else 0.0,
                    "source_opening_al": opening_al if 'opening_al' in locals() else 0.0,
                    "source_opening_strength": opening_strength if 'opening_strength' in locals() else 0.0,
                    
                    # Storage wastage fields
                    "expected_opening_bl": swdata.get("expected_bl", 0.0),
                    "expected_opening_al": swdata.get("expected_al", 0.0),
                    "actual_opening_bl": swdata.get("actual_bl", 0.0),
                    "actual_opening_al": swdata.get("actual_al", 0.0),
                    "opening_dip_cm": swdata.get("opening_dip", 0.0), # NEW
                    "opening_temp": swdata.get("opening_temp", 0.0), # NEW
                    "opening_indication": swdata.get("opening_indication", ""), # NEW
                    "storage_wastage_bl": swdata.get("wastage_bl", 0.0),
                    "storage_wastage_al": swdata.get("wastage_al", 0.0),
                    "storage_wastage_percentage": swdata.get("wastage_percentage", 0.0),
                    "storage_days": swdata.get("storage_days", 0),
                    "storage_wastage_note": swdata.get("wastage_note", ""),
                    
                    "receipt_date": str(operation_date),
                    "receipt_bl": receipt_bl if 'receipt_bl' in locals() else 0.0,
                    "receipt_al": receipt_al if 'receipt_al' in locals() else 0.0,
                    "receipt_strength": receipt_strength if 'receipt_strength' in locals() else 0.0,
                    "receipt_temp": receipt_temp if 'receipt_temp' in locals() else 0.0,
                    "receipt_density": receipt_density if 'receipt_density' in locals() else 0.0,
                    "water_added_bl": water_added_bl if 'water_added_bl' in locals() else 0.0,
                    "water_temp": water_temp if 'water_temp' in locals() else 0.0,
                    "target_strength": target_strength_val if 'target_strength_val' in locals() else 0.0,
                    "total_bl": closing_bl if 'closing_bl' in locals() else 0.0,
                    "total_al": closing_al if 'closing_al' in locals() else 0.0,
                    "total_strength": closing_strength if 'closing_strength' in locals() else 0.0,
                    "issue_date": str(operation_date),
                    "issue_bl": issue_bl if 'issue_bl' in locals() else 0.0,
                    "issue_al": issue_al if 'issue_al' in locals() else 0.0,
                    "issue_strength": issue_strength if 'issue_strength' in locals() else 0.0,
                    "issue_temp": issue_temp if 'issue_temp' in locals() else 0.0,
                    "issue_density": 0.0,
                    "destination_vat": destination_vat if 'destination_vat' in locals() else "",
                    "closing_bl": closing_bl if 'closing_bl' in locals() else 0.0,
                    "closing_al": closing_al if 'closing_al' in locals() else 0.0,
                    "closing_strength": closing_strength if 'closing_strength' in locals() else 0.0,
                    "wastage_bl": 0.0,
                    "wastage_al": 0.0,
                    "wastage_percentage": 0.0,
                    "wastage_remarks": "",
                    "dip_reading_cm": dip_reading,
                    "dip_temp": dip_temp,
                    "closing_indication": dip_ind, # NEW
                    "dip_calculated_bl": 0.0,
                    "dip_variance_bl": 0.0,
                    "permit_no": permit_no if 'permit_no' in locals() else "",
                    "pass_no": permit_no if 'permit_no' in locals() else "",
                    "pass_date": str(operation_date),
                    "evc_no": evc_no if 'evc_no' in locals() else "",
                    "evc_date": str(operation_date),
                    "operation_remarks": operation_remarks,
                    "officer_name": officer_name,
                    "officer_signature_date": str(officer_sig_date),
                    "status": "Submitted"
                }
                
                rid = reg74_backend.save_record(payload)
                st.success(f"✅ Record Successfully Saved. Reg-74 ID: {rid}")
                time.sleep(2)
                st.rerun()

with tab_admin:
    st.subheader("Reg-74 Administrative Control")
    
    # Filter Controls
    with st.expander("🔍 Search & Filter", expanded=True):
        f1, f2, f3 = st.columns(3)
        with f1: f_date = st.date_input("Filter by Date", value=None)
        with f2: f_operation = st.selectbox("Filter by Operation", ["All"] + OPERATION_TYPES)
        with f3: f_vat = st.selectbox("Filter by VAT", ["All"] + ALL_VATS)
    
    # Data Table
    records = reg74_backend.filter_records(date_from=f_date, operation_type=f_operation, vat_no=f_vat)
    
    if records.empty:
        st.info("No records found in the system.")
    else:
        st.dataframe(
            records[[
                "reg74_id", "operation_date", "operation_type", "source_vat", 
                "destination_vat", "closing_bl", "closing_al", "status"
            ]],
            use_container_width=True,
            hide_index=True
        )
        
        st.info(f"""
        📊 **Data Storage**: {len(records)} records stored locally in `reg74_data.csv` 
        and synced to Google Sheets (Reg74 worksheet).
        """)
        
        st.divider()
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            csv = records.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Export to Excel (CSV)", 
                data=csv, 
                file_name=f"Reg74_Export_{datetime.now().strftime('%Y%m%d')}.csv"
            )
        with col_btn2:
            if st.button("🔄 Sync with GSheet", type="secondary"):
                with st.spinner("Synchronizing..."):
                    local_df = reg74_backend.get_data_local()
                    if local_df.empty:
                        st.info("No local records to sync.")
                    else:
                        success = reg74_backend.sync_to_gsheet(local_df)
                        if success:
                            st.success("✅ GSheet updated with local records!")
                            st.rerun()
                        else:
                            st.error("GSheet sync failed.")
