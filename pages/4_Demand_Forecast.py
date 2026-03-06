"""
Demand Forecast Page - Time series analysis and predictions.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_connection import get_daily_sales, get_transaction_items
from modules.prediction import (
    train_demand_model, forecast_next_days,
    calculate_moving_averages, get_seasonal_analysis,
    predict_item_demand
)

from utils.ui import (
    setup_page_config, setup_sidebar, apply_custom_css,
    get_chart_colors, chart_layout, render_section_title, render_footer
)

setup_page_config(page_title="Demand Forecast")

# Setup UI
dark_mode = setup_sidebar()
colors = apply_custom_css(dark_mode)
CHART_COLORS = get_chart_colors()

render_section_title("Demand Forecasting")
st.markdown(f"<p style='color:{colors['text_muted']};margin-top:-10px;margin-bottom:8px;'>Sales predictions for the next 30 days using time series models.</p>", unsafe_allow_html=True)

st.markdown("Predict future demand using time series analysis.")

# Load data
@st.cache_data
def load_sales_data():
    daily_sales = get_daily_sales()
    daily_sales['date'] = pd.to_datetime(daily_sales['date'])
    return daily_sales

daily_sales = load_sales_data()

# Sidebar
st.sidebar.header("Forecast Settings")
forecast_days = st.sidebar.slider(
    "Days to Forecast",
    min_value=7,
    max_value=60,
    value=30,
    help="Number of days to predict into the future"
)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Trends", "Seasonal Analysis", "Forecast", "Item Demand"])

with tab1:
    st.subheader("Sales Trends")
    
    # Add moving averages
    sales_with_ma = calculate_moving_averages(daily_sales)
    
    # Main trend chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=sales_with_ma['date'],
        y=sales_with_ma['daily_revenue'],
        mode='lines',
        name='Daily Revenue',
        line=dict(color=CHART_COLORS[0], width=1)
    ))
    
    fig.add_trace(go.Scatter(
        x=sales_with_ma['date'],
        y=sales_with_ma['ma_7'],
        mode='lines',
        name='7-Day MA',
        line=dict(color=CHART_COLORS[1], width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=sales_with_ma['date'],
        y=sales_with_ma['ma_30'],
        mode='lines',
        name='30-Day MA',
        line=dict(color=CHART_COLORS[2], width=2)
    ))
    
    fig.update_layout(
        title='Daily Revenue with Moving Averages',
        xaxis_title='Date',
        yaxis_title='Revenue (Rs.)',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=colors['text_color'])
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Revenue", f"Rs. {daily_sales['daily_revenue'].sum():,.2f}")
    with col2:
        st.metric("Avg Daily Revenue", f"Rs. {daily_sales['daily_revenue'].mean():,.2f}")
    with col3:
        st.metric("Peak Day Revenue", f"Rs. {daily_sales['daily_revenue'].max():,.2f}")
    with col4:
        st.metric("Total Days", len(daily_sales))

with tab2:
    st.subheader("Seasonal Analysis")
    
    seasonal = get_seasonal_analysis(daily_sales)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Revenue by Day of Week")
        day_data = pd.DataFrame({
            'Day': list(seasonal['by_day_of_week'].keys()),
            'Avg Revenue': list(seasonal['by_day_of_week'].values())
        })
        
        fig = px.bar(
            day_data,
            x='Day',
            y='Avg Revenue',
            color='Avg Revenue',
            color_continuous_scale='Blues'
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=colors['text_color'])
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.success(f"**Best Day**: {seasonal['best_day']}")
        st.warning(f"**Slowest Day**: {seasonal['worst_day']}")
    
    with col2:
        st.markdown("#### Revenue by Month")
        month_data = pd.DataFrame({
            'Month': list(seasonal['by_month'].keys()),
            'Avg Revenue': list(seasonal['by_month'].values())
        })
        
        fig = px.bar(
            month_data,
            x='Month',
            y='Avg Revenue',
            color='Avg Revenue',
            color_continuous_scale='Greens'
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=colors['text_color'])
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Heatmap
    st.markdown("#### Weekly Revenue Patterns")
    daily_sales['day_of_week'] = daily_sales['date'].dt.day_name()
    daily_sales['week'] = daily_sales['date'].dt.isocalendar().week
    
    pivot = daily_sales.pivot_table(
        values='daily_revenue',
        index='week',
        columns='day_of_week',
        aggfunc='mean'
    )
    
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    pivot = pivot.reindex(columns=[d for d in day_order if d in pivot.columns])
    
    fig = px.imshow(
        pivot.tail(12),
        color_continuous_scale='Blues',
        title='Weekly Revenue Heatmap (Last 12 Weeks)'
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=colors['text_color'])
    )
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Revenue Forecast")
    
    with st.spinner("Training prediction model..."):
        try:
            model, metrics, feature_importance = train_demand_model(daily_sales)
            forecast = forecast_next_days(model, daily_sales, days=forecast_days)
            
            # Model metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Model R² Score", f"{metrics['r2_score']:.4f}")
            with col2:
                st.metric("RMSE", f"Rs. {metrics['rmse']:,.2f}")
            with col3:
                st.metric("Forecast Days", forecast_days)
            
            st.markdown("---")
            
            # Forecast chart
            fig = go.Figure()
            
            # Historical data
            fig.add_trace(go.Scatter(
                x=daily_sales['date'],
                y=daily_sales['daily_revenue'],
                mode='lines',
                name='Historical',
                line=dict(color=CHART_COLORS[0])
            ))
            
            # Forecast
            fig.add_trace(go.Scatter(
                x=forecast['date'],
                y=forecast['predicted_revenue'],
                mode='lines+markers',
                name='Forecast',
                line=dict(color=CHART_COLORS[3], dash='dash')
            ))
            
            fig.update_layout(
                title=f'{forecast_days}-Day Revenue Forecast',
                xaxis_title='Date',
                yaxis_title='Revenue (Rs.)',
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color=colors['text_color'])
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Forecast summary
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Forecast Summary")
                st.dataframe(
                    forecast.head(14).style.format({'predicted_revenue': 'Rs. {:.2f}'}),
                    use_container_width=True,
                    hide_index=True
                )
            
            with col2:
                st.markdown("#### Feature Importance")
                fig = px.bar(
                    feature_importance,
                    x='coefficient',
                    y='feature',
                    orientation='h',
                    title='',
                    color='coefficient',
                    color_continuous_scale='RdBu'
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color=colors['text_color'])
                )
                st.plotly_chart(fig, use_container_width=True)
                
        except Exception as e:
            st.error(f"Error in forecasting: {e}")
            st.info("Ensure sufficient historical data is available.")

with tab4:
    st.subheader("Item-Level Demand Prediction")
    
    trans_items = get_transaction_items()
    item_demand = predict_item_demand(trans_items)
    
    # Top items by predicted demand
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Highest Predicted Demand (30 Days)")
        top_demand = item_demand.head(10)
        
        fig = px.bar(
            top_demand,
            x='predicted_30_day_demand',
            y='item_name',
            orientation='h',
            color='avg_daily_demand',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Demand Statistics")
        st.dataframe(
            item_demand[['item_name', 'total_quantity', 'avg_daily_demand', 'predicted_30_day_demand']].head(15),
            use_container_width=True,
            hide_index=True
        )
    
    # Inventory planning
    st.markdown("---")
    st.markdown("#### Inventory Planning Recommendations")
    
    high_demand = item_demand[item_demand['predicted_30_day_demand'] > item_demand['predicted_30_day_demand'].median()]
    
    st.info(f"**{len(high_demand)} items** require priority stocking based on predicted demand.")
    
    with st.expander("View High Demand Items"):
        st.dataframe(
            high_demand[['item_name', 'predicted_30_day_demand']],
            use_container_width=True,
            hide_index=True
        )
