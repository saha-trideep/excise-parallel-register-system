import streamlit as st
from auth import login_required

login_required()

from datetime import datetime
import time
import spirit_transaction_backend as st_backend

st.set_page_config(
    page_title="Spirit Transaction",
    page_icon="📈",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp { background-color: #0a0e1a; }

    .section-container {
        background: linear-gradient(135deg, #1a1f2e 0%, #0f1419 100%);
        padding: 15px 18px;
        border-radius: 8px;
        margin-bottom: 12px;
        border-left: 3px solid #f59e0b;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }

    .section-header {
        color: #f59e0b;
        font-size: 0.95rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 12px;
        padding-bottom: 6px;
        border-bottom: 2px solid #f59e0b;
    }

    .metric-card {
        background: linear-gradient(135deg, #1e3a5f 0%, #0f1e3a 100%);
        padding: 12px;
        border-radius: 6px;
        border: 1px solid #f59e0b;
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

    .stTextInput input, .stNumberInput input, .stSelectbox select, 
    .stDateInput input, .stTextArea textarea {
        background-color: #1a1f2e !important;
        border: 1px solid: #f59e0b !important;
        color: #e8edf5 !important;
        padding: 6px 10px !important;
        height: 38px !important;
        font-size: 0.9rem !important;
    }

    .stTextInput label, .stNumberInput label, .stSelectbox label,
    .stDateInput label, .stTextArea label {
        color: #cbd5e0 !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        margin-bottom: 4px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown(
        """
        <div style='text-align: center; padding: 20px 10px; background: linear-gradient(135deg, #3b2f0a 0%, #201a05 100%); border-radius: 10px; margin-bottom: 20px;'>
            <h2 style='color: #f59e0b; margin: 0; font-size: 1.5rem;'>📈 Spirit Transaction</h2>
            <p style='color: #fbbf24; margin: 5px 0 0 0; font-size: 0.85rem;'>Daily Spirit Summary</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.info("Auto-populates from Reg-76, Reg-74, Reg-A, and Reg-78.")

tab_entry, tab_admin = st.tabs(["🧾 DATA ENTRY", "📋 ADMIN VIEW"])

with tab_entry:
    st.markdown("## 📈 Spirit Transaction Register")
    st.subheader("Daily Summary of Strong/Blended Spirit, Production, and Wastage")

    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Select Date</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        txn_date = st.date_input("Transaction Date*", value=datetime.now().date())
    with col2:
        if st.button("🤖 AUTO-COMPUTE", type="primary", use_container_width=True):
            with st.spinner("Computing from registers..."):
                st.session_state.spirit_txn_data = st_backend.compute_spirit_transaction_row(
                    txn_date
                )
                time.sleep(0.5)
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    if "spirit_txn_data" not in st.session_state:
        st.info("Select a date and click AUTO-COMPUTE to load register values.")
        st.stop()

    row = st.session_state.spirit_txn_data

    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Strong Spirit (Columns 2-8)</div>', unsafe_allow_html=True)
    s1, s2, s3 = st.columns(3)
    with s1:
        strong_opening = st.number_input(
            "Strong Spirit Opening Balance (AL)",
            value=float(row.get("strong_spirit_opening_balance", 0.0)),
            format="%.3f",
        )
        transit_increase = st.number_input(
            "In-transit / Unloading Increase (AL)",
            value=float(row.get("in_transit_unloading_increase", 0.0)),
            format="%.3f",
        )
        strong_oper_increase = st.number_input(
            "Operational Increase in Strong Spirit (AL)",
            value=float(row.get("operational_increase_strong_spirit", 0.0)),
            format="%.3f",
        )
    with s2:
        strong_received = st.number_input(
            "Strong Spirit Received / Unloaded (AL)",
            value=float(row.get("strong_spirit_received_unloaded", 0.0)),
            format="%.3f",
        )
        transit_wastage = st.number_input(
            "In-transit / Unloading Wastage (AL)",
            value=float(row.get("in_transit_unloading_wastage", 0.0)),
            format="%.3f",
        )
        strong_transferred = st.number_input(
            "Strong Spirit Transferred to Blending (AL)",
            value=float(row.get("strong_spirit_transferred_to_blending", 0.0)),
            format="%.3f",
        )
    with s3:
        strong_closing = st.number_input(
            "Strong Spirit Closing Balance (AL)",
            value=float(row.get("strong_spirit_closing_balance", 0.0)),
            format="%.3f",
        )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Blended / Finished Spirit (Columns 9-15)</div>', unsafe_allow_html=True)
    b1, b2, b3 = st.columns(3)
    with b1:
        blended_opening = st.number_input(
            "Blended Spirit Opening Balance (AL)",
            value=float(row.get("blended_spirit_opening_balance", 0.0)),
            format="%.3f",
        )
        blended_oper_increase = st.number_input(
            "Operational Increase in Blended Spirit (AL)",
            value=float(row.get("operational_increase_blended_spirit", 0.0)),
            format="%.3f",
        )
        sample_drawn = st.number_input(
            "Sample Drawn (AL)",
            value=float(row.get("sample_drawn", 0.0)),
            format="%.3f",
        )
    with b2:
        blended_received = st.number_input(
            "Blended Spirit Received from Strong (AL)",
            value=float(row.get("blended_spirit_received_from_strong", 0.0)),
            format="%.3f",
        )
        blended_oper_wastage = st.number_input(
            "Operational Wastage in Blended Spirit (AL)",
            value=float(row.get("operational_wastage_blended_spirit", 0.0)),
            format="%.3f",
        )
        spirit_passed = st.number_input(
            "Spirit Passed to Bottling (AL)",
            value=float(row.get("spirit_passed_to_bottling", 0.0)),
            format="%.3f",
        )
    with b3:
        blended_closing = st.number_input(
            "Blended Spirit Closing Balance (AL)",
            value=float(row.get("blended_spirit_closing_balance", 0.0)),
            format="%.3f",
        )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Production & Wastage (Columns 16-23)</div>', unsafe_allow_html=True)
    p1, p2, p3 = st.columns(3)
    with p1:
        production_increase = st.number_input(
            "Production Increase (AL)",
            value=float(row.get("production_increase", 0.0)),
            format="%.3f",
        )
        total_bottles = st.number_input(
            "Total Bottles Produced",
            value=int(row.get("total_bottles_produced", 0)),
            step=1,
        )
        spirit_accounted = st.number_input(
            "Spirit Accounted in Bottled Production (AL)",
            value=float(row.get("spirit_accounted_in_bottled_production", 0.0)),
            format="%.3f",
        )
    with p2:
        production_wastage = st.number_input(
            "Production Wastage (AL)",
            value=float(row.get("production_wastage", 0.0)),
            format="%.3f",
        )
        total_cases = st.number_input(
            "Total Cases Produced",
            value=int(row.get("total_cases_produced", 0)),
            step=1,
        )
        total_allowable = st.number_input(
            "Total Allowable Wastage (AL)",
            value=float(row.get("total_allowable_wastage", 0.0)),
            format="%.3f",
        )
    with p3:
        st.markdown(
            """
            <div class="metric-card">
                <small>Auto-Calculated</small>
                <span>Net Difference & Chargeable</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    credits = (
        strong_opening
        + strong_received
        + transit_increase
        + strong_oper_increase
        + blended_opening
        + blended_received
        + blended_oper_increase
        + production_increase
    )
    debits = (
        transit_wastage
        + strong_transferred
        + blended_oper_wastage
        + sample_drawn
        + spirit_passed
        + production_wastage
    )
    expected_closing = credits - debits
    actual_closing = strong_closing + blended_closing
    net_difference = actual_closing - expected_closing

    actual_wastage = transit_wastage + blended_oper_wastage + production_wastage
    chargeable_excess = max(0.0, actual_wastage - total_allowable)

    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Reconciliation & Totals</div>', unsafe_allow_html=True)
    r1, r2, r3 = st.columns(3)
    with r1:
        st.metric("Total Credits (AL)", f"{credits:.3f}")
        st.metric("Total Debits (AL)", f"{debits:.3f}")
    with r2:
        st.metric("Expected Closing (AL)", f"{expected_closing:.3f}")
        st.metric("Actual Closing (AL)", f"{actual_closing:.3f}")
    with r3:
        st.metric("Net Difference (AL)", f"{net_difference:.3f}")
        st.metric("Chargeable Excess Wastage (AL)", f"{chargeable_excess:.3f}")
    st.markdown("</div>", unsafe_allow_html=True)

    recon_status, recon_note = st_backend.validate_reconciliation(
        {
            "strong_spirit_closing_balance": strong_closing,
            "blended_spirit_closing_balance": blended_closing,
        },
        txn_date,
    )

    if recon_status == "ok":
        st.success(f"Reconciliation OK: {recon_note}")
    else:
        st.warning(f"Reconciliation Warning: {recon_note}")

    if st.button("💾 Save Spirit Transaction", type="primary", use_container_width=True):
        payload = {
            "txn_date": str(txn_date),
            "strong_spirit_opening_balance": strong_opening,
            "strong_spirit_received_unloaded": strong_received,
            "in_transit_unloading_increase": transit_increase,
            "in_transit_unloading_wastage": transit_wastage,
            "strong_spirit_transferred_to_blending": strong_transferred,
            "operational_increase_strong_spirit": strong_oper_increase,
            "strong_spirit_closing_balance": strong_closing,
            "blended_spirit_opening_balance": blended_opening,
            "blended_spirit_received_from_strong": blended_received,
            "operational_increase_blended_spirit": blended_oper_increase,
            "operational_wastage_blended_spirit": blended_oper_wastage,
            "sample_drawn": sample_drawn,
            "spirit_passed_to_bottling": spirit_passed,
            "blended_spirit_closing_balance": blended_closing,
            "production_increase": production_increase,
            "production_wastage": production_wastage,
            "total_bottles_produced": int(total_bottles),
            "total_cases_produced": int(total_cases),
            "spirit_accounted_in_bottled_production": spirit_accounted,
            "net_difference": net_difference,
            "total_allowable_wastage": total_allowable,
            "chargeable_excess_wastage": chargeable_excess,
            "recon_status": recon_status,
            "recon_note": recon_note,
            "status": "Submitted",
        }

        with st.spinner("Saving Spirit Transaction..."):
            record_id = st_backend.save_record(payload)
            if record_id:
                st.success(f"✅ Spirit Transaction saved for {record_id}")
                time.sleep(0.5)
                st.rerun()

with tab_admin:
    st.subheader("Spirit Transaction Admin View")
    with st.expander("🔍 Search & Filter", expanded=True):
        f1, f2 = st.columns(2)
        with f1:
            f_date_from = st.date_input("From Date", value=None, key="st_date_from")
        with f2:
            f_date_to = st.date_input("To Date", value=None, key="st_date_to")

    records = st_backend.get_spirit_transaction(date_from=f_date_from, date_to=f_date_to)
    if records.empty:
        st.info("No Spirit Transaction records found.")
    else:
        st.dataframe(
            records[
                [
                    "txn_date",
                    "strong_spirit_opening_balance",
                    "strong_spirit_closing_balance",
                    "blended_spirit_opening_balance",
                    "blended_spirit_closing_balance",
                    "net_difference",
                    "recon_status",
                    "status",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )
