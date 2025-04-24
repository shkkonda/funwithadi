import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime

st.set_page_config(page_title="Segments Activator", layout="wide")

st.title("🚀 Segments Activator")

# -------------------------
# 1. Bulk Upload Section
# -------------------------
st.header("📁 Bulk Upload (Excel)")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
template_df = pd.DataFrame({
    "SegKey": [""],
    "Platform ID": [""],
    "Country Code": [""],
    "Action (Add/Remove)": [""]
})

# Downloadable Excel template
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

st.download_button("📥 Download Template", to_excel(template_df), file_name="bulk_template.xlsx")

if uploaded_file:
    try:
        df_uploaded = pd.read_excel(uploaded_file)
        st.success("File uploaded successfully!")
        st.dataframe(df_uploaded)
    except Exception as e:
        st.error(f"Failed to read file: {e}")

# -------------------------
# 2. Tabs for Bulk Actions
# -------------------------
tab1, tab2 = st.tabs(["📦 Segment-Level Actions", "📘 Description-Level Actions"])

with tab1:
    st.subheader("Segment-Level Bulk Actions")
    st.text("Upload an Excel or enter data manually below:")
    st.button("▶️ Process Segment Actions")

with tab2:
    st.subheader("Description-Level Bulk Actions")
    st.text("Supports actions based on Level1 descriptions")
    st.button("▶️ Process Description-Level Actions")

# -------------------------
# 3. Missing Segments Lookup
# -------------------------
st.header("🔍 Missing Segments Insights")

col1, col2 = st.columns(2)
with col1:
    platform_filter = st.selectbox("Platform ID", list(range(0, 47)))
with col2:
    date_range = st.date_input("Created Date Range", (datetime(2024, 1, 1), datetime(2025, 4, 24)))

if st.button("🔍 View Unused Segments"):
    st.info("Query would run to check unused segments based on filters.")
    # You can show a mock result
    st.table(pd.DataFrame({
        "SegKey": ["123", "456"],
        "Description": ["Segment A", "Segment B"],
        "Reason Not Added": ["Custom", "Not valid for platform"]
    }))

# -------------------------
# 4. Platform Reference Table
# -------------------------
with st.expander("ℹ️ Platform Name ↔ ID Mapping"):
    platform_dict = {
        0: "SODA", 1: "TTD - The Trade Desk", 2: "ODC - Oracle Data Cloud", 3: "AdSquare",
        10: "StartApp", 15: "Adobe", 16: "Lotame", 17: "Nielsen", 18: "Retargetly", 21: "Eyeota",
        22: "Acxiom", 23: "Neustar", 25: "TTD Extension Product", 26: "Tru Optik", 27: "Amobee",
        28: "Magenta", 31: "Pubmatic", 32: "NativeTouch", 35: "BidMind", 36: "Mediagrid",
        37: "Turk Telekom", 38: "Appsflyer", 42: "OpenX", 43: "Equativ", 44: "Yahoo", 45: "Xandr",
        46: "TTD V2"
    }
    platform_table = pd.DataFrame(list(platform_dict.items()), columns=["Platform ID", "Platform Name"])
    st.dataframe(platform_table)

# -------------------------
# Optional: Logging output for failed actions
# -------------------------
st.header("📋 Failed Segment Log")
st.caption("Here you’ll see segments that couldn’t be activated with reasons.")

# Example error table
st.dataframe(pd.DataFrame({
    "SegKey": ["789", "012"],
    "Platform": ["StartApp", "TTD"],
    "Reason": ["Country not mapped", "Invalid segment type"]
}))

