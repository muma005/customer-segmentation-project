#!/usr/bin/env python3
"""
Janah Customer Segmentation - Streamlit Module
Core segmentation logic with RFM analysis and K-means clustering
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import warnings
import os
from datetime import datetime
import json

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(
    page_title="Janah Customer Segmentation",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1E90FF 0%, #0066CC 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1E90FF;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def load_and_clean_data(file_path):
    """
    Load and clean the dataset
    
    Args:
        file_path (str): Path to the CSV file
        
    Returns:
        pd.DataFrame: Cleaned dataset
    """
    try:
        # Load the dataset
        st.info(f"📂 Loading dataset from: {file_path}")
        data = pd.read_csv(file_path, encoding='latin-1')
        
        # Display initial data info
        st.write(f"**Initial dataset shape:** {data.shape}")
        st.write(f"**Columns:** {list(data.columns)}")
        
        # Check for missing values
        missing_values = data.isnull().sum()
        if missing_values.sum() > 0:
            st.warning(f"⚠️ Found missing values:\n{missing_values[missing_values > 0]}")
        
        # Remove rows where CustomerID is missing
        initial_rows = len(data)
        data = data.dropna(subset=['CustomerID'])
        rows_after_customerid = len(data)
        
        if initial_rows != rows_after_customerid:
            st.info(f"🗑️ Removed {initial_rows - rows_after_customerid} rows with missing CustomerID")
        
        # Drop duplicate rows
        initial_rows = len(data)
        data = data.drop_duplicates()
        rows_after_dedup = len(data)
        
        if initial_rows != rows_after_dedup:
            st.info(f"🗑️ Removed {initial_rows - rows_after_dedup} duplicate rows")
        
        # Convert CustomerID to string and remove leading/trailing spaces
        data['CustomerID'] = data['CustomerID'].astype(str).str.strip()
        
        # Convert InvoiceDate to datetime
        data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])
        
        # Filter outliers using IQR method for Quantity and UnitPrice
        def remove_outliers_iqr(df, column):
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
        
        # Remove outliers from Quantity
        initial_rows = len(data)
        data = remove_outliers_iqr(data, 'Quantity')
        rows_after_quantity = len(data)
        
        if initial_rows != rows_after_quantity:
            st.info(f"🗑️ Removed {initial_rows - rows_after_quantity} rows with outlier Quantity values")
        
        # Remove outliers from UnitPrice
        initial_rows = len(data)
        data = remove_outliers_iqr(data, 'UnitPrice')
        rows_after_price = len(data)
        
        if initial_rows != rows_after_price:
            st.info(f"🗑️ Removed {initial_rows - rows_after_price} rows with outlier UnitPrice values")
        
        # Remove negative quantities and prices
        data = data[(data['Quantity'] > 0) & (data['UnitPrice'] > 0)]
        
        st.success(f"✅ Data cleaning completed! Final dataset shape: {data.shape}")
        
        return data
        
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return None

def calculate_rfm(data):
    """
    Calculate RFM (Recency, Frequency, Monetary) metrics
    
    Args:
        data (pd.DataFrame): Cleaned transaction data
        
    Returns:
        pd.DataFrame: RFM metrics for each customer
    """
    try:
        st.info("🔄 Calculating RFM metrics...")
        
        # Find the latest date in the dataset
        latest_date = data['InvoiceDate'].max()
        st.write(f"**Latest transaction date:** {latest_date.strftime('%Y-%m-%d')}")
        
        # Calculate RFM metrics
        rfm = data.groupby('CustomerID').agg({
            'InvoiceDate': lambda x: (latest_date - x.max()).days,  # Recency
            'InvoiceNo': 'nunique',  # Frequency
            'Quantity': lambda x: (x * data.loc[x.index, 'UnitPrice']).sum()  # Monetary
        }).reset_index()
        
        # Rename columns
        rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']
        
        # Display RFM summary statistics
        st.write("**RFM Metrics Summary:**")
        st.write(rfm.describe())
        
        # Check for any negative monetary values and fix
        if (rfm['Monetary'] < 0).any():
            st.warning("⚠️ Found negative monetary values. Converting to absolute values.")
            rfm['Monetary'] = rfm['Monetary'].abs()
        
        st.success(f"✅ RFM calculation completed! {len(rfm)} customers analyzed")
        
        return rfm
        
    except Exception as e:
        st.error(f"❌ Error calculating RFM: {str(e)}")
        return None

def perform_clustering(rfm_data, n_clusters=None):
    """
    Perform K-means clustering on RFM data
    
    Args:
        rfm_data (pd.DataFrame): RFM metrics data
        n_clusters (int): Number of clusters (if None, use elbow method)
        
    Returns:
        tuple: (clustered_data, optimal_clusters, model)
    """
    try:
        st.info("🔍 Performing clustering analysis...")
        
        # Prepare data for clustering (exclude CustomerID)
        clustering_data = rfm_data[['Recency', 'Frequency', 'Monetary']].copy()
        
        # Standardize the features
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(clustering_data)
        
        # Determine optimal number of clusters using elbow method
        if n_clusters is None:
            st.write("📊 Finding optimal number of clusters using elbow method...")
            
            # Calculate within-cluster sum of squares for different k values
            wcss = []
            silhouette_scores = []
            k_range = range(2, 11)
            
            for k in k_range:
                kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
                kmeans.fit(scaled_data)
                wcss.append(kmeans.inertia_)
                
                # Calculate silhouette score
                if k > 1:
                    silhouette_scores.append(silhouette_score(scaled_data, kmeans.labels_))
                else:
                    silhouette_scores.append(0)
            
            # Create elbow plot
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
            
            # Elbow plot
            ax1.plot(k_range, wcss, 'bo-')
            ax1.set_xlabel('Number of Clusters (k)')
            ax1.set_ylabel('Within-Cluster Sum of Squares (WCSS)')
            ax1.set_title('Elbow Method for Optimal k')
            ax1.grid(True, alpha=0.3)
            
            # Silhouette score plot
            ax2.plot(k_range[1:], silhouette_scores, 'ro-')
            ax2.set_xlabel('Number of Clusters (k)')
            ax2.set_ylabel('Silhouette Score')
            ax2.set_title('Silhouette Score vs Number of Clusters')
            ax2.grid(True, alpha=0.3)
            
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
            
            # Find optimal k (elbow point)
            # Simple method: find the point where the rate of decrease slows down
            wcss_diff = np.diff(wcss)
            wcss_diff_rate = np.diff(wcss_diff)
            optimal_k = np.argmax(wcss_diff_rate) + 3  # +3 because we start from k=2
            
            # Also consider silhouette score
            optimal_k_silhouette = np.argmax(silhouette_scores) + 2
            
            # Choose the better of the two methods
            if optimal_k_silhouette >= 3 and optimal_k_silhouette <= 6:
                optimal_k = optimal_k_silhouette
            
            # Ensure optimal_k is within reasonable range
            optimal_k = max(3, min(6, optimal_k))
            
            st.success(f"🎯 Optimal number of clusters: {optimal_k}")
            n_clusters = optimal_k
        
        # Perform K-means clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(scaled_data)
        
        # Add cluster labels to the data
        rfm_data['Cluster'] = cluster_labels
        
        # Calculate cluster statistics
        cluster_stats = rfm_data.groupby('Cluster')[['Recency', 'Frequency', 'Monetary']].mean()
        cluster_sizes = rfm_data['Cluster'].value_counts().sort_index()
        
        st.write("**Cluster Statistics:**")
        st.write(cluster_stats)
        
        st.write("**Cluster Sizes:**")
        for cluster, size in cluster_sizes.items():
            percentage = (size / len(rfm_data)) * 100
            st.write(f"Cluster {cluster}: {size} customers ({percentage:.1f}%)")
        
        st.success(f"✅ Clustering completed! {n_clusters} clusters created")
        
        return rfm_data, n_clusters, kmeans
        
    except Exception as e:
        st.error(f"❌ Error performing clustering: {str(e)}")
        return None, None, None

def create_visualizations(rfm_data):
    """
    Create visualizations for RFM analysis and clustering results
    
    Args:
        rfm_data (pd.DataFrame): RFM data with cluster labels
    """
    try:
        print("📈 Creating visualizations...")
        
        # Set style for plots
        plt.style.use('default')
        sns.set_palette("husl")
        
        # Create output directory for plots
        plots_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'processed', 'plots')
        os.makedirs(plots_dir, exist_ok=True)
        
        # Create subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. RFM Distribution Histograms
        axes[0, 0].hist(rfm_data['Recency'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        axes[0, 0].set_title('Recency Distribution')
        axes[0, 0].set_xlabel('Days Since Last Purchase')
        axes[0, 0].set_ylabel('Number of Customers')
        axes[0, 0].grid(True, alpha=0.3)
        
        axes[0, 1].hist(rfm_data['Monetary'], bins=30, alpha=0.7, color='lightgreen', edgecolor='black')
        axes[0, 1].set_title('Monetary Distribution')
        axes[0, 1].set_xlabel('Total Spending ($)')
        axes[0, 1].set_ylabel('Number of Customers')
        axes[0, 1].grid(True, alpha=0.3)
        
        # 2. Scatter plot: Recency vs Monetary (colored by cluster)
        scatter = axes[1, 0].scatter(rfm_data['Recency'], rfm_data['Monetary'], 
                                   c=rfm_data['Cluster'], cmap='viridis', alpha=0.6)
        axes[1, 0].set_title('Recency vs Monetary (Colored by Cluster)')
        axes[1, 0].set_xlabel('Recency (Days)')
        axes[1, 0].set_ylabel('Monetary ($)')
        axes[1, 0].grid(True, alpha=0.3)
        plt.colorbar(scatter, ax=axes[1, 0], label='Cluster')
        
        # 3. Frequency vs Monetary scatter plot
        scatter2 = axes[1, 1].scatter(rfm_data['Frequency'], rfm_data['Monetary'], 
                                    c=rfm_data['Cluster'], cmap='viridis', alpha=0.6)
        axes[1, 1].set_title('Frequency vs Monetary (Colored by Cluster)')
        axes[1, 1].set_xlabel('Frequency (Number of Transactions)')
        axes[1, 1].set_ylabel('Monetary ($)')
        axes[1, 1].grid(True, alpha=0.3)
        plt.colorbar(scatter2, ax=axes[1, 1], label='Cluster')
        
        plt.tight_layout()
        
        # Save the plot
        plot_path = os.path.join(plots_dir, 'rfm_analysis.png')
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        # Create cluster distribution pie chart
        fig2, ax = plt.subplots(figsize=(10, 6))
        cluster_counts = rfm_data['Cluster'].value_counts()
        colors = plt.cm.Set3(np.linspace(0, 1, len(cluster_counts)))
        
        wedges, texts, autotexts = ax.pie(cluster_counts.values, labels=[f'Cluster {i}' for i in cluster_counts.index], 
                                         autopct='%1.1f%%', colors=colors, startangle=90)
        ax.set_title('Customer Distribution by Cluster')
        
        # Save the pie chart
        pie_path = os.path.join(plots_dir, 'cluster_distribution.png')
        plt.savefig(pie_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✅ Visualizations created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating visualizations: {str(e)}")
        return False

def create_visualizations_streamlit(rfm_data):
    """
    Streamlit version of create_visualizations for when running in Streamlit context
    """
    try:
        st.info("📈 Creating visualizations...")
        
        # Set style for plots
        plt.style.use('default')
        sns.set_palette("husl")
        
        # Create subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. RFM Distribution Histograms
        axes[0, 0].hist(rfm_data['Recency'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        axes[0, 0].set_title('Recency Distribution')
        axes[0, 0].set_xlabel('Days Since Last Purchase')
        axes[0, 0].set_ylabel('Number of Customers')
        axes[0, 0].grid(True, alpha=0.3)
        
        axes[0, 1].hist(rfm_data['Monetary'], bins=30, alpha=0.7, color='lightgreen', edgecolor='black')
        axes[0, 1].set_title('Monetary Distribution')
        axes[0, 1].set_xlabel('Total Spending ($)')
        axes[0, 1].set_ylabel('Number of Customers')
        axes[0, 1].grid(True, alpha=0.3)
        
        # 2. Scatter plot: Recency vs Monetary (colored by cluster)
        scatter = axes[1, 0].scatter(rfm_data['Recency'], rfm_data['Monetary'], 
                                   c=rfm_data['Cluster'], cmap='viridis', alpha=0.6)
        axes[1, 0].set_title('Recency vs Monetary (Colored by Cluster)')
        axes[1, 0].set_xlabel('Recency (Days)')
        axes[1, 0].set_ylabel('Monetary ($)')
        axes[1, 0].grid(True, alpha=0.3)
        plt.colorbar(scatter, ax=axes[1, 0], label='Cluster')
        
        # 3. Frequency vs Monetary scatter plot
        scatter2 = axes[1, 1].scatter(rfm_data['Frequency'], rfm_data['Monetary'], 
                                    c=rfm_data['Cluster'], cmap='viridis', alpha=0.6)
        axes[1, 1].set_title('Frequency vs Monetary (Colored by Cluster)')
        axes[1, 1].set_xlabel('Frequency (Number of Transactions)')
        axes[1, 1].set_ylabel('Monetary ($)')
        axes[1, 1].grid(True, alpha=0.3)
        plt.colorbar(scatter2, ax=axes[1, 1], label='Cluster')
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        
        # Create cluster distribution pie chart
        fig2, ax = plt.subplots(figsize=(10, 6))
        cluster_counts = rfm_data['Cluster'].value_counts()
        colors = plt.cm.Set3(np.linspace(0, 1, len(cluster_counts)))
        
        wedges, texts, autotexts = ax.pie(cluster_counts.values, labels=[f'Cluster {i}' for i in cluster_counts.index], 
                                         autopct='%1.1f%%', colors=colors, startangle=90)
        ax.set_title('Customer Distribution by Cluster')
        
        st.pyplot(fig2)
        plt.close()
        
        st.success("✅ Visualizations created successfully!")
        
    except Exception as e:
        st.error(f"❌ Error creating visualizations: {str(e)}")

def generate_report(rfm_data, analysis_params):
    """Generate a comprehensive analysis report"""
    report = f"""
