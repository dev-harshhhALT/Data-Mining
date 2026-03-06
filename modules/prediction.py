"""
Prediction module for demand forecasting.
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score


def prepare_time_features(daily_sales_df):
    """
    Create time-based features for prediction.
    
    Args:
        daily_sales_df: DataFrame with date and daily_revenue columns
    
    Returns:
        DataFrame with time features
    """
    df = daily_sales_df.copy()
    df['date'] = pd.to_datetime(df['date'])
    
    # Extract time features
    df['day_of_week'] = df['date'].dt.dayofweek
    df['day_of_month'] = df['date'].dt.day
    df['month'] = df['date'].dt.month
    df['week_of_year'] = df['date'].dt.isocalendar().week
    df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
    
    # Lag features
    df['revenue_lag_1'] = df['daily_revenue'].shift(1)
    df['revenue_lag_7'] = df['daily_revenue'].shift(7)
    
    # Rolling averages
    df['revenue_ma_7'] = df['daily_revenue'].rolling(window=7).mean()
    df['revenue_ma_30'] = df['daily_revenue'].rolling(window=30).mean()
    
    return df.dropna()


def train_demand_model(daily_sales_df):
    """
    Train a Linear Regression model for demand prediction.
    
    Args:
        daily_sales_df: DataFrame with daily sales data
    
    Returns:
        Trained model, metrics, feature list
    """
    df = prepare_time_features(daily_sales_df)
    
    # Features
    feature_cols = ['day_of_week', 'day_of_month', 'month', 'is_weekend',
                    'revenue_lag_1', 'revenue_lag_7', 'revenue_ma_7']
    
    X = df[feature_cols]
    y = df['daily_revenue']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )
    
    # Train model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Predictions
    y_pred = model.predict(X_test)
    
    # Metrics
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    metrics = {
        'rmse': round(rmse, 2),
        'r2_score': round(r2, 4),
        'mse': round(mse, 2)
    }
    
    # Feature importance (coefficients)
    feature_importance = pd.DataFrame({
        'feature': feature_cols,
        'coefficient': model.coef_
    }).sort_values('coefficient', key=abs, ascending=False)
    
    return model, metrics, feature_importance


def forecast_next_days(model, daily_sales_df, days=30):
    """
    Forecast revenue for next N days.
    
    Args:
        model: Trained prediction model
        daily_sales_df: Historical daily sales data
        days: Number of days to forecast
    
    Returns:
        DataFrame with forecasted values
    """
    df = prepare_time_features(daily_sales_df)
    last_date = pd.to_datetime(df['date'].max())
    
    forecasts = []
    
    # Get last known values for lag features
    last_values = df['daily_revenue'].tail(30).tolist()
    
    for i in range(1, days + 1):
        forecast_date = last_date + pd.Timedelta(days=i)
        
        # Create features for forecast date
        features = {
            'day_of_week': forecast_date.dayofweek,
            'day_of_month': forecast_date.day,
            'month': forecast_date.month,
            'is_weekend': 1 if forecast_date.dayofweek in [5, 6] else 0,
            'revenue_lag_1': last_values[-1] if last_values else 0,
            'revenue_lag_7': last_values[-7] if len(last_values) >= 7 else 0,
            'revenue_ma_7': np.mean(last_values[-7:]) if len(last_values) >= 7 else 0
        }
        
        # Predict
        X_forecast = pd.DataFrame([features])
        predicted_revenue = model.predict(X_forecast)[0]
        predicted_revenue = max(0, predicted_revenue)  # Ensure non-negative
        
        forecasts.append({
            'date': forecast_date,
            'predicted_revenue': round(predicted_revenue, 2)
        })
        
        # Update last values for next iteration
        last_values.append(predicted_revenue)
    
    return pd.DataFrame(forecasts)


def calculate_moving_averages(daily_sales_df):
    """
    Calculate various moving averages for trend analysis.
    
    Args:
        daily_sales_df: DataFrame with daily sales
    
    Returns:
        DataFrame with moving averages
    """
    df = daily_sales_df.copy()
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    # Moving averages
    df['ma_7'] = df['daily_revenue'].rolling(window=7).mean()
    df['ma_14'] = df['daily_revenue'].rolling(window=14).mean()
    df['ma_30'] = df['daily_revenue'].rolling(window=30).mean()
    
    return df


def get_seasonal_analysis(daily_sales_df):
    """
    Analyze sales by day of week and month.
    
    Args:
        daily_sales_df: DataFrame with daily sales
    
    Returns:
        Dictionary with seasonal analysis
    """
    df = daily_sales_df.copy()
    df['date'] = pd.to_datetime(df['date'])
    df['day_of_week'] = df['date'].dt.day_name()
    df['month'] = df['date'].dt.month_name()
    
    # Average by day of week
    by_day = df.groupby('day_of_week')['daily_revenue'].mean().round(2)
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
                 'Friday', 'Saturday', 'Sunday']
    by_day = by_day.reindex(day_order)
    
    # Average by month
    by_month = df.groupby('month')['daily_revenue'].mean().round(2)
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    by_month = by_month.reindex([m for m in month_order if m in by_month.index])
    
    return {
        'by_day_of_week': by_day.to_dict(),
        'by_month': by_month.to_dict(),
        'best_day': by_day.idxmax(),
        'worst_day': by_day.idxmin()
    }


def predict_item_demand(transaction_items_df, days=30):
    """
    Predict demand for individual menu items.
    
    Args:
        transaction_items_df: DataFrame with transaction items
        days: Days to analyze
    
    Returns:
        DataFrame with predicted demand per item
    """
    df = transaction_items_df.copy()
    
    # Calculate average daily demand per item
    df['date'] = pd.to_datetime(df['date']) if 'date' in df.columns else None
    
    # Group by item
    item_demand = df.groupby('item_name').agg({
        'quantity': 'sum',
        'transaction_id': 'nunique'
    }).reset_index()
    
    item_demand.columns = ['item_name', 'total_quantity', 'num_transactions']
    
    # Calculate daily average (assuming data spans certain period)
    num_days = max(1, df['transaction_id'].nunique() // 10)  # Approximate
    item_demand['avg_daily_demand'] = (item_demand['total_quantity'] / num_days).round(2)
    item_demand['predicted_30_day_demand'] = (item_demand['avg_daily_demand'] * 30).round(0)
    
    return item_demand.sort_values('total_quantity', ascending=False)
