import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import plotly.express as px

def main():
    st.set_page_config(
        page_title="Janah Customer Segmentation",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 Janah Customer Segmentation Dashboard")
    st.markdown("---")
    
    # Sidebar
    st.sidebar.header("Configuration")
    
    # File upload
    uploaded_file = st.sidebar.file_uploader(
        "Upload CSV file",
        type=['csv'],
        help="Upload your customer data in CSV format"
    )
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.sidebar.success(f"Data loaded: {df.shape[0]} rows, {df.shape[1]} columns")
        st.subheader("Data Preview")
        st.dataframe(df.head())
    else:
        st.info("Please upload a CSV file to begin segmentation analysis")

if __name__ == "__main__":
    main()
