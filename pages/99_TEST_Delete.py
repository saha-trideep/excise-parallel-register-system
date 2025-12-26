import streamlit as st
import pandas as pd
from datetime import datetime
import time
import reg76_backend

# NO AUTHENTICATION - Direct access for testing
st.set_page_config(
    page_title="TEST: Reg-76 Delete Functionality",
    page_icon="🧪",
    layout="wide",
)

st.title("🧪 TEST PAGE: Reg-76 Delete Functionality")
st.success("✅ **This is a TEST PAGE** - No authentication required!")
st.info("📅 **Created**: December 26, 2025, 15:05 IST")

st.divider()

# Load records
records = reg76_backend.get_data()

st.subheader("📊 Current Records")

if records.empty:
    st.warning("⚠️ No records found in reg76_data.csv")
    st.info("💡 Run `python add_test_record_reg76.py` to add a test record")
else:
    st.success(f"✅ Found {len(records)} record(s)")
    
    # Show data table
    st.dataframe(
        records[["reg76_id", "created_at", "vehicle_no", "permit_no", "storage_vat_no"]],
        use_container_width=True,
        hide_index=True
    )
    
    st.divider()
    
    # DELETE SECTION
    st.subheader("🗑️ Delete Functionality Test")
    
    with st.expander("🗑️ Delete Individual Record", expanded=True):
        st.warning("⚠️ **WARNING**: This will delete from both CSV and Google Sheets!")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            record_to_delete = st.selectbox(
                "Select Record to Delete",
                options=[""] + records['reg76_id'].tolist(),
                help="Choose a record ID to delete"
            )
        
        with col2:
            st.write("")  # Spacer
            st.write("")  # Spacer
            if st.button("🗑️ Delete Selected", type="primary", disabled=(record_to_delete == "")):
                if record_to_delete:
                    success, message = reg76_backend.delete_record(record_to_delete)
                    if success:
                        st.success(message)
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(message)
    
    with st.expander("⚠️ DANGER ZONE: Clear All Data", expanded=False):
        st.error("🚨 **EXTREME CAUTION**: This will DELETE ALL records!")
        
        clear_confirm = st.text_input("Type DELETE ALL to confirm", key="clear_confirm")
        
        if st.button("🗑️ CLEAR ALL DATA", type="secondary", disabled=(clear_confirm != "DELETE ALL")):
            if clear_confirm == "DELETE ALL":
                success, message = reg76_backend.clear_all_data()
                if success:
                    st.success(message)
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error(message)

st.divider()

st.info("""
### 📝 Instructions:
1. If you see records above, the delete buttons should work
2. Select a record and click "Delete Selected"
3. If this works, it means the delete code is functional
4. The issue is likely with browser cache or Streamlit not reloading the main Reg-76 page

### 🔧 If delete works here but not in main Reg-76:
- Clear browser cache completely
- Try opening in Incognito/Private mode
- Check if you're accessing a deployed version instead of local
""")
