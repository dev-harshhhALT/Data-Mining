"""
Classification module for menu item popularity analysis.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


def classify_item_popularity(item_sales_df, threshold_percentile=50):
    """
    Classify menu items as Popular or Unpopular based on sales.
    
    Args:
        item_sales_df: DataFrame with item sales data
        threshold_percentile: Percentile threshold for popularity
    
    Returns:
        DataFrame with popularity classification
    """
    df = item_sales_df.copy()
    threshold = np.percentile(df['total_quantity'], threshold_percentile)
    df['popularity'] = df['total_quantity'].apply(
        lambda x: 'Popular' if x >= threshold else 'Unpopular'
    )
    return df


def train_popularity_classifier(item_sales_df):
    """
    Train a Decision Tree classifier to predict item popularity.
    
    Args:
        item_sales_df: DataFrame with item sales and features
    
    Returns:
        Trained model, accuracy score, feature importance
    """
    df = item_sales_df.copy()
    
    # Create target variable
    median_quantity = df['total_quantity'].median()
    df['is_popular'] = (df['total_quantity'] >= median_quantity).astype(int)
    
    # Features
    feature_columns = ['price', 'cost', 'is_veg']
    X = df[feature_columns]
    y = df['is_popular']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    
    # Train Decision Tree
    clf = DecisionTreeClassifier(max_depth=5, random_state=42)
    clf.fit(X_train, y_train)
    
    # Predictions
    y_pred = clf.predict(X_test)
    
    # Metrics
    accuracy = accuracy_score(y_test, y_pred)
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': feature_columns,
        'importance': clf.feature_importances_
    }).sort_values('importance', ascending=False)
    
    return clf, accuracy, feature_importance


def classify_customers(rfm_df):
    """
    Classify customers based on RFM segments.
    
    Args:
        rfm_df: DataFrame with RFM features
    
    Returns:
        DataFrame with customer classifications
    """
    df = rfm_df.copy()
    
    # Calculate quartiles for each RFM metric
    for col in ['recency', 'frequency', 'monetary']:
        df[f'{col}_score'] = pd.qcut(
            df[col], 
            q=4, 
            labels=[4, 3, 2, 1] if col == 'recency' else [1, 2, 3, 4],
            duplicates='drop'
        )
    
    # Calculate overall RFM score
    df['rfm_score'] = (
        df['recency_score'].astype(int) + 
        df['frequency_score'].astype(int) + 
        df['monetary_score'].astype(int)
    )
    
    # Classify customers
    def get_customer_segment(score):
        if score >= 10:
            return 'Champions'
        elif score >= 8:
            return 'Loyal Customers'
        elif score >= 6:
            return 'Potential Loyalists'
        elif score >= 4:
            return 'At Risk'
        else:
            return 'Lost'
    
    df['customer_segment'] = df['rfm_score'].apply(get_customer_segment)
    
    return df


def get_category_performance(transaction_items_df):
    """
    Analyze performance by food category.
    
    Args:
        transaction_items_df: DataFrame with transaction items
    
    Returns:
        DataFrame with category performance metrics
    """
    category_stats = transaction_items_df.groupby('category').agg({
        'quantity': 'sum',
        'subtotal': 'sum',
        'item_name': 'nunique'
    }).reset_index()
    
    category_stats.columns = ['category', 'total_quantity', 'total_revenue', 'num_items']
    category_stats['avg_revenue_per_item'] = (
        category_stats['total_revenue'] / category_stats['num_items']
    ).round(2)
    
    return category_stats.sort_values('total_revenue', ascending=False)
