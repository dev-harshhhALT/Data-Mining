"""
Customer Segments Page - K-Means clustering analysis.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_connection import get_all_transactions
from modules.preprocessing import create_rfm_features
from modules.clustering import (
    perform_customer_segmentation, find_optimal_clusters,
    get_cluster_profiles
)
from modules.classification import classify_customers

from utils.ui import (
    setup_page_config, setup_sidebar, apply_custom_css,
    get_chart_colors, chart_layout, render_section_title, render_footer
)

setup_page_config(page_title="Customer Segments")

# Setup UI
dark_mode = setup_sidebar()
colors = apply_custom_css(dark_mode)
CHART_COLORS = get_chart_colors()

render_section_title("Customer Segmentation")
st.markdown(f"<p style='color:{colors['text_muted']};margin-top:-10px;margin-bottom:8px;'>K-Means RFM clustering — understand your customer groups.</p>", unsafe_allow_html=True)



# Load data
@st.cache_data
def load_customer_data():
    transactions = get_all_transactions()
    rfm = create_rfm_features(transactions)
    return transactions, rfm

transactions, rfm_data = load_customer_data()

# Sidebar controls
st.sidebar.header("Clustering Parameters")
n_clusters = st.sidebar.slider(
    "Number of Clusters",
    min_value=2,
    max_value=8,
    value=4,
    help="Number of customer segments to create"
)

# Tabs
tab1, tab2, tab3 = st.tabs(["RFM Analysis", "Cluster Analysis", "Segment Profiles"])

with tab1:
    st.subheader("RFM (Recency, Frequency, Monetary) Analysis")
    
    st.markdown("""
    RFM Analysis segments customers based on:
    - **Recency**: How recently did they purchase?
    - **Frequency**: How often do they purchase?
    - **Monetary**: How much do they spend?
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Customers", len(rfm_data))
    with col2:
        st.metric("Avg Recency (days)", f"{rfm_data['recency'].mean():.1f}")
    with col3:
        st.metric("Avg Monetary Value", f"Rs. {rfm_data['monetary'].mean():.2f}")
    
    st.markdown("---")
    
    # RFM Distributions
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fig = px.histogram(
            rfm_data, x='recency', 
            title='Recency Distribution',
            labels={'recency': 'Days Since Last Purchase'},
            color_discrete_sequence=[CHART_COLORS[0]]
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=colors['text_color'])
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.histogram(
            rfm_data, x='frequency',
            title='Frequency Distribution',
            labels={'frequency': 'Number of Transactions'},
            color_discrete_sequence=[CHART_COLORS[1]]
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=colors['text_color'])
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        fig = px.histogram(
            rfm_data, x='monetary',
            title='Monetary Distribution',
            labels={'monetary': 'Total Spend (Rs.)'},
            color_discrete_sequence=[CHART_COLORS[2]]
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=colors['text_color'])
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # RFM Classification
    st.subheader("Customer Classification")
    classified = classify_customers(rfm_data)
    
    segment_counts = classified['customer_segment'].value_counts().reset_index()
    segment_counts.columns = ['Segment', 'Count']
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(
            segment_counts,
            values='Count',
            names='Segment',
            title='Customer Segments Distribution',
            hole=0.4,
            color_discrete_sequence=CHART_COLORS
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=colors['text_color'])
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.dataframe(segment_counts, use_container_width=True, hide_index=True)
        
        with st.expander("Segment Descriptions"):
            st.markdown("""
            - **Champions**: Recent, frequent, high spenders
            - **Loyal Customers**: Regular valuable customers
            - **Potential Loyalists**: Recent customers with potential
            - **At Risk**: Were good customers, haven't purchased recently
            - **Lost**: Haven't purchased in a long time
            """)