JANAH HARDWARE STORE - CUSTOMER SEGMENTATION REPORT
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

ANALYSIS SUMMARY
================
Total Customers Analyzed: {len(rfm_data):,}
Number of Segments: {rfm_data['Cluster'].nunique()}
Analysis Parameters: {analysis_params}

SEGMENT PROFILES
================
"""
    
    # Add segment details
    for segment in rfm_data['Segment'].unique():
        segment_data = rfm_data[rfm_data['Segment'] == segment]
        report += f"""
{segment.upper()}
- Customer Count: {len(segment_data):,} ({len(segment_data)/len(rfm_data)*100:.1f}%)
- Average Recency: {segment_data['Recency'].mean():.1f} days
- Average Frequency: {segment_data['Frequency'].mean():.1f} transactions
- Average Monetary: ${segment_data['Monetary'].mean():,.2f}
- Total Revenue: ${segment_data['Monetary'].sum():,.2f}

RECOMMENDATIONS:
"""
        
        if "Loyal" in segment:
            report += "- Maintain relationship with exclusive offers\n- Consider VIP program\n- Request referrals\n"
        elif "At-Risk" in segment:
            report += "- Re-engagement campaigns\n- Special discounts\n- Customer feedback surveys\n"
        elif "New" in segment:
            report += "- Welcome series\n- Product education\n- First purchase incentives\n"
        elif "High-Value" in segment:
            report += "- Premium services\n- Early access to new products\n- Personal account manager\n"
        elif "Inactive" in segment:
            report += "- Win-back campaigns\n- Significant discounts\n- Product updates\n"
        
        report += "\n"
    
    report += f"""
