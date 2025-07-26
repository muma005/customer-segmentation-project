from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd

class CustomerSegmentation:
    def __init__(self, n_clusters=4):
        self.n_clusters = n_clusters
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        self.scaler = StandardScaler()
    
    def fit_predict(self, data):
        """Fit the model and predict clusters"""
        scaled_data = self.scaler.fit_transform(data)
        clusters = self.kmeans.fit_predict(scaled_data)
        return clusters
