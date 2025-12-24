"""
Reg-B - Issue of Country Liquor in Bottles
Streamlit application for finished goods inventory and production fees tracking
"""

import streamlit as st
from datetime import date, datetime, timedelta
from decimal import Decimal
import pandas as pd
from typing import Dict, List

# Import backend modules
from regb_schema import (
    ProductionFeesAccount,
    BottleStockInventory,
    FEE_PER_BOTTLE,
    BOTTLE_SIZES_ML,
    STRENGTH_OPTIONS
)
from regb_backend import (
    init_regb_database,
    save_production_fees,
    get_production_fees,
    get_previous_day_closing_balance,
    save_bottle_stock,
    get_bottle_stock_for_date,
    get_previous_day_stock,
    get_rega_production_data,
    generate_daily_summary,
    save_daily_summary,
    delete_regb_entry
)
from regb_utils import (
    calculate_bl_from_bottles,
    calculate_al_from_bl,
    calculate_production_fees,
    calculate_complete_stock_movement,
    format_currency,
    format_litres,
    format_bottles,
    validate_stock_balance,
    validate_fees_balance,
    calculate_wastage_percentage
)

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Reg-B - Issue of Country Liquor in Bottles",
    page_icon="🍾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS
# ============================================================================

st.markdown("""
<style>
    /* Main container styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem 1.5rem;
        border-radius: 8px;
        color: white;
        margin: 1.5rem 0 1rem 0;
        font-size: 1.3rem;
        font-weight: 600;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .section-header-blue {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    
    .section-header-green {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
    }
    
    .section-header-orange {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
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
    
    /* Metric cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Tables */
    .dataframe {
        font-size: 0.9rem;
    }
    
    .dataframe th {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        padding: 0.75rem;
    }
    
    .dataframe td {
        padding: 0.5rem;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# INITIALIZE DATABASE
# ============================================================================

@st.cache_resource
def initialize_database():
    """Initialize database on app start"""
    return init_regb_database()

# Initialize
initialize_database()

# ============================================================================
# HEADER
# ============================================================================

st.markdown("""
<div class="main-header">
    <h1>🍾 REG-B - ISSUE OF COUNTRY LIQUOR IN BOTTLES</h1>
    <p>Production Fees Account & Bottle Stock Inventory Management</p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR - DATE SELECTION & CONTROLS
# ============================================================================

with st.sidebar:
    st.markdown("### 📅 Date Selection")
    
    selected_date = st.date_input(
        "Select Date",
        value=date.today(),
        max_value=date.today(),
        help="Select the date for Reg-B entry"
    )
    
    st.markdown("---")
    
    # Auto-fill controls
    st.markdown("### 🔄 Auto-Fill Options")
    
    auto_fill_production = st.checkbox(
        "Auto-fill from Reg-A Production",
        value=True,
        help="Automatically fetch production data from Reg-A"
    )
    
    auto_fill_opening = st.checkbox(
        "Auto-fill Opening Balances",
        value=True,
        help="Use previous day's closing as today's opening"
    )
    
    st.markdown("---")
    
    # View mode
    st.markdown("### 👁️ View Mode")
    view_mode = st.radio(
        "Select View",
        ["Data Entry", "Summary View", "Administrative View"],
        help="Choose how to view Reg-B data"
    )
    
    st.markdown("---")
    
    # Actions
    st.markdown("### ⚙️ Actions")
    
    if st.button("🗑️ Delete Entry", use_container_width=True):
        if delete_regb_entry(selected_date):
            st.success(f"Deleted entry for {selected_date}")
            st.rerun()
        else:
            st.error("Failed to delete entry")
    
    if st.button("📊 Generate Summary", use_container_width=True):
        summary = generate_daily_summary(selected_date)
        if summary and save_daily_summary(summary):
            st.success("Summary generated successfully!")
        else:
            st.error("Failed to generate summary")

# ============================================================================
# MAIN CONTENT
# ============================================================================

if view_mode == "Data Entry":
    
    # ========================================================================
    # SECTION 1: PRODUCTION FEES ACCOUNT
    # ========================================================================
    
    st.markdown('<div class="section-header section-header-blue">💰 SECTION 1: PRODUCTION FEES ACCOUNT</div>', unsafe_allow_html=True)
    
    # Get existing fees data or create new
    existing_fees = get_production_fees(selected_date)
    
    # Auto-fill opening balance from previous day
    if auto_fill_opening and not existing_fees:
        previous_closing = get_previous_day_closing_balance(selected_date)
    else:
        previous_closing = existing_fees.opening_balance if existing_fees else Decimal("0.00")
    
    # Get production data from Reg-A
    production_data = {}
    if auto_fill_production:
        production_data = get_rega_production_data(selected_date)
        st.markdown(f"""
        <div class="info-box">
            <strong>📦 Auto-filled from Reg-A Production:</strong><br>
            Total Bottles Produced: <strong>{production_data.get('total_bottles_produced', 0):,}</strong><br>
            Production Fees: <strong>{format_currency(production_data.get('production_fees', Decimal('0.00')))}</strong>
        </div>
        """, unsafe_allow_html=True)
    
    # Production fees form
    with st.form("production_fees_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### Opening & Deposits")
            opening_balance = st.number_input(
                "Opening Balance (₹)",
                min_value=0.0,
                value=float(previous_closing),
                step=100.0,
                format="%.2f",
                help="Opening balance carried forward from previous day"
            )
            
            deposit_amount = st.number_input(
                "Deposit Amount (₹)",
                min_value=0.0,
                value=float(existing_fees.deposit_amount) if existing_fees else 0.0,
                step=100.0,
                format="%.2f",
                help="Amount deposited today"
            )
            
            total_credited = opening_balance + deposit_amount
            st.metric("Total Amount Credited", format_currency(Decimal(str(total_credited))))
        
        with col2:
            st.markdown("#### E-Challan Details")
            echallan_no = st.text_input(
                "E-Challan Number",
                value=existing_fees.echallan_no if existing_fees and existing_fees.echallan_no else "",
                help="E-Challan number for the deposit"
            )
            
            echallan_date = st.date_input(
                "E-Challan Date",
                value=existing_fees.echallan_date if existing_fees and existing_fees.echallan_date else selected_date,
                max_value=selected_date,
                help="Date of E-Challan"
            )
        
        with col3:
            st.markdown("#### Production Data")
            iml_bottles = st.number_input(
                "IML Bottles Produced",
                min_value=0,
                value=existing_fees.iml_bottles_qty if existing_fees else 0,
                step=1,
                help="Number of IML bottles produced"
            )
            
            total_bottles = st.number_input(
                "Total Bottles Produced",
                min_value=0,
                value=production_data.get('total_bottles_produced', 0) if auto_fill_production else (existing_fees.total_bottles_produced if existing_fees else 0),
                step=1,
                help="Total bottles produced (auto-filled from Reg-A)"
            )
            
            fee_per_bottle = FEE_PER_BOTTLE
            total_fees_debited = calculate_production_fees(total_bottles, fee_per_bottle)
            
            st.metric("Fee per Bottle", format_currency(fee_per_bottle))
            st.metric("Total Fees Debited", format_currency(total_fees_debited))
        
        # Closing balance calculation
        closing_balance = Decimal(str(total_credited)) - total_fees_debited
        
        st.markdown("---")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("💵 Total Credited", format_currency(Decimal(str(total_credited))), help="Opening + Deposit")
        with col_b:
            st.metric("💸 Total Debited", format_currency(total_fees_debited), help="Fees for bottles produced")
        with col_c:
            st.metric("💰 Closing Balance", format_currency(closing_balance), help="Credited - Debited")
        
        st.markdown("---")
        
        # Administrative fields
        col_x, col_y = st.columns(2)
        with col_x:
            remarks = st.text_area(
                "Remarks",
                value=existing_fees.remarks if existing_fees and existing_fees.remarks else "",
                height=100,
                help="Any additional remarks or notes"
            )
        
        with col_y:
            excise_officer = st.text_input(
                "Excise Officer Name",
                value=existing_fees.excise_officer_name if existing_fees and existing_fees.excise_officer_name else "",
                help="Name of the excise officer"
            )
        
        # Submit button
        submit_fees = st.form_submit_button("💾 Save Production Fees", use_container_width=True)
        
        if submit_fees:
            # Create fees object
            fees_account = ProductionFeesAccount(
                date=selected_date,
                opening_balance=Decimal(str(opening_balance)),
                deposit_amount=Decimal(str(deposit_amount)),
                echallan_no=echallan_no if echallan_no else None,
                echallan_date=echallan_date,
                total_credited=Decimal(str(total_credited)),
                iml_bottles_qty=iml_bottles,
                total_bottles_produced=total_bottles,
                fee_per_bottle=fee_per_bottle,
                total_fees_debited=total_fees_debited,
                closing_balance=closing_balance,
                remarks=remarks if remarks else None,
                excise_officer_name=excise_officer if excise_officer else None,
                status="submitted"
            )
            
            # Validate
            if validate_fees_balance(fees_account.total_credited, fees_account.total_fees_debited, fees_account.closing_balance):
                if save_production_fees(fees_account):
                    st.success("✅ Production fees saved successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to save production fees")
            else:
                st.error("❌ Balance validation failed! Please check your entries.")
    
    # ========================================================================
    # SECTION 2: BOTTLE STOCK INVENTORY
    # ========================================================================
    
    st.markdown('<div class="section-header section-header-green">🍾 SECTION 2: BOTTLE STOCK INVENTORY</div>', unsafe_allow_html=True)
    
    # Get existing stock data
    existing_stocks = get_bottle_stock_for_date(selected_date)
    
    # Product variant selector
    st.markdown("#### Add/Edit Product Variant")
    
    col_p1, col_p2, col_p3 = st.columns(3)
    
    with col_p1:
        product_name = st.text_input(
            "Product Name",
            value="Country Liquor",
            help="Name of the product"
        )
    
    with col_p2:
        # Create mapping for strength display
        strength_labels = {
            Decimal("28.5"): "50° U.P. (28.5% v/v)",
            Decimal("22.8"): "60° U.P. (22.8% v/v)",
            Decimal("17.1"): "70° U.P. (17.1% v/v)",
            Decimal("11.4"): "80° U.P. (11.4% v/v)"
        }
        
        strength = st.selectbox(
            "Strength",
            options=STRENGTH_OPTIONS,
            format_func=lambda x: strength_labels.get(x, f"{x}% v/v"),
            help="Alcohol strength in U.P. degrees"
        )
    
    with col_p3:
        bottle_size = st.selectbox(
            "Bottle Size (ml)",
            options=BOTTLE_SIZES_ML,
            format_func=lambda x: f"{x}ml",
            help="Bottle size in milliliters"
        )
    
    # Get previous day's stock for this variant
    prev_stock = get_previous_day_stock(selected_date, product_name, Decimal(str(strength)), bottle_size)
    
    # Check if this variant exists in today's data
    existing_variant = None
    for stock in existing_stocks:
        if (stock.product_name == product_name and 
            stock.strength == Decimal(str(strength)) and 
            stock.bottle_size_ml == bottle_size):
            existing_variant = stock
            break
    
    # Get production data for this variant
    variant_production = 0
    variant_production_bl = Decimal("0.000")
    variant_production_al = Decimal("0.000")
    
    if auto_fill_production and production_data:
        for item in production_data.get('production_items', []):
            if (item['product_name'] == product_name and 
                item['strength'] == Decimal(str(strength)) and 
                item['bottle_size_ml'] == bottle_size):
                variant_production = item['bottles']
                variant_production_bl = item['bl']
                variant_production_al = item['al']
                break
    
    # Stock entry form
    with st.form("bottle_stock_form"):
        st.markdown(f"##### Stock Entry: {product_name} - {strength}% v/v - {bottle_size}ml")
        
        if variant_production > 0:
            st.markdown(f"""
            <div class="success-box">
                <strong>✅ Production Data Available:</strong> {variant_production:,} bottles ({format_litres(variant_production_bl, 'BL')}, {format_litres(variant_production_al, 'AL')})
            </div>
            """, unsafe_allow_html=True)
        
        col_s1, col_s2, col_s3, col_s4 = st.columns(4)
        
        with col_s1:
            st.markdown("**Opening Balance**")
            opening_bottles = st.number_input(
                "Bottles",
                min_value=0,
                value=prev_stock.closing_balance_bottles if (auto_fill_opening and prev_stock) else (existing_variant.opening_balance_bottles if existing_variant else 0),
                step=1,
                key="opening_bottles"
            )
        
        with col_s2:
            st.markdown("**Received from Production**")
            received_bottles = st.number_input(
                "Bottles",
                min_value=0,
                value=variant_production if auto_fill_production else (existing_variant.quantity_received_bottles if existing_variant else 0),
                step=1,
                key="received_bottles"
            )
        
        with col_s3:
            st.markdown("**Wastage/Breakage**")
            wastage_bottles = st.number_input(
                "Bottles",
                min_value=0,
                value=existing_variant.wastage_breakage_bottles if existing_variant else 0,
                step=1,
                key="wastage_bottles"
            )
        
        with col_s4:
            st.markdown("**Issued on Duty**")
            issued_bottles = st.number_input(
                "Bottles",
                min_value=0,
                value=existing_variant.issue_on_duty_bottles if existing_variant else 0,
                step=1,
                key="issued_bottles"
            )
        
        # Calculate complete stock movement
        stock_movement = calculate_complete_stock_movement(
            opening_bottles,
            received_bottles,
            wastage_bottles,
            issued_bottles,
            bottle_size,
            Decimal(str(strength))
        )
        
        # Display calculations
        st.markdown("---")
        st.markdown("##### 📊 Calculated Stock Movement")
        
        col_calc1, col_calc2, col_calc3 = st.columns(3)
        
        with col_calc1:
            st.markdown("**Bottles**")
            st.metric("Total Accounted", format_bottles(stock_movement['total_accounted_bottles']))
            st.metric("Closing Balance", format_bottles(stock_movement['closing_bottles']))
        
        with col_calc2:
            st.markdown("**Bulk Litres (BL)**")
            st.metric("Total BL", format_litres(stock_movement['total_bl'], 'BL'))
            st.metric("Closing BL", format_litres(stock_movement['closing_bl'], 'BL'))
        
        with col_calc3:
            st.markdown("**Absolute Litres (AL)**")
            st.metric("Total AL", format_litres(stock_movement['total_al'], 'AL'))
            st.metric("Closing AL", format_litres(stock_movement['closing_al'], 'AL'))
        
        # Wastage percentage
        if stock_movement['total_accounted_bottles'] > 0:
            wastage_pct = calculate_wastage_percentage(wastage_bottles, stock_movement['total_accounted_bottles'])
            if wastage_pct > 0:
                st.markdown(f"""
                <div class="warning-box">
                    <strong>⚠️ Wastage:</strong> {wastage_pct:.2f}% of total stock
                </div>
                """, unsafe_allow_html=True)
        
        # Submit button
        submit_stock = st.form_submit_button("💾 Save Bottle Stock", use_container_width=True)
        
        if submit_stock:
            # Create stock object
            stock_inventory = BottleStockInventory(
                date=selected_date,
                product_name=product_name,
                strength=Decimal(str(strength)),
                bottle_size_ml=bottle_size,
                opening_balance_bottles=stock_movement['opening_bottles'],
                quantity_received_bottles=stock_movement['received_bottles'],
                total_accounted_bottles=stock_movement['total_accounted_bottles'],
                wastage_breakage_bottles=stock_movement['wastage_bottles'],
                issue_on_duty_bottles=stock_movement['issued_bottles'],
                closing_balance_bottles=stock_movement['closing_bottles'],
                opening_balance_bl=stock_movement['opening_bl'],
                received_bl=stock_movement['received_bl'],
                total_bl=stock_movement['total_bl'],
                wastage_bl=stock_movement['wastage_bl'],
                issue_bl=stock_movement['issued_bl'],
                closing_bl=stock_movement['closing_bl'],
                opening_balance_al=stock_movement['opening_al'],
                received_al=stock_movement['received_al'],
                total_al=stock_movement['total_al'],
                wastage_al=stock_movement['wastage_al'],
                issue_al=stock_movement['issued_al'],
                closing_al=stock_movement['closing_al'],
                status="submitted"
            )
            
            # Validate
            if validate_stock_balance(
                stock_inventory.total_accounted_bottles,
                stock_inventory.wastage_breakage_bottles,
                stock_inventory.issue_on_duty_bottles,
                stock_inventory.closing_balance_bottles
            ):
                if save_bottle_stock(stock_inventory):
                    st.success(f"✅ Stock saved for {product_name} - {strength}% - {bottle_size}ml")
                    st.rerun()
                else:
                    st.error("❌ Failed to save stock")
            else:
                st.error("❌ Stock balance validation failed!")
    
    # Display existing stocks
    if existing_stocks:
        st.markdown("---")
        st.markdown("#### 📦 Current Stock Entries")
        
        stock_df_data = []
        for stock in existing_stocks:
            stock_df_data.append({
                'Product': stock.product_name,
                'Strength': f"{stock.strength}%",
                'Size': f"{stock.bottle_size_ml}ml",
                'Opening': stock.opening_balance_bottles,
                'Received': stock.quantity_received_bottles,
                'Wastage': stock.wastage_breakage_bottles,
                'Issued': stock.issue_on_duty_bottles,
                'Closing': stock.closing_balance_bottles,
                'Closing BL': f"{stock.closing_bl:.3f}",
                'Closing AL': f"{stock.closing_al:.3f}"
            })
        
        stock_df = pd.DataFrame(stock_df_data)
        st.dataframe(stock_df, use_container_width=True, hide_index=True)

elif view_mode == "Summary View":
    
    # ========================================================================
    # SUMMARY VIEW
    # ========================================================================
    
    st.markdown('<div class="section-header section-header-orange">📊 DAILY SUMMARY VIEW</div>', unsafe_allow_html=True)
    
    # Generate and display summary
    summary = generate_daily_summary(selected_date)
    
    if summary:
        # Production Fees Summary
        st.markdown("### 💰 Production Fees Summary")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Opening", format_currency(summary.production_fees_opening))
        with col2:
            st.metric("Deposit", format_currency(summary.production_fees_deposit))
        with col3:
            st.metric("Credited", format_currency(summary.production_fees_credited))
        with col4:
            st.metric("Debited", format_currency(summary.production_fees_debited))
        with col5:
            st.metric("Closing", format_currency(summary.production_fees_closing))
        
        st.markdown("---")
        
        # Bottle Stock Summary
        st.markdown("### 🍾 Bottle Stock Summary")
        
        tab1, tab2, tab3 = st.tabs(["📦 Bottles", "🔵 Bulk Litres (BL)", "🔴 Absolute Litres (AL)"])
        
        with tab1:
            col_b1, col_b2, col_b3, col_b4, col_b5, col_b6 = st.columns(6)
            with col_b1:
                st.metric("Opening", f"{summary.total_opening_bottles:,}")
            with col_b2:
                st.metric("Received", f"{summary.total_received_bottles:,}")
            with col_b3:
                st.metric("Total", f"{summary.total_accounted_bottles:,}")
            with col_b4:
                st.metric("Wastage", f"{summary.total_wastage_bottles:,}")
            with col_b5:
                st.metric("Issued", f"{summary.total_issued_bottles:,}")
            with col_b6:
                st.metric("Closing", f"{summary.total_closing_bottles:,}")
        
        with tab2:
            col_bl1, col_bl2, col_bl3, col_bl4, col_bl5, col_bl6 = st.columns(6)
            with col_bl1:
                st.metric("Opening", f"{summary.total_opening_bl:.3f}")
            with col_bl2:
                st.metric("Received", f"{summary.total_received_bl:.3f}")
            with col_bl3:
                st.metric("Total", f"{summary.total_accounted_bl:.3f}")
            with col_bl4:
                st.metric("Wastage", f"{summary.total_wastage_bl:.3f}")
            with col_bl5:
                st.metric("Issued", f"{summary.total_issued_bl:.3f}")
            with col_bl6:
                st.metric("Closing", f"{summary.total_closing_bl:.3f}")
        
        with tab3:
            col_al1, col_al2, col_al3, col_al4, col_al5, col_al6 = st.columns(6)
            with col_al1:
                st.metric("Opening", f"{summary.total_opening_al:.3f}")
            with col_al2:
                st.metric("Received", f"{summary.total_received_al:.3f}")
            with col_al3:
                st.metric("Total", f"{summary.total_accounted_al:.3f}")
            with col_al4:
                st.metric("Wastage", f"{summary.total_wastage_al:.3f}")
            with col_al5:
                st.metric("Issued", f"{summary.total_issued_al:.3f}")
            with col_al6:
                st.metric("Closing", f"{summary.total_closing_al:.3f}")
        
        # Save summary button
        if st.button("💾 Save Summary to Database", use_container_width=True):
            if save_daily_summary(summary):
                st.success("✅ Summary saved successfully!")
            else:
                st.error("❌ Failed to save summary")
    else:
        st.info("ℹ️ No data available for the selected date. Please enter data first.")

else:
    
    # ========================================================================
    # ADMINISTRATIVE VIEW
    # ========================================================================
    
    st.markdown('<div class="section-header">👨‍💼 ADMINISTRATIVE VIEW</div>', unsafe_allow_html=True)
    
    st.info("🚧 Administrative view with multi-date reports and analytics coming soon!")
    
    # Placeholder for future administrative features
    st.markdown("""
    **Planned Features:**
    - 📅 Multi-date range selection
    - 📈 Trend analysis and charts
    - 📊 Comparative reports
    - 📄 PDF export functionality
    - 🔍 Advanced search and filtering
    - 📧 Email reports
    """)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p><strong>Reg-B - Issue of Country Liquor in Bottles</strong></p>
    <p>Excise Parallel Register System | SIP 2 LIFE DISTILLERIES</p>
</div>
""", unsafe_allow_html=True)
