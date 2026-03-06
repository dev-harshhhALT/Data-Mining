"""
Data preprocessing module for cleaning and transforming data.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder



def clean_dataframe(df):
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Handle missing values
    for col in df.columns:
        if df[col].dtype in ['float64', 'int64']:
            df[col].fillna(df[col].median(), inplace=True)
        else:
            df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else 'Unknown', inplace=True)
    
    return df


def normalize_numerical(df, columns):
    scaler = StandardScaler()
    df_copy = df.copy()
    
    for col in columns:
        if col in df_copy.columns:
            df_copy[f'{col}_normalized'] = scaler.fit_transform(df_copy[[col]])
    
    return df_copy


def encode_categorical(df, columns):
    df_copy = df.copy()
    encoders = {}
    
    for col in columns:
        if col in df_copy.columns:
            encoder = LabelEncoder()
            df_copy[f'{col}_encoded'] = encoder.fit_transform(df_copy[col].astype(str))
            encoders[col] = encoder
    
    return df_copy, encoders


def create_rfm_features(transactions_df):
    # Convert date to datetime
    transactions_df['date'] = pd.to_datetime(transactions_df['date'])
    
    # Get the most recent date
    max_date = transactions_df['date'].max()
    
    # Calculate RFM metrics
    rfm = transactions_df.groupby('customer_id').agg({
        'date': lambda x: (max_date - x.max()).days,  # Recency
        'transaction_id': 'count',  # Frequency
        'total_amount': 'sum'  # Monetary
    }).reset_index()
    
    rfm.columns = ['customer_id', 'recency', 'frequency', 'monetary']
    
    return rfm


def prepare_basket_data(transaction_items_df):
    # Create basket matrix
    basket = transaction_items_df.groupby(['transaction_id', 'item_name'])['quantity'].sum().unstack()
    basket = basket.fillna(0)
    
    # Convert to binary (1 if item present, 0 otherwise)
    basket = basket.applymap(lambda x: 1 if x > 0 else 0)
    
    return basket


def prepare_time_series(daily_sales_df):
    df = daily_sales_df.copy()
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')
    
    # Create complete date range
    date_range = pd.date_range(start=df.index.min(), end=df.index.max(), freq='D')
    df = df.reindex(date_range, fill_value=0)
    df.index.name = 'date'
    df = df.reset_index()
    
    return df


def calculate_profit_margin(item_sales_df):
    df = item_sales_df.copy()
    # Avoid division by zero
    df['profit_margin'] = df.apply(
        lambda row: ((row['price'] - row['cost']) / row['price'] * 100) if row['price'] > 0 else 0,
        axis=1
    ).round(2)
    return df


def categorize_menu_items(item_sales_df):
    """
    Categorize menu items using Menu Engineering Matrix.
    (Star, Puzzle, Plowhorse, Dog)
    """
    df = item_sales_df.copy()
    
    # Calculate medians for thresholds
    median_quantity = df['total_quantity'].median()
    median_profit = df['total_profit'].median()
    
    def get_category(row):
        high_pop = row['total_quantity'] >= median_quantity
        high_profit = row['total_profit'] >= median_profit
        
        if high_pop and high_profit:
            return 'Star'
        elif not high_pop and high_profit:
            return 'Puzzle'
        elif high_pop and not high_profit:
            return 'Plowhorse'
        else:
            return 'Dog'
    
    df['menu_category'] = df.apply(get_category, axis=1)
    
    return df
