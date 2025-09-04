import streamlit as st
import pandas as pd

st.title("📊 Café Sales Forecasting Tool")

# File uploader
uploaded_file = st.file_uploader("Upload your café sales data (.csv)", type=["csv", "xlsx"])

if uploaded_file:
    # Read data
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("File uploaded successfully!")
    st.subheader("Sample of your data:")
    st.write(df.head())
else:
    st.info("Submission error.")