TECHNICAL DETAILS
=================
- RFM Analysis: Recency, Frequency, Monetary metrics
- Clustering Algorithm: K-means with StandardScaler
- Optimal Clusters: Determined by Elbow Method + Silhouette Score
- Data Quality: Outliers removed using IQR method

BUSINESS INSIGHTS
=================
- Top Revenue Segment: {rfm_data.groupby('Segment')['Monetary'].sum().idxmax()}
- Most Active Segment: {rfm_data.groupby('Segment')['Frequency'].mean().idxmax()}
- Largest Segment: {rfm_data['Segment'].value_counts().index[0]}

NEXT STEPS
==========
1. Implement targeted marketing campaigns
2. Monitor segment performance over time
3. Adjust segmentation parameters as needed
4. Integrate with CRM system for automation

---
Report generated by Janah Customer Segmentation System
For questions, contact: janah@hardwarestore.com
"""
    
    return report

def create_campaign_preview(segment_name, rfm_data):
    """Create a mock campaign preview for a segment"""
    segment_data = rfm_data[rfm_data['Segment'] == segment_name]
    
    if len(segment_data) == 0:
        return "No data available for this segment."
    
    avg_recency = segment_data['Recency'].mean()
    avg_monetary = segment_data['Monetary'].mean()
    customer_count = len(segment_data)
    
    campaign_templates = {
        "Loyal Customers": {
            "subject": "🎉 Exclusive VIP Offer for Our Loyal Customers!",
            "content": f"""
