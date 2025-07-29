import streamlit as st
import pandas as pd
import openai

# --- Title ---
st.set_page_config(page_title="Project Health AI Dashboard", layout="wide")
st.title("📊 Project Health Dashboard (Gen AI Enabled)")

# --- File Upload ---
st.sidebar.header("Upload Clarity Export File")
uploaded_file = st.sidebar.file_uploader("Upload Excel file", type=["xlsx"])

if uploaded_file:
    # Load Excel file
    xl = pd.ExcelFile(uploaded_file)

    if "Project Portfolio" not in xl.sheet_names:
        st.error("'Project Portfolio' sheet not found in Excel file.")
    else:
        df = xl.parse("Project Portfolio")

        # Preprocess and compute cost variance
        df["Cost Variance ($M)"] = df["Planned Cost ($M)"] - df["Forecast Cost ($M)"]
        df["Cost Variance (%)"] = round((df["Cost Variance ($M)"] / df["Planned Cost ($M)"]) * 100, 2)

        # Show metrics
        st.subheader("Portfolio Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Projects", len(df))
        col2.metric("Total Planned Budget ($M)", f"{df['Planned Cost ($M)'].sum():.2f}")
        col3.metric("Total Forecast Cost ($M)", f"{df['Forecast Cost ($M)'].sum():.2f}")

        # Show detailed table
        st.subheader("📋 Project Overview")
        st.dataframe(df.style.applymap(
            lambda val: "background-color: #ffcccc" if val == "Red" else ("background-color: #fff3cd" if val == "Amber" else "background-color: #d4edda"),
            subset=["Status (RAG)"]
        ))

        # Optional AI insight
        st.subheader("🤖 Gen AI Summary (Static Prompt)")
        if st.button("Generate Insight with Gen AI"):
            prompt = """
You are a Program Manager Assistant. Analyze the following project health data and generate a summary:
- Highlight projects that are over budget
- Comment on ROI and RAG status
- Suggest any action or watchlist flags

"""
            preview = df[["Project Name", "Status (RAG)", "Planned Cost ($M)", "Forecast Cost ($M)", "Cost Variance (%)", "ROI (%)"]].to_string(index=False)
            st.code(prompt + preview)
            st.info("Paste this prompt into ChatGPT or Copilot to get a summary.")

else:
    st.info("👈 Upload your Clarity-style Excel file to begin.")
