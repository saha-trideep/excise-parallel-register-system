import streamlit as st
from auth import login_required

# Apply Authentication
login_required()

from datetime import date, datetime, timedelta
from decimal import Decimal
import pandas as pd
from typing import Dict, List

# Import modules
from excise_duty_schema import (
    ExciseDutyLedger,
    ExciseDutyBottle,
    DUTY_RATES,
    BOTTLE_SIZES_ML,
    STRENGTH_OPTIONS,
    get_duty_rate_for_strength,
    get_strength_label
)
from excise_duty_backend import (
    init_excise_duty_database,
    save_duty_ledger,
    get_duty_ledger,
    get_previous_day_duty_closing,
    save_duty_bottle,
    get_duty_bottles_for_date,
    get_regb_issued_bottles,
    generate_duty_summary,
    save_duty_summary,
    delete_duty_entry
)
from excise_duty_utils import (
    calculate_duty_for_bottles,
    calculate_total_duty,
    calculate_duty_balance,
    validate_duty_balance,
    validate_sufficient_balance,
    format_currency,
    format_litres,
    format_bottles,
    format_duty_rate,
    get_all_duty_rates,
    aggregate_bottle_summary,
    calculate_duty_by_strength
)

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Excise Duty Register - IML",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS
# ============================================================================