Dear Valued Customer,

Thank you for being one of our {customer_count:,} loyal customers! 
You've made an average of {segment_data['Frequency'].mean():.1f} purchases with us, 
spending an average of ${avg_monetary:.2f} per transaction.

🎁 SPECIAL OFFER: 15% OFF your next purchase
⏰ Valid until: {datetime.now().strftime('%B %d, %Y')}
🏷️ Use code: LOYAL15

Plus, enjoy:
• Free priority shipping
• Early access to new products
• Exclusive member-only events

Shop now: https://janah-hardware.com/vip

Best regards,
The Janah Hardware Team
            """
        },
        "At-Risk Customers": {
            "subject": "💝 We Miss You! Special Comeback Offer",
            "content": f"""
Dear Customer,

We noticed you haven't visited us in {avg_recency:.0f} days, and we miss you!
You're one of {customer_count:,} customers we'd love to see back.

🎯 COMEBACK OFFER: 25% OFF your next purchase
⏰ Limited time: {datetime.now().strftime('%B %d, %Y')}
🏷️ Use code: COMEBACK25

What's new:
• New product arrivals
• Improved customer service
• Better prices than ever

Come back to us: https://janah-hardware.com/welcome-back

We're here for you,
The Janah Hardware Team
            """
        },
        "New Customers": {
            "subject": "👋 Welcome to Janah Hardware! Your First Order Awaits",
            "content": f"""
