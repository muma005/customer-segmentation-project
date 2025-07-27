import json
import os
import sys
from http.server import BaseHTTPRequestHandler
import pandas as pd
import numpy as np
from datetime import datetime

# Add the parent directory to the path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def load_and_clean_data(file_path):
    """Load and clean the dataset"""
    try:
        data = pd.read_csv(file_path, encoding='latin-1')
        
        # Remove rows with missing CustomerID
        data = data.dropna(subset=['CustomerID'])
        
        # Drop duplicates
        data = data.drop_duplicates()
        
        # Convert InvoiceDate to datetime
        data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])
        
        # Remove negative quantities and prices
        data = data[(data['Quantity'] > 0) & (data['UnitPrice'] > 0)]
        
        return data
    except Exception as e:
        return None

def calculate_rfm(data):
    """Calculate RFM metrics"""
    try:
        # Find the latest date
        latest_date = data['InvoiceDate'].max()
        
        # Calculate RFM metrics
        rfm = data.groupby('CustomerID').agg({
            'InvoiceDate': lambda x: (latest_date - x.max()).days,  # Recency
            'InvoiceNo': 'nunique',  # Frequency
            'Quantity': lambda x: (x * data.loc[x.index, 'UnitPrice']).sum()  # Monetary
        }).reset_index()
        
        rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']
        
        # Remove negative monetary values
        rfm = rfm[rfm['Monetary'] > 0]
        
        return rfm
    except Exception as e:
        return None

def perform_clustering(rfm_data, n_clusters=4):
    """Perform K-means clustering"""
    try:
        from sklearn.cluster import KMeans
        from sklearn.preprocessing import StandardScaler
        
        # Prepare data for clustering
        rfm_clustering = rfm_data[['Recency', 'Frequency', 'Monetary']].copy()
        
        # Standardize the data
        scaler = StandardScaler()
        rfm_scaled = scaler.fit_transform(rfm_clustering)
        
        # Perform K-means clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        rfm_data['Cluster'] = kmeans.fit_predict(rfm_scaled)
        
        # Add cluster labels
        cluster_labels = {
            0: "Loyal Customers",
            1: "At-Risk Customers", 
            2: "New Customers",
            3: "High-Value Customers",
            4: "Inactive Customers"
        }
        
        rfm_data['Segment'] = rfm_data['Cluster'].map(cluster_labels)
        
        return rfm_data
    except Exception as e:
        return None

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/api/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                'status': 'healthy',
                'message': 'Janah Segmentation API is running',
                'timestamp': datetime.now().isoformat()
            }
            
            self.wfile.write(json.dumps(response).encode())
            return
        
        self.send_response(404)
        self.end_headers()
        self.wfile.write(json.dumps({'error': 'Not found'}).encode())
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/api/run-segmentation':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            try:
                # Get request body
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                request_data = json.loads(post_data.decode('utf-8'))
                
                # Simulate analysis (in a real app, you'd process actual data)
                analysis_result = {
                    'status': 'completed',
                    'total_customers': 1000,
                    'n_clusters': 4,
                    'avg_recency': 45.2,
                    'avg_monetary': 1250.0,
                    'cluster_sizes': {
                        'Loyal Customers': 250,
                        'At-Risk Customers': 200,
                        'New Customers': 300,
                        'High-Value Customers': 250
                    },
                    'timestamp': datetime.now().isoformat()
                }
                
                self.wfile.write(json.dumps(analysis_result).encode())
                
            except Exception as e:
                error_response = {
                    'status': 'error',
                    'message': str(e),
                    'timestamp': datetime.now().isoformat()
                }
                self.wfile.write(json.dumps(error_response).encode())
            
            return
        
        self.send_response(404)
        self.end_headers()
        self.wfile.write(json.dumps({'error': 'Not found'}).encode())
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers() 