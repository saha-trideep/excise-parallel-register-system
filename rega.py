import streamlit as st
import pandas as pd
from datetime import datetime
import time
import importlib
from utils import calculate_bl, calculate_al
import rega_backend
from rega_schema import (
    PRODUCTION_SHIFTS, BOTTLE_SIZES, BOTTLES_PER_CASE, BRT_VATS,
    DISPATCH_TYPES, PRODUCT_TYPES, PRODUCTION_WASTAGE_LIMIT,
    CRITICAL_WASTAGE_THRESHOLD, STATUS_OPTIONS
)

# Reload backend to get latest changes
importlib.reload(rega_backend)

# Page Configuration
st.set_page_config(
    page_title="Reg-A Production Register",
    page_icon="🍾",
    layout="wide",
)

# Ultra-Compact Dark Mode CSS
st.markdown("""
    <style>
    /* Global Dark Mode */
    .stApp {
        background-color: #0a0e1a;
    }
    
    /* Compact Input Fields */
    .stTextInput input, .stNumberInput input, .stSelectbox select, 
    .stDateInput input, .stTextArea textarea {
        background-color: #1a1f2e !important;
        border: 1px solid #3b82f6 !important;
        color: #e8edf5 !important;
        padding: 6px 10px !important;
        height: 38px !important;
        font-size: 0.9rem !important;
    }
    
    .stTextArea textarea {
        height: 80px !important;
    }
    
    /* Compact Labels */
    .stTextInput label, .stNumberInput label, .stSelectbox label,
    .stDateInput label, .stTextArea label {
        color: #cbd5e0 !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        margin-bottom: 4px !important;
    }
    
    /* Section Containers */
    .section-container {
        background: linear-gradient(135deg, #1a1f2e 0%, #0f1419 100%);
        padding: 15px 18px;
        border-radius: 8px;
        margin-bottom: 12px;
        border-left: 3px solid #3b82f6;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    
    .section-header {
        color: #4f9eff;
        font-size: 0.95rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 12px;
        padding-bottom: 6px;
        border-bottom: 2px solid #3b82f6;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #1e3a5f 0%, #0f1e3a 100%);
        padding: 12px;
        border-radius: 6px;
        border: 1px solid #3b82f6;
        text-align: center;
    }
    
    .metric-card small {
        color: #94a3b8;
        font-size: 0.75rem;
        display: block;
        margin-bottom: 4px;
    }
    
    .metric-card span {
        color: #e8edf5;
        font-size: 1.1rem;
        font-weight: 700;
    }
    
    /* Wastage Alert Cards */
    .wastage-ok {
        background: linear-gradient(135deg, #064e3b 0%, #022c22 100%);
        border: 1px solid #10b981;
        padding: 12px;
        border-radius: 6px;
        color: #d1fae5;
    }
    
    .wastage-warning {
        background: linear-gradient(135deg, #7c2d12 0%, #431407 100%);
        border: 1px solid #f59e0b;
        padding: 12px;
        border-radius: 6px;
        color: #fed7aa;
    }
    
    .wastage-critical {
        background: linear-gradient(135deg, #7f1d1d 0%, #450a0a 100%);
        border: 1px solid #ef4444;
        padding: 12px;
        border-radius: 6px;
        color: #fecaca;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
        color: white;
        border: none;
        padding: 10px 20px;
        font-weight: 600;
        border-radius: 6px;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1e3a8a 100%);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    }
    
    /* Columns Spacing */
    [data-testid="column"] {
        padding: 0 6px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #0f1419;
        padding: 8px;
        border-radius: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #1a1f2e;
        color: #94a3b8;
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
        color: white;
    }
    
    /* Dataframe */
    .stDataFrame {
        background-color: #1a1f2e;
    }
    
    /* Info/Warning/Error boxes */
    .stAlert {
        background-color: #1a1f2e;
        border-radius: 6px;
        padding: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 20px 10px; background: linear-gradient(135deg, #1e3a5f 0%, #0f1e3a 100%); border-radius: 10px; margin-bottom: 20px;'>
            <h2 style='color: #4f9eff; margin: 0; font-size: 1.5rem;'>🍾 Reg-A</h2>
            <p style='color: #94a3b8; margin: 5px 0 0 0; font-size: 0.85rem;'>Production Register</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    register = st.radio(
        "Register Selection",
        ["Reg-76 – Spirit Receipt",
         "Reg-74 – Spirit Operations", 
         "▶ Reg-A – Production"],
        index=2
    )
    
    if "Reg-76" in register:
        st.info("💡 To access Reg-76, run: `streamlit run reg76.py`")
        st.stop()
    elif "Reg-74" in register:
        st.info("💡 To access Reg-74, run: `streamlit run reg74.py`")
        st.stop()

# Helper Functions
def display_calc_result(label, value, unit=""):
    st.markdown(f"""
        <div class="metric-card">
            <small>{label}</small>
            <span>{value:.3f} {unit}</span>
        </div>
    """, unsafe_allow_html=True)

def calculate_bottles_bl(bottles_180, bottles_375, bottles_750, bottles_1000):
    """Calculate total BL from bottle counts"""
    bl_180 = bottles_180 * BOTTLE_SIZES["180ml"]
    bl_375 = bottles_375 * BOTTLE_SIZES["375ml"]
    bl_750 = bottles_750 * BOTTLE_SIZES["750ml"]
    bl_1000 = bottles_1000 * BOTTLE_SIZES["1000ml"]
    
    return {
        "bl_180": bl_180,
        "bl_375": bl_375,
        "bl_750": bl_750,
        "bl_1000": bl_1000,
        "total_bl": bl_180 + bl_375 + bl_750 + bl_1000,
        "total_bottles": bottles_180 + bottles_375 + bottles_750 + bottles_1000
    }

def display_wastage_analysis(mfm2_bl, mfm2_al, bottles_bl, bottles_al, strength):
    """Display comprehensive wastage analysis"""
    wastage_result = rega_backend.calculate_production_wastage(mfm2_bl, mfm2_al, bottles_bl, bottles_al)
    
    st.markdown("---")
    st.markdown("### 📊 Production Wastage Analysis")
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("MFM2 Reading", f"{mfm2_bl:.3f} BL", f"{mfm2_al:.3f} AL")
    with col2:
        st.metric("Bottles Produced", f"{bottles_bl:.3f} BL", f"{bottles_al:.3f} AL")
    with col3:
        st.metric("Wastage", f"{wastage_result['wastage_bl']:.3f} BL", 
                 f"{wastage_result['wastage_al']:.3f} AL",
                 delta=f"-{wastage_result['wastage_al']:.3f}" if wastage_result['wastage_al'] > 0 else None,
                 delta_color="inverse")
    with col4:
        st.metric("Wastage %", f"{wastage_result['wastage_percentage']:.4f}%",
                 f"Limit: {PRODUCTION_WASTAGE_LIMIT}%")
    
    # Wastage status card
    if wastage_result['critical']:
        st.markdown(f"""
            <div class="wastage-critical">
                <strong>🚨 CRITICAL WASTAGE ALERT</strong><br>
                Wastage of <strong>{wastage_result['wastage_percentage']:.4f}%</strong> exceeds critical threshold ({CRITICAL_WASTAGE_THRESHOLD}%)!<br>
                <strong>Immediate investigation required!</strong><br>
                Allowable limit: {PRODUCTION_WASTAGE_LIMIT}% of MFM2 AL
            </div>
        """, unsafe_allow_html=True)
    elif not wastage_result['within_limit']:
        st.markdown(f"""
            <div class="wastage-warning">
                <strong>⚠️ WASTAGE EXCEEDS ALLOWABLE LIMIT</strong><br>
                Wastage of <strong>{wastage_result['wastage_percentage']:.4f}%</strong> exceeds allowable limit of {PRODUCTION_WASTAGE_LIMIT}%<br>
                Explanation required for excise compliance.<br>
                Wastage: {wastage_result['wastage_al']:.3f} AL out of {mfm2_al:.3f} AL passed through MFM2
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="wastage-ok">
                <strong>✅ WASTAGE WITHIN ALLOWABLE LIMIT</strong><br>
                Wastage of <strong>{wastage_result['wastage_percentage']:.4f}%</strong> is within allowable limit of {PRODUCTION_WASTAGE_LIMIT}%<br>
                Production efficiency: {((bottles_al / mfm2_al) * 100):.2f}%
            </div>
        """, unsafe_allow_html=True)
    
    return wastage_result


# Main Content
tab_entry, tab_admin = st.tabs(["🔒 SECURE DATA ENTRY", "📋 ADMINISTRATIVE VIEW"])

with tab_entry:
    st.markdown("## 🍾 Reg-A Production Register")
    st.subheader("Bottle Production & MFM2 Tracking")
    
    # SECTION 1: PRODUCTION DETAILS
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">SECTION 1 – PRODUCTION DETAILS</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        production_date = st.date_input("Production Date*", value=datetime.now())
    with col2:
        production_shift = st.selectbox("Production Shift*", PRODUCTION_SHIFTS)
    with col3:
        # Get available batches from Reg-74
        available_batches = rega_backend.get_available_batches()
        if not available_batches.empty and 'batch_no' in available_batches.columns:
            batch_list = ["Select Batch"] + available_batches['batch_no'].dropna().unique().tolist()
        else:
            batch_list = ["Select Batch"]
        
        batch_no = st.selectbox("Batch Number*", batch_list,
                               help="Select batch from Reg-74 reduction operations")
    with col4:
        if batch_no != "Select Batch":
            session_number = rega_backend.get_next_session_number(batch_no)
            st.text_input("Session Number", value=f"Session-{session_number}", disabled=True,
                         help="Auto-incremented for multi-day production")
        else:
            session_number = 1
            st.text_input("Session Number", value="Session-1", disabled=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Initialize variables
    mfm2_bl = mfm2_al = 0.0
    bottles_total_bl = bottles_total_al = 0.0
    brt_vat = ""
    brt_opening_bl = brt_opening_al = brt_opening_strength = 0.0
    
    if batch_no != "Select Batch":
        # Get batch details from Reg-74
        batch_details = rega_backend.get_batch_details(batch_no)
        
        if batch_details:
            brt_vat = batch_details['brt_vat']
            brt_opening_bl = batch_details['bl']
            brt_opening_al = batch_details['al']
            brt_opening_strength = batch_details['strength']
            ref_reg74_id = batch_details['reg74_id']
            
            # SECTION 2: BRT SOURCE DETAILS
            st.markdown('<div class="section-container">', unsafe_allow_html=True)
            st.markdown(f'<div class="section-header">SECTION 2 – SOURCE BRT DETAILS - {brt_vat}</div>', unsafe_allow_html=True)
            
            st.info(f"""
            📋 **Batch:** {batch_no} | **BRT VAT:** {brt_vat} | **Reg-74 ID:** {ref_reg74_id}  
            **Available Stock:** {brt_opening_bl:.3f} BL | {brt_opening_al:.3f} AL | {brt_opening_strength:.2f}% v/v
            """)
            
            c1, c2, c3 = st.columns(3)
            with c1:
                display_calc_result("Opening BL", brt_opening_bl, "L")
            with c2:
                display_calc_result("Opening AL", brt_opening_al, "L")
            with c3:
                display_calc_result("Strength", brt_opening_strength, "% v/v")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # SECTION 3: MFM2 READINGS
            st.markdown('<div class="section-container">', unsafe_allow_html=True)
            st.markdown('<div class="section-header">SECTION 3 – MFM2 READINGS (Production Mass Flow Meter)</div>', unsafe_allow_html=True)
            
            st.markdown("**MFM2 Meter Readings**")
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                mfm2_start = st.number_input("MFM2 Start Reading", min_value=0.0, step=0.001, format="%.3f",
                                            help="Meter reading at production start")
            with m2:
                mfm2_end = st.number_input("MFM2 End Reading*", min_value=0.0, step=0.001, format="%.3f",
                                          help="Meter reading at production end")
            with m3:
                mfm2_bl = mfm2_end - mfm2_start
                st.number_input("MFM2 Total BL*", value=mfm2_bl, disabled=True, format="%.3f",
                              help="Auto-calculated: End - Start")
            with m4:
                mfm2_al = mfm2_bl * (brt_opening_strength / 100)
                st.number_input("MFM2 Total AL*", value=mfm2_al, disabled=True, format="%.3f",
                              help="Auto-calculated: MFM2 BL × Strength / 100")
            
            st.markdown("**MFM2 Parameters**")
            p1, p2, p3 = st.columns(3)
            with p1:
                mfm2_temp = st.number_input("Temperature (°C)", value=20.0, step=0.1)
            with p2:
                mfm2_density = st.number_input("Density (gm/cc)", value=0.9652, step=0.0001, format="%.4f")
            with p3:
                st.number_input("Strength (% v/v)", value=brt_opening_strength, disabled=True, format="%.2f")
            
            # Validation
            if mfm2_bl > brt_opening_bl:
                st.error(f"❌ MFM2 reading ({mfm2_bl:.3f} BL) exceeds available BRT stock ({brt_opening_bl:.3f} BL)!")
            elif mfm2_bl > 0:
                st.success(f"✅ MFM2 reading valid. Remaining in BRT: {(brt_opening_bl - mfm2_bl):.3f} BL")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # SECTION 4: BOTTLE PRODUCTION
            st.markdown('<div class="section-container">', unsafe_allow_html=True)
            st.markdown('<div class="section-header">SECTION 4 – BOTTLE PRODUCTION</div>', unsafe_allow_html=True)
            
            st.markdown("**Bottle Counts (Enter number of bottles produced)**")
            b1, b2, b3, b4 = st.columns(4)
            with b1:
                bottles_180ml = st.number_input("180 ML Bottles", min_value=0, step=1, value=0)
            with b2:
                bottles_375ml = st.number_input("375 ML Bottles", min_value=0, step=1, value=0)
            with b3:
                bottles_750ml = st.number_input("750 ML Bottles", min_value=0, step=1, value=0)
            with b4:
                bottles_1000ml = st.number_input("1000 ML Bottles", min_value=0, step=1, value=0)
            
            # Calculate bottle volumes
            bottle_calc = calculate_bottles_bl(bottles_180ml, bottles_375ml, bottles_750ml, bottles_1000ml)
            bottles_total_bl = bottle_calc['total_bl']
            bottles_total_al = bottles_total_bl * (brt_opening_strength / 100)
            
            st.markdown("**Bottle Volume Summary**")
            v1, v2, v3, v4 = st.columns(4)
            with v1:
                st.metric("Total Bottles", f"{bottle_calc['total_bottles']:,}")
            with v2:
                st.metric("Total BL", f"{bottles_total_bl:.3f} L")
            with v3:
                st.metric("Total AL", f"{bottles_total_al:.3f} L")
            with v4:
                efficiency = (bottles_total_al / mfm2_al * 100) if mfm2_al > 0 else 0
                st.metric("Efficiency", f"{efficiency:.2f}%")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # SECTION 5: WASTAGE ANALYSIS
            if mfm2_bl > 0 and bottles_total_bl > 0:
                wastage_result = display_wastage_analysis(mfm2_bl, mfm2_al, bottles_total_bl, bottles_total_al, brt_opening_strength)
                
                # Wastage note if required
                if not wastage_result['within_limit']:
                    st.markdown('<div class="section-container">', unsafe_allow_html=True)
                    st.markdown('<div class="section-header">⚠️ WASTAGE EXPLANATION (MANDATORY)</div>', unsafe_allow_html=True)
                    wastage_note = st.text_area("Wastage Explanation*", 
                                               placeholder="Explain reason for wastage exceeding 0.1% limit...",
                                               height=100,
                                               help="Mandatory explanation for excise compliance")
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    wastage_note = ""
            else:
                wastage_result = None
                wastage_note = ""
            
            # SECTION 6: DISPATCH DETAILS
            st.markdown('<div class="section-container">', unsafe_allow_html=True)
            st.markdown('<div class="section-header">SECTION 6 – DISPATCH DETAILS</div>', unsafe_allow_html=True)
            
            d1, d2, d3, d4 = st.columns(4)
            with d1:
                dispatch_type = st.selectbox("Dispatch Type*", DISPATCH_TYPES)
            with d2:
                warehouse_location = st.text_input("Warehouse/Godown Location")
            with d3:
                dispatch_challan = st.text_input("Challan/Invoice No.")
            with d4:
                dispatch_date = st.date_input("Dispatch Date", value=datetime.now())
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # SECTION 7: PRODUCT & BRAND DETAILS
            st.markdown('<div class="section-container">', unsafe_allow_html=True)
            st.markdown('<div class="section-header">SECTION 7 – PRODUCT & BRAND DETAILS</div>', unsafe_allow_html=True)
            
            pr1, pr2, pr3, pr4 = st.columns(4)
            with pr1:
                brand_name = st.text_input("Brand Name", placeholder="e.g., Premium Whisky")
            with pr2:
                product_type = st.selectbox("Product Type", PRODUCT_TYPES)
            with pr3:
                label_reg_no = st.text_input("Label Registration No.")
            with pr4:
                mrp_per_bottle = st.number_input("MRP per Bottle (₹)", min_value=0.0, step=1.0)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # SECTION 8: APPROVAL & REMARKS
            st.markdown('<div class="section-container">', unsafe_allow_html=True)
            st.markdown('<div class="section-header">SECTION 8 – APPROVAL & REMARKS</div>', unsafe_allow_html=True)
            
            a1, a2, a3 = st.columns(3)
            with a1:
                production_officer = st.text_input("Production Officer Name*")
                production_officer_sig = st.date_input("Production Officer Signature Date", value=datetime.now())
            with a2:
                excise_officer = st.text_input("Excise Officer Name")
                excise_officer_sig = st.date_input("Excise Officer Signature Date", value=datetime.now())
            with a3:
                operation_remarks = st.text_area("Remarks", height=80)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # SUBMISSION
            if st.button("🚀 FINAL SUBMIT & LOCK PRODUCTION RECORD", use_container_width=True, type="primary"):
                # Validation
                errors = []
                if batch_no == "Select Batch":
                    errors.append("Please select a batch")
                if mfm2_bl <= 0:
                    errors.append("MFM2 reading must be greater than 0")
                if bottle_calc['total_bottles'] == 0:
                    errors.append("At least one bottle must be produced")
                if not production_officer:
                    errors.append("Production officer name is required")
                if wastage_result and not wastage_result['within_limit'] and not wastage_note:
                    errors.append("Wastage explanation is required (wastage exceeds 0.1% limit)")
                if mfm2_bl > brt_opening_bl:
                    errors.append("MFM2 reading exceeds available BRT stock")
                
                if errors:
                    for error in errors:
                        st.error(f"❌ {error}")
                else:
                    with st.spinner("Saving Production Record..."):
                        # Calculate closing balance
                        brt_closing_bl = brt_opening_bl - mfm2_bl
                        brt_closing_al = brt_opening_al - mfm2_al
                        
                        # Check if batch is complete
                        is_batch_complete = brt_closing_bl < 0.1
                        
                        payload = {
                            "production_date": str(production_date),
                            "production_shift": production_shift,
                            "session_number": session_number,
                            "batch_no": batch_no,
                            "ref_reg74_id": ref_reg74_id,
                            "source_brt_vat": brt_vat,
                            "brt_opening_bl": brt_opening_bl,
                            "brt_opening_al": brt_opening_al,
                            "brt_opening_strength": brt_opening_strength,
                            "brt_available_bl": brt_opening_bl,
                            "brt_available_al": brt_opening_al,
                            "mfm2_reading_bl": mfm2_bl,
                            "mfm2_reading_al": mfm2_al,
                            "mfm2_strength": brt_opening_strength,
                            "mfm2_temperature": mfm2_temp,
                            "mfm2_density": mfm2_density,
                            "mfm2_start_reading": mfm2_start,
                            "mfm2_end_reading": mfm2_end,
                            "mfm2_total_passed": mfm2_bl,
                            "bottles_180ml": bottles_180ml,
                            "bottles_375ml": bottles_375ml,
                            "bottles_750ml": bottles_750ml,
                            "bottles_1000ml": bottles_1000ml,
                            "total_bottles": bottle_calc['total_bottles'],
                            "bottles_bl_180ml": bottle_calc['bl_180'],
                            "bottles_bl_375ml": bottle_calc['bl_375'],
                            "bottles_bl_750ml": bottle_calc['bl_750'],
                            "bottles_bl_1000ml": bottle_calc['bl_1000'],
                            "bottles_total_bl": bottles_total_bl,
                            "bottles_total_al": bottles_total_al,
                            "wastage_bl": wastage_result['wastage_bl'] if wastage_result else 0.0,
                            "wastage_al": wastage_result['wastage_al'] if wastage_result else 0.0,
                            "wastage_percentage": wastage_result['wastage_percentage'] if wastage_result else 0.0,
                            "allowable_limit": PRODUCTION_WASTAGE_LIMIT,
                            "wastage_status": "Within Limit" if wastage_result and wastage_result['within_limit'] else "Exceeds Limit",
                            "wastage_note": wastage_note,
                            "brt_issue_bl": mfm2_bl,
                            "brt_issue_al": mfm2_al,
                            "brt_closing_bl": brt_closing_bl,
                            "brt_closing_al": brt_closing_al,
                            "brt_closing_strength": brt_opening_strength,
                            "dispatch_type": dispatch_type,
                            "warehouse_location": warehouse_location,
                            "dispatch_challan_no": dispatch_challan,
                            "dispatch_date": str(dispatch_date),
                            "brand_name": brand_name,
                            "product_type": product_type,
                            "label_registration_no": label_reg_no,
                            "mrp_per_bottle": mrp_per_bottle,
                            "production_officer_name": production_officer,
                            "production_officer_signature": str(production_officer_sig),
                            "excise_officer_name": excise_officer,
                            "excise_officer_signature": str(excise_officer_sig),
                            "approval_date": str(datetime.now().date()),
                            "operation_remarks": operation_remarks,
                            "is_batch_complete": is_batch_complete,
                            "remaining_in_brt_bl": brt_closing_bl,
                            "remaining_in_brt_al": brt_closing_al,
                            "status": "Submitted"
                        }
                        
                        rid = rega_backend.save_record(payload)
                        st.success(f"✅ Production Record Successfully Saved! Reg-A ID: {rid}")
                        
                        if is_batch_complete:
                            st.info(f"🎉 Batch {batch_no} is now complete! All spirit from BRT-{brt_vat} has been bottled.")
                        else:
                            st.info(f"📊 Remaining in BRT-{brt_vat}: {brt_closing_bl:.3f} BL / {brt_closing_al:.3f} AL")
                        
                        time.sleep(2)
                        st.rerun()
        else:
            st.warning(f"⚠️ Batch {batch_no} not found in Reg-74 records. Please check the batch number.")
    else:
        st.info("👆 Please select a batch to start production entry.")

with tab_admin:
    st.subheader("Reg-A Administrative Control")
    
    # Filter Controls
    with st.expander("🔍 Search & Filter", expanded=True):
        f1, f2, f3 = st.columns(3)
        with f1: f_date = st.date_input("Filter by Date", value=None)
        with f2: f_batch = st.text_input("Filter by Batch No.", placeholder="BATCH-001")
        with f3: f_shift = st.selectbox("Filter by Shift", ["All"] + PRODUCTION_SHIFTS)
    
    # Data Table
    records = rega_backend.filter_records(date_from=f_date, batch_no=f_batch if f_batch else None, shift=f_shift)
    
    if records.empty:
        st.info("No production records found in the system.")
    else:
        st.dataframe(
            records[[
                "rega_id", "production_date", "batch_no", "source_brt_vat",
                "total_bottles", "bottles_total_al", "wastage_percentage", "status"
            ]],
            use_container_width=True,
            hide_index=True
        )
        
        st.info(f"""
        📊 **Data Storage**: {len(records)} production records stored in `RegA_Data.xlsx` (Desktop Excel)
        with a CSV backup in `rega_data.csv`, and synced to Google Sheets (RegA worksheet).
        """)
        
        st.divider()
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            csv = records.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Export to Excel (CSV)", 
                data=csv, 
                file_name=f"RegA_Export_{datetime.now().strftime('%Y%m%d')}.csv"
            )
        with col_btn2:
            if st.button("🔄 Sync with GSheet", type="secondary"):
                with st.spinner("Synchronizing..."):
                    local_df = rega_backend.get_data_local()
                    if local_df.empty:
                        st.info("No local records to sync.")
                    else:
                        success = rega_backend.sync_to_gsheet(local_df)
                        if success:
                            st.success("✅ GSheet updated with local records!")
                            st.rerun()
                        else:
                            st.error("GSheet sync failed.")