st.markdown("""
<style>
    /* Main header */
    .main-header {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* Section headers */
    .section-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem 1.5rem;
        border-radius: 8px;
        color: white;
        margin: 1.5rem 0 1rem 0;
        font-size: 1.3rem;
        font-weight: 600;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .section-header-orange {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
    }
    
    .section-header-green {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
    }
    
    .section-header-blue {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    
    /* Info boxes */
    .info-box {
        background: #f0f7ff;
        border-left: 4px solid #2196F3;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    
    .success-box {
        background: #f0fff4;
        border-left: 4px solid #48bb78;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: #fffaf0;
        border-left: 4px solid #ed8936;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    
    .duty-rate-box {
        background: #fff5f5;
        border-left: 4px solid #f56565;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# INITIALIZE DATABASE
# ============================================================================

@st.cache_resource
def initialize_database():
    """Initialize database on app start"""
    return init_excise_duty_database()

initialize_database()

# ============================================================================
# HEADER
# ============================================================================

st.markdown("""
<div class="main-header">
    <h1>💰 EXCISE DUTY REGISTER</h1>
    <p>Register of Personal Ledger Account of Excise Duty for IML</p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("### 📅 Date Selection")
    
    selected_date = st.date_input(
        "Select Date",
        value=date.today(),
        max_value=date.today(),
        help="Select the date for duty entry"
    )
    
    st.markdown("---")
    
    # Auto-fill controls
    st.markdown("### 🔄 Auto-Fill Options")
    
    auto_fill_regb = st.checkbox(
        "Auto-fill from Reg-B Issues",
        value=True,
        help="Automatically fetch issued bottles from Reg-B"
    )
    
    auto_fill_opening = st.checkbox(
        "Auto-fill Opening Balance",
        value=True,
        help="Use previous day's closing as opening"
    )
    
    st.markdown("---")
    
    # Duty Rates Display
    st.markdown("### 💵 Duty Rates")
    
    duty_rates = get_all_duty_rates()
    for label, rate in duty_rates.items():
        st.markdown(f"**{label}**")
        st.markdown(f"→ {format_duty_rate(rate)}")
    
    st.markdown("---")
    
    # View mode
    st.markdown("### 👁️ View Mode")
    view_mode = st.radio(
        "Select View",
        ["Data Entry", "Summary View"],
        help="Choose how to view duty register"
    )
    
    st.markdown("---")
    
    # Actions
    st.markdown("### ⚙️ Actions")
    
    if st.button("🗑️ Delete Entry", use_container_width=True):
        if delete_duty_entry(selected_date):
            st.success(f"Deleted entry for {selected_date}")
            st.rerun()
        else:
            st.error("Failed to delete entry")
    
    if st.button("📊 Generate Summary", use_container_width=True):
        summary = generate_duty_summary(selected_date)
        if summary and save_duty_summary(summary):
            st.success("Summary generated!")
        else:
            st.error("Failed to generate summary")

# ============================================================================
# MAIN CONTENT
# ============================================================================

if view_mode == "Data Entry":
    
    # Get existing ledger
    existing_ledger = get_duty_ledger(selected_date)
    
    # Auto-fill opening balance
    if auto_fill_opening and not existing_ledger:
        previous_closing = get_previous_day_duty_closing(selected_date)
    else:
        previous_closing = existing_ledger.opening_balance if existing_ledger else Decimal("0.00")
    
    # Get Reg-B issued bottles
    regb_data = {}
    if auto_fill_regb:
        regb_data = get_regb_issued_bottles(selected_date)
        if regb_data['total_bottles'] > 0:
            st.markdown(f"""
            <div class="success-box">
                <strong>✅ Auto-filled from Reg-B:</strong><br>
                Total Bottles Issued: <strong>{regb_data['total_bottles']:,}</strong><br>
                Total BL: <strong>{regb_data['total_bl']:.3f}</strong><br>
                Total Duty: <strong>{format_currency(regb_data['total_duty'])}</strong>
            </div>
            """, unsafe_allow_html=True)
    
    # ========================================================================
    # SECTION 1: FINANCIAL ACCOUNT
    # ========================================================================
    
    st.markdown('<div class="section-header section-header-orange">💰 SECTION 1: FINANCIAL ACCOUNT</div>', unsafe_allow_html=True)
    
    with st.form("financial_account_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### Opening & Deposits")
            opening_balance = st.number_input(
                "Opening Balance (₹)",
                min_value=0.0,
                value=float(previous_closing),
                step=100.0,
                format="%.2f",
                help="Opening balance from previous day"
            )
            
            deposit_amount = st.number_input(
                "Deposit Amount (₹)",
                min_value=0.0,
                value=float(existing_ledger.deposit_amount) if existing_ledger else 0.0,
                step=100.0,
                format="%.2f",
                help="Deposit made today"
            )
            
            amount_credited = opening_balance + deposit_amount
            st.metric("Amount Credited", format_currency(Decimal(str(amount_credited))))
        
        with col2:
            st.markdown("#### E-Challan Details")
            echallan_no = st.text_input(
                "E-Challan Number",
                value=existing_ledger.echallan_no if existing_ledger and existing_ledger.echallan_no else "",
                help="E-Challan number for deposit"
            )
            
            echallan_date = st.date_input(
                "E-Challan Date",
                value=existing_ledger.echallan_date if existing_ledger and existing_ledger.echallan_date else selected_date,
                max_value=selected_date,
                help="Date of E-Challan"
            )
        
        with col3:
            st.markdown("#### Duty Summary")
            total_duty = regb_data.get('total_duty', Decimal("0.00")) if auto_fill_regb else Decimal("0.00")
            
            st.metric("Total Duty", format_currency(total_duty))
            
            closing_balance = Decimal(str(amount_credited)) - total_duty
            st.metric("Closing Balance", format_currency(closing_balance))
            
            if closing_balance < 0:
                st.error("⚠️ Insufficient balance!")
        
        st.markdown("---")
        
        # Issue Details
        st.markdown("#### Issue Details")
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            name_of_issue = st.text_input(
                "Name of Issue (Customer/Distributor)",
                value=existing_ledger.name_of_issue if existing_ledger and existing_ledger.name_of_issue else "",
                help="Name of customer or distributor"
            )
        
        with col_b:
            warehouse_no = st.text_input(
                "Warehouse Number",
                value=existing_ledger.warehouse_no if existing_ledger and existing_ledger.warehouse_no else "",
                help="Warehouse number"
            )
        
        with col_c:
            transport_permit_no = st.text_input(
                "Transport Permit Number",
                value=existing_ledger.transport_permit_no if existing_ledger and existing_ledger.transport_permit_no else "",
                help="Transport permit number (required)"
            )
        
        st.markdown("---")
        
        # Remarks
        remarks = st.text_area(
            "Remarks",
            value=existing_ledger.remarks if existing_ledger and existing_ledger.remarks else "",
            height=80,
            help="Any additional remarks"
        )
        
        # Submit
        submit_ledger = st.form_submit_button("💾 Save Financial Account", use_container_width=True)
        
        if submit_ledger:
            # Create ledger object
            ledger = ExciseDutyLedger(
                date=selected_date,
                opening_balance=Decimal(str(opening_balance)),
                deposit_amount=Decimal(str(deposit_amount)),
                echallan_no=echallan_no if echallan_no else None,
                echallan_date=echallan_date,
                amount_credited=Decimal(str(amount_credited)),
                name_of_issue=name_of_issue if name_of_issue else None,
                warehouse_no=warehouse_no if warehouse_no else None,
                transport_permit_no=transport_permit_no if transport_permit_no else None,
                total_duty_amount=total_duty,
                duty_debited=total_duty,
                closing_balance=closing_balance,
                remarks=remarks if remarks else None,
                status="submitted"
            )
            
            # Validate
            if validate_duty_balance(ledger.amount_credited, ledger.duty_debited, ledger.closing_balance):
                if validate_sufficient_balance(ledger.amount_credited, ledger.duty_debited):
                    if save_duty_ledger(ledger):
                        st.success("✅ Financial account saved successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to save financial account")
                else:
                    st.error("❌ Insufficient balance to cover duty!")
            else:
                st.error("❌ Balance validation failed!")
    
    # ========================================================================
    # SECTION 2: BOTTLE ISSUES
    # ========================================================================
    
    st.markdown('<div class="section-header section-header-green">🍾 SECTION 2: ISSUED BOTTLES</div>', unsafe_allow_html=True)
    
    # Display auto-filled bottles from Reg-B
    if auto_fill_regb and regb_data.get('bottles'):
        st.markdown("#### Auto-filled from Reg-B")
        
        bottles_df_data = []
        for bottle in regb_data['bottles']:
            bottles_df_data.append({
                'Product': bottle['product_name'],
                'Strength': get_strength_label(bottle['strength']),
                'Size (ml)': bottle['bottle_size_ml'],
                'Qty Issued': bottle['qty_issued'],
                'BL Issued': f"{bottle['bl_issued']:.3f}",
                'AL Issued': f"{bottle['al_issued']:.3f}",
                'Duty Rate': format_duty_rate(bottle['duty_rate_per_bl']),
                'Duty Amount': format_currency(bottle['duty_amount'])
            })
        
        bottles_df = pd.DataFrame(bottles_df_data)
        st.dataframe(bottles_df, use_container_width=True, hide_index=True)
        
        # Save all bottles button
        if st.button("💾 Save All Issued Bottles", use_container_width=True):
            success_count = 0
            for bottle_data in regb_data['bottles']:
                bottle = ExciseDutyBottle(
                    date=selected_date,
                    product_name=bottle_data['product_name'],
                    strength=bottle_data['strength'],
                    bottle_size_ml=bottle_data['bottle_size_ml'],
                    qty_issued=bottle_data['qty_issued'],
                    bl_issued=bottle_data['bl_issued'],
                    al_issued=bottle_data['al_issued'],
                    duty_rate_per_bl=bottle_data['duty_rate_per_bl'],
                    duty_amount=bottle_data['duty_amount'],
                    status="submitted"
                )
                if save_duty_bottle(bottle):
                    success_count += 1
            
            if success_count == len(regb_data['bottles']):
                st.success(f"✅ Saved {success_count} bottle issues!")
                st.rerun()
            else:
                st.warning(f"⚠️ Saved {success_count} of {len(regb_data['bottles'])} bottles")
    
    # Manual entry option
    st.markdown("---")
    st.markdown("#### Manual Bottle Entry")
    
    with st.form("manual_bottle_form"):
        col_p1, col_p2, col_p3, col_p4 = st.columns(4)
        
        with col_p1:
            product_name = st.text_input("Product Name", value="Country Liquor")
        
        with col_p2:
            strength_labels = {
                Decimal("28.5"): "50° U.P. (28.5% v/v)",
                Decimal("22.8"): "60° U.P. (22.8% v/v)",
                Decimal("17.1"): "70° U.P. (17.1% v/v)",
                Decimal("11.4"): "80° U.P. (11.4% v/v)"
            }
            strength = st.selectbox(
                "Strength",
                options=STRENGTH_OPTIONS,
                format_func=lambda x: strength_labels.get(x, f"{x}% v/v")
            )
        
        with col_p3:
            bottle_size = st.selectbox(
                "Bottle Size (ml)",
                options=BOTTLE_SIZES_ML,
                format_func=lambda x: f"{x}ml"
            )
        
        with col_p4:
            qty_issued = st.number_input(
                "Quantity Issued",
                min_value=0,
                step=1
            )
        
        # Calculate duty
        if qty_issued > 0:
            duty_calc = calculate_duty_for_bottles(qty_issued, bottle_size, Decimal(str(strength)))
            
            st.markdown("##### Calculated Values")
            col_c1, col_c2, col_c3, col_c4 = st.columns(4)
            
            with col_c1:
                st.metric("BL Issued", format_litres(duty_calc['bl_issued'], 'BL'))
            with col_c2:
                st.metric("AL Issued", format_litres(duty_calc['al_issued'], 'AL'))
            with col_c3:
                st.metric("Duty Rate", format_duty_rate(duty_calc['duty_rate_per_bl']))
            with col_c4:
                st.metric("Duty Amount", format_currency(duty_calc['duty_amount']))
        
        submit_manual = st.form_submit_button("💾 Save Manual Entry", use_container_width=True)
        
        if submit_manual and qty_issued > 0:
            bottle = ExciseDutyBottle(
                date=selected_date,
                product_name=product_name,
                strength=Decimal(str(strength)),
                bottle_size_ml=bottle_size,
                qty_issued=duty_calc['qty_issued'],
                bl_issued=duty_calc['bl_issued'],
                al_issued=duty_calc['al_issued'],
                duty_rate_per_bl=duty_calc['duty_rate_per_bl'],
                duty_amount=duty_calc['duty_amount'],
                status="submitted"
            )
            
            if save_duty_bottle(bottle):
                st.success("✅ Manual entry saved!")
                st.rerun()
            else:
                st.error("❌ Failed to save manual entry")

elif view_mode == "Summary View":
    
    # ========================================================================
    # SUMMARY VIEW
    # ========================================================================
    
    st.markdown('<div class="section-header section-header-blue">📊 DAILY SUMMARY</div>', unsafe_allow_html=True)
    
    summary = generate_duty_summary(selected_date)
    
    if summary:
        # Financial Summary
        st.markdown("### 💰 Financial Summary")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Opening", format_currency(summary.opening_balance))
        with col2:
            st.metric("Deposit", format_currency(summary.deposit_amount))
        with col3:
            st.metric("Credited", format_currency(summary.amount_credited))
        with col4:
            st.metric("Duty Debited", format_currency(summary.duty_debited))
        with col5:
            st.metric("Closing", format_currency(summary.closing_balance))
        
        st.markdown("---")
        
        # Bottle Summary
        st.markdown("### 🍾 Bottle Summary")
        col_b1, col_b2, col_b3, col_b4 = st.columns(4)
        
        with col_b1:
            st.metric("Total Bottles", f"{summary.total_bottles_issued:,}")
        with col_b2:
            st.metric("Total BL", f"{summary.total_bl_issued:.3f}")
        with col_b3:
            st.metric("Total AL", f"{summary.total_al_issued:.3f}")
        with col_b4:
            st.metric("Total Duty", format_currency(summary.total_duty))
        
        # Duty by Strength
        bottles = get_duty_bottles_for_date(selected_date)
        if bottles:
            st.markdown("---")
            st.markdown("### 📋 Duty Breakdown by Strength")
            
            breakdown = calculate_duty_by_strength([{
                'strength': b.strength,
                'qty_issued': b.qty_issued,
                'bl_issued': b.bl_issued,
                'al_issued': b.al_issued,
                'duty_amount': b.duty_amount
            } for b in bottles])
            
            breakdown_df_data = []
            for label, data in breakdown.items():
                breakdown_df_data.append({
                    'Strength': label,
                    'Duty Rate': format_duty_rate(data['rate']),
                    'Bottles': f"{data['qty']:,}",
                    'BL': f"{data['bl']:.3f}",
                    'AL': f"{data['al']:.3f}",
                    'Duty': format_currency(data['duty'])
                })
            
            breakdown_df = pd.DataFrame(breakdown_df_data)
            st.dataframe(breakdown_df, use_container_width=True, hide_index=True)
    else:
        st.info("ℹ️ No data available for the selected date")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p><strong>Excise Duty Register - Register of Personal Ledger Account of Excise Duty for IML</strong></p>
    <p>Excise Parallel Register System | SIP 2 LIFE DISTILLERIES</p>
</div>
""", unsafe_allow_html=True)
