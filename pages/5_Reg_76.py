import streamlit as st
from auth import login_required

# Apply Authentication
login_required()

import pandas as pd
from datetime import datetime
import time
from utils import calculate_bl, calculate_al, calculate_transit_days, calculate_wastage, validate_wb
import reg76_backend

# Page Configuration
st.set_page_config(
    page_title="Reg-76 Spirit Receipt",
    page_icon="🥃",
    layout="wide",
)

# Custom CSS for Dark Mode Optimized Design
st.markdown("""
    <style>
    /* Global Dark Mode Styles */
    .stApp {
        background-color: #0e1117;
    }
    
    /* Input Fields - High Contrast for Dark Mode */
    .stTextInput input, .stNumberInput input, .stSelectbox select, .stDateInput input {
        background-color: #1e2530 !important;
        border: 2px solid #4a5568 !important;
        color: #f7fafc !important;
        font-weight: 500;
    }
    
    .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox select:focus {
        border-color: #60a5fa !important;
        box-shadow: 0 0 0 1px #60a5fa !important;
    }
    
    /* Section Containers - Dark Cards */
    .section-container {
        background-color: #1a1f2e;
        padding: 25px;
        border-radius: 10px;
        margin-bottom: 25px;
        border: 1px solid #2d3748;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    .section-header {
        font-size: 1.15rem;
        font-weight: 800;
        color: #60a5fa;
        margin-bottom: 20px;
        border-bottom: 3px solid #3b82f6;
        padding-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    
    /* Metric Cards - Vibrant for Dark Mode */
    .metric-card {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d4a6f 100%);
        padding: 18px;
        border-radius: 8px;
        border: 2px solid #3b82f6;
        text-align: center;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
    }
    
    .metric-card small {
        color: #93c5fd !important;
        font-weight: 600;
    }
    
    .metric-card span {
        color: #e0f2fe !important;
    }
    
    /* Labels - High Visibility */
    label, .stMarkdown p, label p {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    
    /* Buttons - Enhanced */
    .stButton button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 6px;
        padding: 0.6rem 1.2rem;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
        transform: translateY(-1px);
    }
    
    /* Dataframe styling */
    .stDataFrame {
        background-color: #1a1f2e;
        border-radius: 8px;
    }
    
    /* Info/Warning/Success boxes */
    .stAlert {
        background-color: #1e2530 !important;
        border-left: 4px solid #3b82f6 !important;
        color: #e2e8f0 !important;
    }
    
    /* Sidebar enhancement */
    section[data-testid="stSidebar"] {
        background-color: #0f1419;
        border-right: 1px solid #2d3748;
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: #e2e8f0;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #1a1f2e;
        padding: 10px;
        border-radius: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #2d3748;
        color: #cbd5e0;
        border-radius: 6px;
        padding: 10px 20px;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #1e2530;
        color: #e2e8f0 !important;
        border-radius: 6px;
        font-weight: 600;
    }
    
    /* Metric widget override */
    [data-testid="stMetricValue"] {
        color: #60a5fa !important;
        font-size: 1.5rem !important;
    }
    
    [data-testid="stMetricDelta"] {
        color: #93c5fd !important;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    # Custom header with emoji icon
    st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <div style='font-size: 4rem; margin-bottom: 10px;'>🚛</div>
            <h2 style='color: #60a5fa; margin: 0; font-weight: 800;'>Excise Register</h2>
            <p style='color: #94a3b8; font-size: 0.85rem; margin-top: 5px;'>Reg-76 Spirit Receipt System</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sync Status
    gs_client = reg76_backend.get_google_client()
    if gs_client:
        st.success("🟢 Connected to Google Sheets")
    else:
        st.warning("🟡 Using Local Storage (CSV)")
        with st.expander("How to Sync with GSheets"):
            st.write("1. Create a Service Account in Google Cloud.")
            st.write("2. Add the JSON key to `.streamlit/secrets.toml`.")
            st.write("3. Share your sheet with the service account email.")

    st.divider()
    register = st.radio(
        "Register Selection",
        ["▶ Reg-76 – Spirit Receipt", 
         "⏸ Reg-74 – (Disabled)", 
         "⏸ Reg-A – (Disabled)"],
        index=0
    )
    st.info("Phase-1: Reg-76 Active Only")

if "Reg-76" not in register:
    st.warning("This section is restricted in Phase-1.")
    st.stop()

# Helper to format metrics
def display_calc_result(label, value, unit=""):
    st.markdown(f"""
        <div class="metric-card">
            <small style="color: #64748b;">{label}</small><br>
            <span style="font-size: 1.1rem; font-weight: 600; color: #0f172a;">{value:.2f} {unit}</span>
        </div>
    """, unsafe_allow_html=True)

# Tabs
tab_entry, tab_admin = st.tabs(["🔒 SECURE DATA ENTRY", "📋 ADMINISTRATIVE VIEW"])

with tab_entry:
    st.subheader("Reg-76 Spirit Receipt Form")
    
    with st.container():
        # SECTION 1: BASIC DETAILS
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">SECTION 1 – BASIC CONSIGNMENT DETAILS</div>', unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            permit_no = st.text_input("Import Permit / Transport Pass No.*", key="p_no")
            dist_source = ["Select Distillery", "Globus Spirits", "Associated Distilleries", "IFB Agro", "Other (Manual)"]
            distillery = st.selectbox("Exporting Distillery", dist_source)
            if distillery == "Other (Manual)":
                distillery = st.text_input("Enter Distillery Name (Manual)")
            spirit_nature = st.selectbox("Nature of Spirit", ["ENA", "GENA", "RS", "Ethanol"])
        
        with c2:
            vehicle_no = st.text_input("Vehicle / Tanker No.*", help="e.g. WB-23-A-1234")
            num_tankers = st.number_input("No. of Tanker", value=1, disabled=True)
            tanker_cap = st.selectbox("Capacity of Tanker", ["Full", "Partial"])
            make_model = st.text_input("Make & Model of Tanker")
            
        with c3:
            invoice_no = st.text_input("Invoice No.")
            invoice_date = st.date_input("Invoice Date", value=datetime.now())
            pass_no = st.text_input("Export / Import Pass No.")
            pass_date = st.date_input("Pass Date", value=datetime.now())

        col_a, col_b = st.columns(2)
        with col_a:
            ex_order_no = st.text_input("Export Order No.")
            ex_order_date = st.date_input("Export Order Date", key="eo_date")
        with col_b:
            im_order_no = st.text_input("Import Order No.")
            im_order_date = st.date_input("Import Order Date", key="io_date")
        st.markdown('</div>', unsafe_allow_html=True)

        # SECTION 2: DATE & MOVEMENT
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">SECTION 2 – DATE & MOVEMENT</div>', unsafe_allow_html=True)
        c4, c5, c6 = st.columns(3)
        with c4:
            date_dispatch = st.date_input("Date of Dispatch")
        with c5:
            date_arrival = st.date_input("Date of Arrival")
        with c6:
            date_receipt = st.date_input("Date of Receipt & Examination")
            
        transit_days = calculate_transit_days(date_dispatch, date_receipt)
        st.info(f"🚚 Transit Duration: **{transit_days} days**")
        st.markdown('</div>', unsafe_allow_html=True)

        # SECTION 3: ADVISED QUANTITY
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">SECTION 3 – ADVISED QUANTITY (AS PER PASS)</div>', unsafe_allow_html=True)
        c7, c8, c9, c10 = st.columns(4)
        with c7:
            adv_w = st.number_input("Weight in Advice (kg)", min_value=0.0, step=0.001, format="%.3f")
        with c8:
            adv_d = st.number_input("Avg Density (gm/cc)", min_value=0.0, step=0.0001, format="%.4f")
        with c9:
            adv_s = st.number_input("Strength (% v/v)", min_value=0.0, max_value=100.0, step=0.01)
        with c10:
            adv_t = st.number_input("Temperature (°C)", value=20.0, step=0.1)
            
        adv_bl = calculate_bl(adv_w, adv_d)
        adv_al = calculate_al(adv_bl, adv_s)
        # BL at 20C calculation placeholder (assuming Density at 20C is same as Avg Density if not separate)
        adv_bl_20c = adv_bl 
        
        m1, m2, m3 = st.columns(3)
        with m1: display_calc_result("Advised BL", adv_bl, "L")
        with m2: display_calc_result("Advised AL", adv_al, "L")
        with m3: display_calc_result("Advised BL at 20°C", adv_bl_20c, "L")
        st.markdown('</div>', unsafe_allow_html=True)

        # SECTION 4: WEIGH BRIDGE
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">SECTION 4 – WEIGH BRIDGE DATA</div>', unsafe_allow_html=True)
        w1, w2 = st.columns(2)
        with w1:
            st.markdown("**At Consignee (Present)**")
            wb_l_c = st.number_input("Laden (kg)", key="wblc")
            wb_u_c = st.number_input("Unladen (kg)", key="wbuc")
            net_c = wb_l_c - wb_u_c
            st.caption(f"Net Weight: {net_c:.2f} kg")
        with w2:
            st.markdown("**As per Pass**")
            wb_l_p = st.number_input("Laden (kg)", key="wblp")
            wb_u_p = st.number_input("Unladen (kg)", key="wbup")
            net_p = wb_l_p - wb_u_p
            st.caption(f"Net Weight: {net_p:.2f} kg")
        
        if abs(net_c - adv_w) > 50:
            st.warning(f"⚠️ Net weight deviation detected: {abs(net_c - adv_w):.2f} kg")
        st.markdown('</div>', unsafe_allow_html=True)

        # SECTION 5: RECEIVED QUANTITY (MFM-1)
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">SECTION 5 – RECEIVED QUANTITY (MFM-1)</div>', unsafe_allow_html=True)
        r1, r2, r3 = st.columns(3)
        with r1:
            rec_m = st.number_input("Mass received (kg) - MFM", step=0.001, format="%.3f")
            rec_t = st.number_input("Avg Unloading Temp", value=20.0, step=0.1)
        with r2:
            rec_d_t = st.number_input("Density @ Temp", step=0.0001, format="%.4f")
            rec_d_20 = st.number_input("Density @ 20°C", step=0.0001, format="%.4f")
        with r3:
            rec_s = st.number_input("Strength % v/v (MFM)", step=0.01)
            
        rec_bl = calculate_bl(rec_m, rec_d_t)
        rec_al = calculate_al(rec_bl, rec_s)
        diff_al = rec_al - adv_al
        
        m4, m5, m6 = st.columns(3)
        with m4: display_calc_result("Received BL", rec_bl, "L")
        with m5: display_calc_result("Received AL", rec_al, "L")
        with m6: display_calc_result("Variance vs Advice", diff_al, "AL")
        st.markdown('</div>', unsafe_allow_html=True)

        # SECTION 6: WASTAGE
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">SECTION 6 – TRANSIT WASTAGE / INCREASE</div>', unsafe_allow_html=True)
        
        diff_al_raw = adv_al - rec_al
        if diff_al_raw >= 0:
            wastage_al = diff_al_raw
            increase_val = 0.0
            label_w = "Transit Wastage (AL)"
            color_w = "normal"
        else:
            wastage_al = 0.0
            increase_val = abs(diff_al_raw)
            label_w = "Transit Increase (AL)"
            color_w = "inverse"
            
        allowable_al = 0.0
        chargeable_al = max(0.0, wastage_al - allowable_al)
        
        v1, v2, v3, v4 = st.columns(4)
        with v1: st.metric(label_w, f"{wastage_al:.3f}", delta=f"-{wastage_al:.3f}" if wastage_al > 0 else None, delta_color=color_w)
        with v2: st.metric("Transit Increase (AL)", f"{increase_val:.3f}", delta=f"+{increase_val:.3f}" if increase_val > 0 else None)
        with v3: st.metric("Allowable (AL)", f"{allowable_al:.3f}")
        with v4: st.metric("Chargeable (AL)", f"{chargeable_al:.3f}", delta=f"-{chargeable_al:.3f}" if chargeable_al > 0 else None, delta_color="inverse")
        st.markdown('</div>', unsafe_allow_html=True)

        # SECTION 7 & 8: DESTINATION & REMARKS
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">SECTION 7 & 8 – DESTINATION & REMARKS</div>', unsafe_allow_html=True)
        col_end1, col_end2 = st.columns(2)
        with col_end1:
            vat_no = st.selectbox("Storage VAT No.*", ["Select VAT"] + [f"SST-{i}" for i in range(5, 11)])
            evc_date = st.date_input("Online EVC Date")
        with col_end2:
            remarks = st.text_area("Official Remarks")
            officer_tag = st.text_input("Officer Name / Signature Tag")
        st.markdown('</div>', unsafe_allow_html=True)

        # Submission
        if st.button("🚀 FINAL SUBMIT & LOCK RECORD", use_container_width=True, type="primary"):
            if not permit_no or not vehicle_no or vat_no == "Select VAT":
                st.error("❌ Mandatory fields missing. Please check Sections 1 and 7.")
            else:
                with st.spinner("Writing to Register..."):
                    payload = {
                        "permit_no": permit_no,
                        "distillery": distillery,
                        "spirit_nature": spirit_nature,
                        "vehicle_no": vehicle_no,
                        "num_tankers": num_tankers,
                        "tanker_capacity": tanker_cap,
                        "tanker_make_model": make_model,
                        "invoice_no": invoice_no,
                        "invoice_date": str(invoice_date),
                        "export_pass_no": pass_no,
                        "export_pass_date": str(pass_date),
                        "date_dispatch": str(date_dispatch),
                        "date_arrival": str(date_arrival),
                        "date_receipt": str(date_receipt),
                        "days_in_transit": transit_days,
                        "adv_weight_kg": adv_w,
                        "adv_avg_density": adv_d,
                        "adv_strength": adv_s,
                        "adv_temp": adv_t,
                        "adv_bl": adv_bl,
                        "adv_al": adv_al,
                        "wb_laden_consignee": wb_l_c,
                        "wb_unladen_consignee": wb_u_c,
                        "rec_mass_kg": rec_m,
                        "rec_unload_temp": rec_t,
                        "rec_density_at_temp": rec_d_t,
                        "rec_strength": rec_s,
                        "rec_bl": rec_bl,
                        "rec_al": rec_al,
                        "diff_advised_al": diff_al,
                        "transit_wastage_al": wastage_al,
                        "transit_increase_al": increase_val,
                        "chargeable_wastage_al": chargeable_al,
                        "storage_vat_no": vat_no,
                        "evc_generated_date": str(evc_date),
                        "excise_remarks": remarks,
                        "status": "Submitted"
                    }
                    rid = reg76_backend.save_record(payload)
                    st.success(f"✅ Record Successfully Saved. Reg-76 ID: {rid}")
                    time.sleep(2)
                    st.rerun()

with tab_admin:
    st.subheader("Reg-76 Administrative Control")
    
    # Filter Controls
    with st.expander("🔍 Search & Filter", expanded=True):
        f1, f2, f3 = st.columns(3)
        with f1: f_date = st.date_input("Filter by Date", value=None)
        with f2: f_tanker = st.text_input("Filter by Tanker No.")
        with f3: f_vat = st.selectbox("Filter by VAT", ["All"] + [f"SST-{i}" for i in range(5, 11)])
    
    # Data Table
    records = reg76_backend.filter_records(date_from=f_date, tanker_no=f_tanker)
    
    if records.empty:
        st.info("No records found in the system.")
    else:
        # Additional VAT filter (handled in UI for simplicity)
        if f_vat != "All":
            records = records[records['storage_vat_no'] == f_vat]
            
        st.dataframe(
            records[["reg76_id", "created_at", "vehicle_no", "permit_no", "adv_al", "rec_al", "transit_wastage_al", "status", "storage_vat_no"]],
            use_container_width=True,
            hide_index=True
        )
        
        # Data Storage Info
        st.info(f"""
        📊 **Data Storage**: {len(records)} records stored locally in `reg76_data.csv` 
        and synced to Google Sheets. Local file serves as backup and ensures zero data loss.
        """)
        
        st.divider()
        col_btn1, col_btn2, col_sync = st.columns([1, 1, 1])
        with col_btn1:
            csv = records.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Export to Excel (CSV)", data=csv, file_name=f"Reg76_Export_{datetime.now().strftime('%Y%m%d')}.csv")
        with col_btn2:
            if st.button("📄 Generate Official PDF", type="primary"):
                try:
                    from pdf_generator import generate_reg76_pdf
                    import os
                    
                    # Generate PDF
                    pdf_filename = f"Reg76_Official_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                    generate_reg76_pdf(records, pdf_filename)
                    
                    # Read the PDF file
                    with open(pdf_filename, "rb") as pdf_file:
                        pdf_bytes = pdf_file.read()
                    
                    # Offer download
                    st.download_button(
                        label="⬇️ Download PDF",
                        data=pdf_bytes,
                        file_name=pdf_filename,
                        mime="application/pdf",
                        type="primary"
                    )
                    
                    # Clean up
                    if os.path.exists(pdf_filename):
                        os.remove(pdf_filename)
                    
                    st.success("✅ PDF generated successfully!")
                except Exception as e:
                    st.error(f"PDF generation failed: {e}")
        with col_sync:
            if st.button("🔄 Sync with GSheet", type="secondary", help="Push all local records to Google Sheet"):
                with st.spinner("Synchronizing..."):
                    local_df = reg76_backend.get_data_local()
                    if local_df.empty:
                        st.info("No local records to sync.")
                    else:
                        success = reg76_backend.sync_to_gsheet(local_df)
                        if success:
                            st.success("✅ GSheet updated with local records!")
                            st.rerun()
                        else:
                            st.error("GSheet sync failed. Check if you have shared the sheet with the service account email.")
