import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import time
import importlib
import reg78_backend
from reg78_schema import PRODUCTION_FEES_RATE_PER_BL, ALL_VATS, SST_VATS, BRT_VATS, SAMPLE_PURPOSES

# Reload backend to get latest changes
importlib.reload(reg78_backend)

# Page Configuration
st.set_page_config(
    page_title="Reg-78 Daily Synopsis",
    page_icon="📊",
    layout="wide",
)

# Ultra-Compact Dark Mode CSS (same as Reg-A)
st.markdown("""
    <style>
    .stApp { background-color: #0a0e1a; }
    
    .stTextInput input, .stNumberInput input, .stSelectbox select, 
    .stDateInput input, .stTextArea textarea {
        background-color: #1a1f2e !important;
        border: 1px solid: #3b82f6 !important;
        color: #e8edf5 !important;
        padding: 6px 10px !important;
        height: 38px !important;
        font-size: 0.9rem !important;
    }
    
    .stTextArea textarea { height: 80px !important; }
    
    .stTextInput label, .stNumberInput label, .stSelectbox label,
    .stDateInput label, .stTextArea label {
        color: #cbd5e0 !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        margin-bottom: 4px !important;
    }
    
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
    
    .auto-fill-success {
        background: linear-gradient(135deg, #064e3b 0%, #022c22 100%);
        border: 1px solid #10b981;
        padding: 15px;
        border-radius: 8px;
        color: #d1fae5;
        margin: 15px 0;
    }
    
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
    
    [data-testid="column"] { padding: 0 6px; }
    
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
    
    .stDataFrame { background-color: #1a1f2e; }
    .stAlert { background-color: #1a1f2e; border-radius: 6px; padding: 12px; }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 20px 10px; background: linear-gradient(135deg, #1e3a5f 0%, #0f1e3a 100%); border-radius: 10px; margin-bottom: 20px;'>
            <h2 style='color: #4f9eff; margin: 0; font-size: 1.5rem;'>📊 Reg-78</h2>
            <p style='color: #94a3b8; margin: 5px 0 0 0; font-size: 0.85rem;'>Daily Synopsis</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    register = st.radio(
        "Register Selection",
        ["Reg-76 – Spirit Receipt",
         "Reg-74 – Spirit Operations", 
         "Reg-A – Production",
         "▶ Reg-78 – Daily Synopsis"],
        index=3
    )
    
    if "Reg-76" in register:
        st.info("💡 To access Reg-76, run: `streamlit run reg76.py`")
        st.stop()
    elif "Reg-74" in register:
        st.info("💡 To access Reg-74, run: `streamlit run reg74.py`")
        st.stop()
    elif "Reg-A" in register:
        st.info("💡 To access Reg-A, run: `streamlit run rega.py`")
        st.stop()

# Helper Functions
def display_metric_card(label, value, unit=""):
    st.markdown(f"""
        <div class="metric-card">
            <small>{label}</small>
            <span>{value:.3f} {unit}</span>
        </div>
    """, unsafe_allow_html=True)

# Main Content
tab_entry, tab_admin = st.tabs(["🔒 SECURE DATA ENTRY", "📋 ADMINISTRATIVE VIEW"])

with tab_entry:
    st.markdown("## 📊 Reg-78 Daily Synopsis Register")
    st.subheader("Automated Daily Summary of All Spirit Operations")
    
    # Date Selection
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">SELECT DATE FOR SYNOPSIS</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        synopsis_date = st.date_input("Synopsis Date*", value=datetime.now().date())
    with col2:
        synopsis_hour = st.time_input("End of Day Hour", value=datetime.strptime("18:00", "%H:%M").time())
    with col3:
        if st.button("🤖 AUTO-FILL FROM REGISTERS", type="primary", use_container_width=True):
            with st.spinner("Aggregating data from all registers..."):
                st.session_state.auto_filled = True
                st.session_state.synopsis_data = reg78_backend.generate_daily_synopsis(synopsis_date)
                time.sleep(1)
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Check if auto-filled
    if 'auto_filled' in st.session_state and st.session_state.auto_filled:
        synopsis = st.session_state.synopsis_data
        
        st.markdown("""
            <div class="auto-fill-success">
                <strong>✅ AUTO-FILL SUCCESSFUL!</strong><br>
                Data automatically aggregated from Reg-76, Reg-74, and Reg-A for {date}<br>
                Review the synopsis below and add manual entries if needed.
            </div>
        """.format(date=synopsis_date), unsafe_allow_html=True)
        
        # SECTION 1: OPENING BALANCE & RECEIPTS (CREDIT SIDE)
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">SECTION 1 – OPENING BALANCE & RECEIPTS (CREDIT SIDE)</div>', unsafe_allow_html=True)
        
        st.markdown("**Opening Balance (from previous day)**")
        c1, c2 = st.columns(2)
        with c1:
            opening_bl = st.number_input("Opening BL", value=synopsis['opening_balance_bl'], disabled=True, format="%.3f")
        with c2:
            opening_al = st.number_input("Opening AL", value=synopsis['opening_balance_al'], disabled=True, format="%.3f")
        
        st.markdown("**Consignment Received (from Reg-76)**")
        r1, r2, r3, r4 = st.columns(4)
        with r1:
            consignment_count = st.number_input("No. of Consignments", value=synopsis['consignment_count'], disabled=True)
        with r2:
            consignment_pass = st.text_input("Pass Numbers", value=synopsis['consignment_pass_numbers'], disabled=True)
        with r3:
            consignment_bl = st.number_input("Received BL", value=synopsis['consignment_received_bl'], disabled=True, format="%.3f")
        with r4:
            consignment_al = st.number_input("Received AL", value=synopsis['consignment_received_al'], disabled=True, format="%.3f")
        
        st.markdown("**MFM1 Readings (from Reg-76)**")
        m1, m2 = st.columns(2)
        with m1:
            mfm1_bl = st.number_input("MFM1 Total BL", value=synopsis['mfm1_total_bl'], disabled=True, format="%.3f")
        with m2:
            mfm1_al = st.number_input("MFM1 Total AL", value=synopsis['mfm1_total_al'], disabled=True, format="%.3f")
        
        st.markdown("**Manual Entries (if any)**")
        man1, man2, man3 = st.columns(3)
        with man1:
            operational_increase_bl = st.number_input("Operational Increase BL", value=0.0, step=0.001, format="%.3f")
            operational_increase_al = st.number_input("Operational Increase AL", value=0.0, step=0.001, format="%.3f")
        with man2:
            production_increase_bl = st.number_input("Production Increase BL", value=0.0, step=0.001, format="%.3f")
            production_increase_al = st.number_input("Production Increase AL", value=0.0, step=0.001, format="%.3f")
        with man3:
            audit_increase_bl = st.number_input("Audit Increase BL", value=0.0, step=0.001, format="%.3f")
            audit_increase_al = st.number_input("Audit Increase AL", value=0.0, step=0.001, format="%.3f")
        
        # Calculate total credit
        total_credit_bl = (synopsis['total_credit_bl'] + operational_increase_bl + 
                          production_increase_bl + audit_increase_bl)
        total_credit_al = (synopsis['total_credit_al'] + operational_increase_al + 
                          production_increase_al + audit_increase_al)
        
        st.markdown("**Total Balance (Credit Side)**")
        tc1, tc2 = st.columns(2)
        with tc1:
            st.metric("Total Credit BL", f"{total_credit_bl:.3f} L")
        with tc2:
            st.metric("Total Credit AL", f"{total_credit_al:.3f} L")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # SECTION 2: ISSUES (DEBIT SIDE)
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">SECTION 2 – ISSUES (DEBIT SIDE)</div>', unsafe_allow_html=True)
        
        st.markdown("**Issues on Payment of Production Fees (from Reg-A)**")
        st.info(f"""
        📋 **Production Fees Calculation**: ₹{PRODUCTION_FEES_RATE_PER_BL:.2f} per BL  
        **Total BL Produced Today**: {synopsis['production_total_bl']:.3f} BL  
        **Total Production Fees Payable**: ₹{synopsis['total_production_fees']:.2f}
        """)
        
        d1, d2, d3 = st.columns(3)
        with d1:
            issues_bl = st.number_input("Issues BL", value=synopsis['issues_on_duty_bl'], disabled=True, format="%.3f")
        with d2:
            issues_al = st.number_input("Issues AL", value=synopsis['issues_on_duty_al'], disabled=True, format="%.3f")
        with d3:
            production_fees = st.number_input("Production Fees (₹)", value=synopsis['total_production_fees'], disabled=True, format="%.2f")
        
        st.markdown("**Sample Drawn (Manual Entry)**")
        s1, s2, s3 = st.columns(3)
        with s1:
            sample_bl = st.number_input("Sample BL", value=0.0, step=0.001, format="%.3f")
        with s2:
            sample_al = st.number_input("Sample AL", value=0.0, step=0.001, format="%.3f")
        with s3:
            sample_purpose = st.selectbox("Sample Purpose", SAMPLE_PURPOSES)
        
        st.markdown("**Wastage (Auto-filled from Reg-74 & Reg-A)**")
        w1, w2, w3, w4 = st.columns(4)
        with w1:
            op_wastage_bl = st.number_input("Operational Wastage BL", value=synopsis['operational_wastage_bl'], disabled=True, format="%.3f")
        with w2:
            op_wastage_al = st.number_input("Operational Wastage AL", value=synopsis['operational_wastage_al'], disabled=True, format="%.3f")
        with w3:
            prod_wastage_bl = st.number_input("Production Wastage BL", value=synopsis['production_wastage_bl'], disabled=True, format="%.3f")
        with w4:
            prod_wastage_al = st.number_input("Production Wastage AL", value=synopsis['production_wastage_al'], disabled=True, format="%.3f")
        
        st.markdown("**Audit Wastage (Manual Entry)**")
        aw1, aw2 = st.columns(2)
        with aw1:
            audit_wastage_bl = st.number_input("Audit Wastage BL", value=0.0, step=0.001, format="%.3f")
        with aw2:
            audit_wastage_al = st.number_input("Audit Wastage AL", value=0.0, step=0.001, format="%.3f")
        
        # Calculate total debit
        total_debit_bl = (synopsis['total_debit_bl'] + sample_bl + audit_wastage_bl)
        total_debit_al = (synopsis['total_debit_al'] + sample_al + audit_wastage_al)
        
        st.markdown("**Total Debit**")
        td1, td2 = st.columns(2)
        with td1:
            st.metric("Total Debit BL", f"{total_debit_bl:.3f} L")
        with td2:
            st.metric("Total Debit AL", f"{total_debit_al:.3f} L")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # SECTION 3: CLOSING BALANCE
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">SECTION 3 – CLOSING BALANCE (SPIRIT LEFT IN VATS)</div>', unsafe_allow_html=True)
        
        # Calculate closing
        closing_bl = total_credit_bl - total_debit_bl
        closing_al = total_credit_al - total_debit_al
        
        st.markdown("**Total Closing Balance**")
        cb1, cb2 = st.columns(2)
        with cb1:
            st.metric("Closing BL", f"{closing_bl:.3f} L", delta=f"{closing_bl - opening_bl:.3f}")
        with cb2:
            st.metric("Closing AL", f"{closing_al:.3f} L", delta=f"{closing_al - opening_al:.3f}")
        
        st.markdown("**VAT-wise Breakdown (from Reg-74)**")
        
        # SST Vats
        st.markdown("**SST Vats (Storage)**")
        sst_cols = st.columns(len(SST_VATS))
        for idx, vat in enumerate(SST_VATS):
            with sst_cols[idx]:
                vat_data = synopsis['vat_balances'].get(vat, {"bl": 0.0, "al": 0.0})
                st.metric(vat, f"{vat_data['bl']:.1f} BL", f"{vat_data['al']:.1f} AL")
        
        # BRT Vats
        st.markdown("**BRT Vats (Blending/Reduction)**")
        brt_cols = st.columns(len(BRT_VATS))
        for idx, vat in enumerate(BRT_VATS):
            with brt_cols[idx]:
                vat_data = synopsis['vat_balances'].get(vat, {"bl": 0.0, "al": 0.0})
                st.metric(vat, f"{vat_data['bl']:.1f} BL", f"{vat_data['al']:.1f} AL")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # SECTION 4: PRODUCTION FEES SUMMARY
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">SECTION 4 – PRODUCTION FEES SUMMARY</div>', unsafe_allow_html=True)
        
        ds1, ds2, ds3, ds4 = st.columns(4)
        with ds1:
            st.metric("Total Bottles Produced", f"{synopsis['total_bottles_produced']:,}")
        with ds2:
            st.metric("Total BL Produced", f"{synopsis['production_total_bl']:.3f} L")
        with ds3:
            fees_payable = st.number_input("Production Fees Payable (₹)", value=synopsis['production_fees_payable'], disabled=True, format="%.2f")
        with ds4:
            fees_paid = st.number_input("Production Fees Paid (₹)*", value=0.0, step=1.0, format="%.2f")
        
        fees_pending = fees_payable - fees_paid
        if fees_pending > 0:
            st.warning(f"⚠️ Pending Production Fees: ₹{fees_pending:.2f}")
        else:
            st.success(f"✅ All production fees paid for {synopsis_date}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # SECTION 5: APPROVAL & REMARKS
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">SECTION 5 – APPROVAL & REMARKS</div>', unsafe_allow_html=True)
        
        a1, a2, a3 = st.columns(3)
        with a1:
            prepared_by = st.text_input("Prepared By*")
            verified_by = st.text_input("Verified By*")
        with a2:
            excise_officer = st.text_input("Excise Officer Name")
            excise_sig_date = st.date_input("Excise Signature Date", value=datetime.now().date())
        with a3:
            remarks = st.text_area("Remarks", height=100)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # SUBMISSION
        if st.button("🚀 FINAL SUBMIT & LOCK DAILY SYNOPSIS", use_container_width=True, type="primary"):
            errors = []
            if not prepared_by:
                errors.append("Prepared by name is required")
            if not verified_by:
                errors.append("Verified by name is required")
            
            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
            else:
                with st.spinner("Saving Daily Synopsis..."):
                    # Build VAT breakdown
                    vat_data = {}
                    for vat in ALL_VATS:
                        vat_balance = synopsis['vat_balances'].get(vat, {"bl": 0.0, "al": 0.0})
                        vat_key = vat.lower().replace('-', '')
                        vat_data[f"{vat_key}_closing_bl"] = vat_balance['bl']
                        vat_data[f"{vat_key}_closing_al"] = vat_balance['al']
                    
                    payload = {
                        "synopsis_date": str(synopsis_date),
                        "synopsis_hour": str(synopsis_hour),
                        "opening_balance_bl": opening_bl,
                        "opening_balance_al": opening_al,
                        "consignment_count": consignment_count,
                        "consignment_pass_numbers": consignment_pass,
                        "consignment_received_bl": consignment_bl,
                        "consignment_received_al": consignment_al,
                        "mfm1_total_bl": mfm1_bl,
                        "mfm1_total_al": mfm1_al,
                        "operational_increase_bl": operational_increase_bl,
                        "operational_increase_al": operational_increase_al,
                        "production_increase_bl": production_increase_bl,
                        "production_increase_al": production_increase_al,
                        "audit_increase_bl": audit_increase_bl,
                        "audit_increase_al": audit_increase_al,
                        "total_credit_bl": total_credit_bl,
                        "total_credit_al": total_credit_al,
                        "production_total_bl": synopsis['production_total_bl'],
                        "production_total_al": synopsis['production_total_al'],
                        "production_fees_rate": PRODUCTION_FEES_RATE_PER_BL,
                        "total_production_fees": production_fees,
                        "issues_on_duty_bl": issues_bl,
                        "issues_on_duty_al": issues_al,
                        "sample_drawn_bl": sample_bl,
                        "sample_drawn_al": sample_al,
                        "sample_purpose": sample_purpose,
                        "operational_wastage_bl": op_wastage_bl,
                        "operational_wastage_al": op_wastage_al,
                        "production_wastage_bl": prod_wastage_bl,
                        "production_wastage_al": prod_wastage_al,
                        "audit_wastage_bl": audit_wastage_bl,
                        "audit_wastage_al": audit_wastage_al,
                        "total_debit_bl": total_debit_bl,
                        "total_debit_al": total_debit_al,
                        "closing_balance_bl": closing_bl,
                        "closing_balance_al": closing_al,
                        **vat_data,
                        "total_bottles_produced": synopsis['total_bottles_produced'],
                        "total_al_in_bottles": synopsis['total_al_in_bottles'],
                        "production_fees_payable": fees_payable,
                        "production_fees_paid": fees_paid,
                        "production_fees_pending": fees_pending,
                        "prepared_by": prepared_by,
                        "verified_by": verified_by,
                        "excise_officer_name": excise_officer,
                        "excise_officer_signature": str(excise_sig_date),
                        "approval_date": str(datetime.now().date()),
                        "remarks": remarks,
                        "status": "Submitted"
                    }
                    
                    rid = reg78_backend.save_record(payload)
                    st.success(f"✅ Daily Synopsis Successfully Saved! Reg-78 ID: {rid}")
                    st.balloons()
                    time.sleep(2)
                    
                    # Clear auto-fill state
                    st.session_state.auto_filled = False
                    st.rerun()
    else:
        st.info("👆 Select a date and click **AUTO-FILL FROM REGISTERS** to generate the daily synopsis automatically!")
        
        st.markdown("""
        ### 🤖 **Smart Auto-Fill Features:**
        
        - ✅ **Opening Balance**: From previous day's Reg-78 closing
        - ✅ **Receipts**: All Reg-76 consignments for the day
        - ✅ **MFM1 Readings**: Aggregated from Reg-76
        - ✅ **Production**: All Reg-A production for the day
        - ✅ **Production Fees Calculation**: Automatic (₹3/- per BL produced)
        - ✅ **Wastage**: Storage (Reg-74) + Production (Reg-A)
        - ✅ **VAT Balances**: Latest closing from Reg-74
        - ✅ **Closing Balance**: Auto-calculated (Credit - Debit)
        
        **Just one click to fill the entire synopsis!** 🚀
        """)

with tab_admin:
    st.subheader("Reg-78 Administrative Control")
    
    # Filter Controls
    with st.expander("🔍 Search & Filter", expanded=True):
        f1, f2 = st.columns(2)
        with f1: f_date_from = st.date_input("From Date", value=None)
        with f2: f_date_to = st.date_input("To Date", value=None)
    
    # Data Table
    records = reg78_backend.filter_records(date_from=f_date_from, date_to=f_date_to)
    
    if records.empty:
        st.info("No daily synopsis records found in the system.")
    else:
        st.dataframe(
            records[[
                "reg78_id", "synopsis_date", "total_credit_al", "total_debit_al",
                "closing_balance_al", "production_fees_payable", "status"
            ]],
            use_container_width=True,
            hide_index=True
        )
        
        st.info(f"""
        📊 **Data Storage**: {len(records)} daily synopsis records stored locally in `reg78_data.csv` 
        and synced to Google Sheets (Reg78 worksheet).
        """)
        
        st.divider()
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            csv = records.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Export to Excel (CSV)", 
                data=csv, 
                file_name=f"Reg78_Export_{datetime.now().strftime('%Y%m%d')}.csv"
            )
        with col_btn2:
            if st.button("🔄 Sync with GSheet", type="secondary"):
                with st.spinner("Synchronizing..."):
                    local_df = reg78_backend.get_data_local()
                    if local_df.empty:
                        st.info("No local records to sync.")
                    else:
                        success = reg78_backend.sync_to_gsheet(local_df)
                        if success:
                            st.success("✅ GSheet updated with local records!")
                            st.rerun()
                        else:
                            st.error("GSheet sync failed.")
