import streamlit as st
import pandas as pd

st.set_page_config(page_title="RAID Log Analyzer", layout="wide")
st.title("🧯 RAID Log Analyzer")

# Check if file is already uploaded in session state
if 'uploaded_file' not in st.session_state:
    st.warning("⚠️ Please upload the Clarity export Excel file using the left sidebar.")
    st.stop()

# Read the uploaded Excel file
xls = pd.ExcelFile(st.session_state.uploaded_file)

# Ensure RAID Log sheet exists
if "RAID Log" not in xls.sheet_names:
    st.error("❌ 'RAID Log' sheet not found in the uploaded file.")
    st.stop()

# Load RAID Log sheet
df = pd.read_excel(xls, sheet_name="RAID Log")
df.columns = df.columns.str.strip()

# Display the raw RAID log
st.subheader("📋 Raw RAID Log")
st.dataframe(df, use_container_width=True)

# Show summary by Type and Status
with st.expander("🔍 RAID Summary"):
    st.markdown("### Counts by Type and Status")
    summary = df.groupby(['Type', 'Status']).size().unstack(fill_value=0)
    st.dataframe(summary)

# Static GenAI Prompt for Manual Copy-Paste
with st.expander("🤖 Gen AI Summary (Static Prompt)"):
    prompt = f"""
You are a PMO Assistant. Summarize the RAID log into key highlights for senior leadership.
Focus on urgent risks, overdue actions, blocked issues, and dependencies.
Return output in bullet points. Use the data below:

{df.head(10).to_markdown()}
"""
    st.code(prompt, language="markdown")
    st.info("Paste this prompt in ChatGPT or connect OpenAI API for automation.")
