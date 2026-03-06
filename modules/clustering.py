"""
Clustering module for customer segmentation and item grouping.
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score


def find_optimal_clusters(data, max_k=10):
    """
    Find optimal number of clusters using elbow method and silhouette score.
    
    Args:
        data: Feature matrix for clustering
        max_k: Maximum number of clusters to try
    
    Returns:
        Dictionary with inertias and silhouette scores
    """
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)
    
    results = {
        'k': [],
        'inertia': [],
        'silhouette': []
    }
    
    for k in range(2, max_k + 1):
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = kmeans.fit_predict(data_scaled)
        
        results['k'].append(k)
        results['inertia'].append(kmeans.inertia_)
        results['silhouette'].append(silhouette_score(data_scaled, labels))
    
    return results


def perform_customer_segmentation(rfm_df, n_clusters=4):
    """
    Segment customers using K-Means clustering on RFM features.
    
    Args:
        rfm_df: DataFrame with RFM features
        n_clusters: Number of clusters
    
    Returns:
        DataFrame with cluster assignments, cluster centers
    """
    df = rfm_df.copy()
    
    # Select features for clustering
    features = ['recency', 'frequency', 'monetary']
    X = df[features]
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Apply K-Means
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df['cluster'] = kmeans.fit_predict(X_scaled)
    
    # Get cluster centers (in original scale)
    cluster_centers = pd.DataFrame(
        scaler.inverse_transform(kmeans.cluster_centers_),
        columns=features
    )
    cluster_centers['cluster'] = range(n_clusters)
    
    # Calculate silhouette score
    sil_score = silhouette_score(X_scaled, df['cluster'])
    
    # Cluster statistics
    cluster_stats = df.groupby('cluster').agg({
        'customer_id': 'count',
        'recency': 'mean',
        'frequency': 'mean',
        'monetary': 'mean'
    }).reset_index()
    cluster_stats.columns = ['cluster', 'num_customers', 'avg_recency', 
                             'avg_frequency', 'avg_monetary']
    
    return df, cluster_stats, sil_score


def segment_menu_items(item_sales_df, n_clusters=4):
    """
    Cluster menu items based on sales performance.
    
    Args:
        item_sales_df: DataFrame with item sales data
        n_clusters: Number of clusters
    
    Returns:
        DataFrame with cluster assignments
    """
    df = item_sales_df.copy()
    
    # Features for clustering
    features = ['price', 'total_quantity', 'total_revenue']
    X = df[features].fillna(0)
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Apply K-Means
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df['item_cluster'] = kmeans.fit_predict(X_scaled)
    
    # Name clusters based on characteristics
    cluster_names = {0: 'Budget Items', 1: 'Popular Items', 
                     2: 'Premium Items', 3: 'Specialty Items'}
    
    return df


def get_cluster_profiles(clustered_df, cluster_col='cluster'):
    """
    Generate detailed profiles for each cluster.
    
    Args:
        clustered_df: DataFrame with cluster assignments
        cluster_col: Name of cluster column
    
    Returns:
        DataFrame with cluster profiles
    """
    # Get numeric columns
    numeric_cols = clustered_df.select_dtypes(include=[np.number]).columns
    numeric_cols = [c for c in numeric_cols if c != cluster_col]
    
    profiles = clustered_df.groupby(cluster_col)[numeric_cols].agg(['mean', 'std'])
    
    return profiles