Welcome to Janah Hardware!

We're excited to have you as one of our {customer_count:,} new customers!
Start your journey with us and discover quality tools and hardware.

🎁 WELCOME OFFER: 20% OFF your first purchase
⏰ Valid for: 30 days from today
🏷️ Use code: WELCOME20

What you'll find:
• Quality tools and equipment
• Expert advice and support
• Competitive prices
• Fast delivery

Start shopping: https://janah-hardware.com/first-order

Welcome aboard,
The Janah Hardware Team
            """
        },
        "High-Value Customers": {
            "subject": "💎 Premium Service Update for Our VIP Customers",
            "content": f"""
Dear Premium Customer,

You're one of our {customer_count:,} highest-value customers!
Your average spend of ${avg_monetary:.2f} makes you part of our elite group.

💎 PREMIUM BENEFITS:
• Personal account manager
• Priority customer service
• Exclusive product previews
• Custom pricing options

🎯 SPECIAL OFFER: 10% OFF + Free Express Shipping
⏰ Valid until: {datetime.now().strftime('%B %d, %Y')}
🏷️ Use code: PREMIUM10

Contact your manager: premium@janah-hardware.com

Best regards,
The Janah Premium Team
            """
        },
        "Inactive Customers": {
            "subject": "🔄 Reconnect with Janah Hardware - Special Re-engagement Offer",
            "content": f"""
