import pandas as pd
import numpy as np

class DataCleaner:
    def __init__(self):
        pass
    
    def clean_data(self, df):
        """Clean and preprocess customer data"""
        # Remove duplicates
        df_clean = df.drop_duplicates()
        
        # Handle missing values
        df_clean = df_clean.fillna(df_clean.mean(numeric_only=True))
        
        return df_clean
