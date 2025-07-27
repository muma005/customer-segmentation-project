#!/usr/bin/env python3
"""
Script to download the Online Retail dataset from UCI Machine Learning Repository
"""

import requests
import os
import pandas as pd
from pathlib import Path

def download_online_retail_dataset():
    """Download the Online Retail dataset from UCI repository"""
    
    # Dataset URL
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx"
    
    # Local file path
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    file_path = data_dir / "online_retail.csv"
    
    print("📥 Downloading Online Retail dataset from UCI repository...")
    print(f"URL: {url}")
    print(f"Local path: {file_path}")
    
    try:
        # Download the Excel file
        print("⏳ Downloading file...")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Save as Excel first
        excel_path = data_dir / "online_retail.xlsx"
        with open(excel_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print("✅ Excel file downloaded successfully!")
        
        # Convert to CSV
        print("🔄 Converting Excel to CSV...")
        df = pd.read_excel(excel_path)
        df.to_csv(file_path, index=False)
        
        # Remove Excel file
        os.remove(excel_path)
        
        print(f"✅ Dataset converted and saved to: {file_path}")
        print(f"📊 Dataset shape: {df.shape}")
        print(f"📋 Columns: {list(df.columns)}")
        
        # Display sample data
        print("\n📋 Sample data:")
        print(df.head())
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error downloading file: {e}")
        return False
    except Exception as e:
        print(f"❌ Error processing file: {e}")
        return False

def create_sample_data():
    """Create a sample dataset for testing if download fails"""
    
    print("🔄 Creating sample dataset for testing...")
    
    import numpy as np
    from datetime import datetime, timedelta
    
    # Generate sample data
    np.random.seed(42)
    n_customers = 1000
    n_transactions = 5000
    
    # Generate customer IDs
    customer_ids = [f"CUST_{i:05d}" for i in range(1, n_customers + 1)]
    
    # Generate transaction data
    data = []
    start_date = datetime(2010, 1, 1)
    end_date = datetime(2011, 12, 31)
    
    for i in range(n_transactions):
        customer_id = np.random.choice(customer_ids)
        invoice_date = start_date + timedelta(days=np.random.randint(0, (end_date - start_date).days))
        quantity = np.random.poisson(5)
        unit_price = np.random.uniform(1, 100)
        
        data.append({
            'InvoiceNo': f"INV_{i:06d}",
            'StockCode': f"SKU_{np.random.randint(1000, 9999)}",
            'Description': f"Product {np.random.randint(1, 100)}",
            'Quantity': quantity,
            'InvoiceDate': invoice_date,
            'UnitPrice': unit_price,
            'CustomerID': customer_id,
            'Country': np.random.choice(['United Kingdom', 'Germany', 'France', 'Spain', 'Italy'])
        })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to CSV
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    file_path = data_dir / "online_retail.csv"
    df.to_csv(file_path, index=False)
    
    print(f"✅ Sample dataset created: {file_path}")
    print(f"📊 Dataset shape: {df.shape}")
    print(f"📋 Columns: {list(df.columns)}")
    
    return True

if __name__ == "__main__":
    print("🚀 Janah Customer Segmentation - Dataset Downloader")
    print("=" * 60)
    
    # Try to download the real dataset
    success = download_online_retail_dataset()
    
    if not success:
        print("\n⚠️ Failed to download real dataset. Creating sample data instead...")
        create_sample_data()
    
    print("\n🎉 Dataset setup completed!")
    print("\n📋 Next steps:")
    print("1. Activate your virtual environment")
    print("2. Install requirements: pip install -r streamlit/requirements.txt")
    print("3. Run Streamlit: streamlit run streamlit/segmentation.py")
    print("4. Or run Flask app: python run.py") 