Dear Customer,

It's been {avg_recency:.0f} days since your last visit, and we'd love to reconnect!
You're one of {customer_count:,} customers we're reaching out to.

🔄 RE-ENGAGEMENT OFFER: 30% OFF your next purchase
⏰ Limited time: {datetime.now().strftime('%B %d, %Y')}
🏷️ Use code: RECONNECT30

What's changed:
• New product lines
• Improved website
• Better customer service
• More competitive prices

Reconnect with us: https://janah-hardware.com/reconnect

We hope to see you soon,
The Janah Hardware Team
            """
        }
    }
    
    template = campaign_templates.get(segment_name, {
        "subject": "Special Offer from Janah Hardware",
        "content": "Thank you for being our customer!"
    })
    
    return template

def is_streamlit_context():
    """Check if we're running in Streamlit context"""
    try:
        import streamlit as st
        return True
    except ImportError:
        return False

def main():
    """Main Streamlit application"""
    
    # Check if we're in Streamlit context
    if not is_streamlit_context():
        print("Running in non-Streamlit context (background processing)")
        return
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📊 Janah Customer Segmentation Analysis</h1>
        <p>RFM Analysis and K-means Clustering for Customer Segmentation</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar configuration
    st.sidebar.header("⚙️ Configuration")
    
    # File upload
    uploaded_file = st.sidebar.file_uploader(
        "Upload your dataset (CSV)",
        type=['csv'],
        help="Upload your customer transaction data in CSV format"
    )
    
    # Default dataset path
    default_dataset_path = "data/online_retail.csv"
    
    # Determine which dataset to use
    if uploaded_file is not None:
        st.sidebar.success(f"✅ File uploaded: {uploaded_file.name}")
        # Save uploaded file temporarily
        with open("temp_upload.csv", "wb") as f:
            f.write(uploaded_file.getbuffer())
        dataset_path = "temp_upload.csv"
    else:
        if os.path.exists(default_dataset_path):
            st.sidebar.info("📁 Using default dataset: online_retail.csv")
            dataset_path = default_dataset_path
        else:
            st.sidebar.warning("⚠️ No dataset found. Please upload a CSV file.")
            st.stop()
    
    # Clustering parameters
    st.sidebar.subheader("🔧 Clustering Parameters")
    use_elbow_method = st.sidebar.checkbox("Use Elbow Method", value=True, 
                                          help="Automatically determine optimal number of clusters")
    
    if not use_elbow_method:
        n_clusters = st.sidebar.slider("Number of Clusters", 3, 6, 4)
    else:
        n_clusters = None
    
    # Analysis options
    st.sidebar.subheader("📋 Analysis Options")
    show_visualizations = st.sidebar.checkbox("Show Visualizations", value=True)
    save_results = st.sidebar.checkbox("Save Results", value=True)
    
    # Run analysis button
    if st.sidebar.button("🚀 Run Analysis", type="primary"):
        with st.spinner("Running analysis..."):
            
            # Step 1: Load and clean data
            data = load_and_clean_data(dataset_path)
            if data is None:
                st.error("❌ Failed to load data. Please check your file.")
                return
            
            # Display data preview
            st.subheader("📋 Data Preview")
            st.write(data.head())
            
            # Step 2: Calculate RFM metrics
            rfm_data = calculate_rfm(data)
            if rfm_data is None:
                st.error("❌ Failed to calculate RFM metrics.")
                return
            
            # Step 3: Perform clustering
            clustered_data, optimal_clusters, model = perform_clustering(rfm_data, n_clusters)
            if clustered_data is None:
                st.error("❌ Failed to perform clustering.")
                return
            
            # Step 4: Create visualizations (use Streamlit version)
            if show_visualizations:
                create_visualizations_streamlit(clustered_data)
            
            # Step 5: Display results
            st.subheader("📊 Analysis Results")
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Customers", len(clustered_data))
            with col2:
                st.metric("Number of Clusters", optimal_clusters)
            with col3:
                st.metric("Avg Recency", f"{clustered_data['Recency'].mean():.1f} days")
            with col4:
                st.metric("Avg Monetary", f"${clustered_data['Monetary'].mean():.0f}")
            
            # Cluster analysis
            st.subheader("🎯 Cluster Analysis")
            
            # Create cluster summary table
            cluster_summary = clustered_data.groupby('Cluster').agg({
                'Recency': ['mean', 'std'],
                'Frequency': ['mean', 'std'],
                'Monetary': ['mean', 'std']
            }).round(2)
            
            cluster_summary.columns = ['Recency_Mean', 'Recency_Std', 'Frequency_Mean', 'Frequency_Std', 
                                     'Monetary_Mean', 'Monetary_Std']
            cluster_summary['Size'] = clustered_data['Cluster'].value_counts().sort_index()
            cluster_summary['Percentage'] = (cluster_summary['Size'] / len(clustered_data) * 100).round(1)
            
            st.write("**Cluster Summary Statistics:**")
            st.dataframe(cluster_summary)
            
            # Save results if requested
            if save_results:
                output_path = "data/processed/rfm_clustered.csv"
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                clustered_data.to_csv(output_path, index=False)
                st.success(f"✅ Results saved to: {output_path}")
            
            # Clean up temporary file
            if uploaded_file is not None and os.path.exists("temp_upload.csv"):
                os.remove("temp_upload.csv")
    
    # Post-segmentation features
    st.markdown("---")
    st.header("📋 Post-Segmentation Actions")
    
    # Download Report
    st.subheader("📄 Download Analysis Report")
    report_content = generate_report(clustered_data, {"data_source": "Uploaded File" if uploaded_file else "Default Dataset", "n_clusters": optimal_clusters or "Auto", "total_customers": len(clustered_data)})
    
    st.download_button(
        label="📥 Download Report (TXT)",
        data=report_content,
        file_name=f"janah_segmentation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain"
    )
    
    # Export Segment Data
    st.subheader("📊 Export Segment Data")
    csv_data = clustered_data.to_csv(index=False)
    
    st.download_button(
        label="📥 Export RFM Data (CSV)",
        data=csv_data,
        file_name=f"janah_rfm_segments_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )
    
    # Campaign Preview
    st.subheader("📧 Campaign Preview")
    segment_options = sorted(clustered_data['Segment'].unique())
    selected_segment = st.selectbox(
        "Select segment for campaign preview:",
        segment_options
    )
    
    if st.button("👀 Preview Campaign"):
        campaign = create_campaign_preview(selected_segment, clustered_data)
        
        st.markdown('<div class="campaign-preview">', unsafe_allow_html=True)
        st.write("**Email Subject:**")
        st.write(campaign["subject"])
        st.write("**Email Content:**")
        st.text_area("Campaign Content", campaign["content"], height=300, disabled=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Share Results
    st.subheader("🔗 Share Results")
    st.markdown("""
    **Share your analysis results:**
    
    📱 **Local Deployment:** http://localhost:5000/results
    
    🌐 **Public Deployment:** Coming soon...
    
    📧 **Email Share:** Copy the report link above and share with your team.
    """)
    
    # Display metrics
    st.subheader("📈 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Customers", f"{len(clustered_data):,}")
    
    with col2:
        st.metric("Segments", clustered_data['Cluster'].nunique())
    
    with col3:
        st.metric("Avg Recency", f"{clustered_data['Recency'].mean():.1f} days")
    
    with col4:
        st.metric("Avg Monetary", f"${clustered_data['Monetary'].mean():,.0f}")

if __name__ == "__main__":
    main()