with tab2:
    st.subheader("K-Means Clustering Analysis")
    
    # Find optimal clusters
    with st.expander("Optimal Clusters Analysis (Elbow Method)"):
        cluster_results = find_optimal_clusters(rfm_data[['recency', 'frequency', 'monetary']])
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.line(
                x=cluster_results['k'],
                y=cluster_results['inertia'],
                markers=True,
                title='Elbow Method',
                labels={'x': 'Number of Clusters (K)', 'y': 'Inertia'},
                color_discrete_sequence=[CHART_COLORS[3]]
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color=colors['text_color'])
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.line(
                x=cluster_results['k'],
                y=cluster_results['silhouette'],
                markers=True,
                title='Silhouette Score',
                labels={'x': 'Number of Clusters (K)', 'y': 'Silhouette Score'},
                color_discrete_sequence=[CHART_COLORS[4]]
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color=colors['text_color'])
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Perform clustering
    clustered_data, cluster_stats, silhouette = perform_customer_segmentation(
        rfm_data, n_clusters=n_clusters
    )
    
    st.metric("Silhouette Score", f"{silhouette:.4f}", help="Higher is better (max 1.0)")
    
    st.markdown("---")
    
    # Visualize clusters
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.scatter(
            clustered_data,
            x='recency',
            y='monetary',
            color='cluster',
            title='Clusters: Recency vs Monetary',
            labels={'cluster': 'Cluster'},
            color_continuous_scale='Viridis'
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=colors['text_color'])
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.scatter(
            clustered_data,
            x='frequency',
            y='monetary',
            color='cluster',
            title='Clusters: Frequency vs Monetary',
            labels={'cluster': 'Cluster'},
            color_continuous_scale='Viridis'
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=colors['text_color'])
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # 3D visualization
    st.subheader("3D Cluster Visualization")
    fig = px.scatter_3d(
        clustered_data,
        x='recency',
        y='frequency',
        z='monetary',
        color='cluster',
        title='Customer Clusters in 3D (RFM Space)',
        labels={'cluster': 'Cluster'}
    )
    fig.update_layout(
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=colors['text_color'])
    )
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Cluster Profiles")
    
    # Cluster statistics
    st.markdown("#### Cluster Summary Statistics")
    
    cluster_stats_display = cluster_stats.copy()
    cluster_stats_display['avg_recency'] = cluster_stats_display['avg_recency'].round(1)
    cluster_stats_display['avg_frequency'] = cluster_stats_display['avg_frequency'].round(1)
    cluster_stats_display['avg_monetary'] = cluster_stats_display['avg_monetary'].round(2)
    
    st.dataframe(cluster_stats_display, use_container_width=True, hide_index=True)
    
    # Cluster characteristics
    st.markdown("#### Cluster Characteristics")
    
    for i in range(n_clusters):
        cluster_data = cluster_stats[cluster_stats['cluster'] == i].iloc[0]
        
        with st.expander(f"Cluster {i} ({int(cluster_data['num_customers'])} customers)"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Avg Recency", f"{cluster_data['avg_recency']:.1f} days")
            with col2:
                st.metric("Avg Frequency", f"{cluster_data['avg_frequency']:.1f} orders")
            with col3:
                st.metric("Avg Monetary", f"Rs. {cluster_data['avg_monetary']:.2f}")
            
            # Characterization
            avg_rec = cluster_data['avg_recency']
            avg_freq = cluster_data['avg_frequency']
            avg_mon = cluster_data['avg_monetary']
            
            overall_avg_rec = cluster_stats['avg_recency'].mean()
            overall_avg_freq = cluster_stats['avg_frequency'].mean()
            overall_avg_mon = cluster_stats['avg_monetary'].mean()
            
            characteristics = []
            if avg_rec < overall_avg_rec:
                characteristics.append("Recent buyers")
            else:
                characteristics.append("Past buyers")
            
            if avg_freq > overall_avg_freq:
                characteristics.append("Frequent shoppers")
            else:
                characteristics.append("Occasional shoppers")
            
            if avg_mon > overall_avg_mon:
                characteristics.append("High spenders")
            else:
                characteristics.append("Budget conscious")
            
            st.info(f"**Profile**: {', '.join(characteristics)}")
    
    # Recommendations
    st.markdown("---")
    st.subheader("Marketing Recommendations")
    
    st.markdown("""
    Based on the cluster analysis, consider these strategies:
    
    | Cluster Type | Recommended Action |
    |--------------|-------------------|
    | High Value, Recent | VIP treatment, exclusive offers |
    | High Value, Not Recent | Re-engagement campaigns |
    | Low Value, Frequent | Upselling opportunities |
    | Low Value, Infrequent | Promotional discounts |
    """)
