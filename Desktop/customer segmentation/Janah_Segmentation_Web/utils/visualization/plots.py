import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

class SegmentationPlotter:
    def __init__(self):
        pass
    
    def plot_clusters(self, df, x_col, y_col, cluster_col):
        """Create cluster visualization"""
        fig = px.scatter(df, x=x_col, y=y_col, color=cluster_col)
        return fig
