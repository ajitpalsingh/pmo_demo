import streamlit as st
import pandas as pd

st.set_page_config(page_title="RAID Log Analyzer", layout="wide")
st.title("🛡️ RAID Log Analyzer")

uploaded_file = st.file_uploader("Upload your RAID Log Excel file", type=[".xlsx"])

if uploaded_file:
    # Load all sheet names
    xl = pd.ExcelFile(uploaded_file)
    raid_sheets = [sheet for sheet in xl.sheet_names if 'RAID' in sheet.upper() or sheet.lower() == 'raid log']

    if not raid_sheets:
        st.warning("No RAID log sheet found. Please include a sheet named 'RAID Log' or with 'RAID' in the name.")
    else:
        sheet_to_use = raid_sheets[0]
        df = xl.parse(sheet_to_use)

        st.subheader(f"📋 Loaded Sheet: {sheet_to_use}")
        st.dataframe(df, use_container_width=True)

        # Optional: Detect column types
        if {'Type', 'Status', 'Description', 'Owner', 'Due Date'}.issubset(df.columns):
            with st.expander("🧠 Summary Insights", expanded=True):
                risk_count = df[df['Type'].str.contains("risk", case=False)].shape[0]
                issue_count = df[df['Type'].str.contains("issue", case=False)].shape[0]
                open_issues = df[(df['Status'].str.lower() == 'open') & (df['Type'].str.contains("issue", case=False))]

                st.markdown(f"**Total Risks:** {risk_count}")
                st.markdown(f"**Total Issues:** {issue_count}")
                st.markdown(f"**Open Issues:** {open_issues.shape[0]}")

                # Highlight overdue
                if 'Due Date' in df.columns:
                    df['Due Date'] = pd.to_datetime(df['Due Date'], errors='coerce')
                    overdue = df[(df['Status'].str.lower() == 'open') & (df['Due Date'] < pd.Timestamp.today())]
                    st.markdown(f"**Overdue Items:** {overdue.shape[0]}")
                    if overdue.shape[0] > 0:
                        st.dataframe(overdue[['Type', 'Description', 'Owner', 'Due Date']], use_container_width=True)
        else:
            st.warning("Missing one or more required columns: Type, Status, Description, Owner, Due Date")
else:
    st.info("Upload a RAID Log Excel file to begin analysis.")
