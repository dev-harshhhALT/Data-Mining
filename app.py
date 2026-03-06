"""
Data Mining Menu Planning - Main Streamlit Application
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db_connection import (
    get_sales_summary, get_item_sales, get_daily_sales,
    get_all_menu_items, get_all_transactions, get_transaction_items,
    initialize_database
)
from utils.helpers import format_currency
from utils.ui import (
    setup_page_config, setup_sidebar, apply_custom_css,
    get_chart_colors, chart_layout,
    render_hero, render_section_title, render_kpi_cards,
    render_stat_row, render_footer
)

setup_page_config(page_title="Menu Planning Analytics")

dark_mode = setup_sidebar()
colors = apply_custom_css(dark_mode)
CHART_COLORS = get_chart_colors()
text_color = colors['text_color']
accent_color = colors['accent_color']

# ── Hero Banner ──────────────────────────────
render_hero(
    title="Data Mining Menu Planning System",
    subtitle="Hospitality Industry Analytics Dashboard",
    badge="Live Analytics"
)

# ── Guard: check for data ────────────────────
try:
    summary = get_sales_summary()
    if summary.empty or summary['total_transactions'].iloc[0] == 0:
        st.warning("⚠️ No data found in database. Please run data generation first.")
        st.code("python data/generate_data.py", language="bash")
        st.stop()
except Exception as e:
    st.error(f"Database error: {e}")
    st.info("Initializing database...")
    initialize_database()
    st.warning("Database initialized. Please generate data:")
    st.code("python data/generate_data.py", language="bash")
    st.stop()

# ── KPI Cards ───────────────────────────────
total_transactions = int(pd.to_numeric(summary['total_transactions'], errors='coerce').fillna(0).iloc[0])
total_revenue      = float(pd.to_numeric(summary['total_revenue'], errors='coerce').fillna(0).iloc[0])
avg_value          = float(pd.to_numeric(summary['avg_transaction_value'], errors='coerce').fillna(0).iloc[0])
unique_customers   = int(pd.to_numeric(summary['unique_customers'], errors='coerce').fillna(0).iloc[0])

render_section_title("Key Performance Indicators")

render_kpi_cards([
    {
        "label": "Total Transactions",
        "value": f"{total_transactions:,}",
        "delta": "All Time",
        "color": "#14b8a6",
    },
    {
        "label": "Total Revenue",
        "value": format_currency(total_revenue),
        "delta": "All Time",
        "color": "#f97316",
    },
    {
        "label": "Avg Order Value",
        "value": format_currency(avg_value),
        "delta": "Per Transaction",
        "color": "#8b5cf6",
    },
    {
        "label": "Unique Customers",
        "value": f"{unique_customers:,}",
        "delta": "Registered",
        "color": "#06b6d4",
    },
])


st.markdown("<br>", unsafe_allow_html=True)

# ── Charts Row 1 ─────────────────────────────
render_section_title("Top Selling Items & Revenue Split")

col1, col2 = st.columns(2)
item_sales = get_item_sales()

with col1:
    top_items = item_sales.nlargest(10, 'total_quantity')
    fig = px.bar(
        top_items,
        x='total_quantity',
        y='item_name',
        orientation='h',
        color='category',
        color_discrete_sequence=CHART_COLORS,
        labels={'total_quantity': 'Qty Sold', 'item_name': ''}
    )
    fig.update_layout(**chart_layout(dark_mode, height=420))
    fig.update_layout(yaxis={'categoryorder': 'total ascending'}, showlegend=True,
                      legend=dict(orientation='h', yanchor='bottom', y=1.02))
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    category_revenue = item_sales.groupby('category')['total_revenue'].sum().reset_index()
    fig = px.pie(
        category_revenue,
        values='total_revenue',
        names='category',
        hole=0.55,
        color_discrete_sequence=CHART_COLORS
    )
    fig.update_traces(textposition='inside', textinfo='percent+label', textfont_size=11)
    fig.update_layout(**chart_layout(dark_mode, height=420))
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Charts Row 2 ─────────────────────────────
render_section_title("Revenue Trends & Weekly Patterns")

col1, col2 = st.columns(2)

with col1:
    daily_sales = get_daily_sales()
    daily_sales['date'] = pd.to_datetime(daily_sales['date'])
    daily_sales['ma_7'] = daily_sales['daily_revenue'].rolling(window=7).mean()

    fig = px.line(
        daily_sales,
        x='date',
        y=['daily_revenue', 'ma_7'],
        labels={'value': 'Revenue (Rs.)', 'date': '', 'variable': ''},
        color_discrete_sequence=[CHART_COLORS[1], CHART_COLORS[0]]
    )
    fig.update_layout(**chart_layout(dark_mode, height=360))
    fig.update_layout(legend=dict(orientation='h', yanchor='bottom', y=1.02))
    fig.for_each_trace(lambda t: t.update(
        name={'daily_revenue': 'Daily Revenue', 'ma_7': '7-Day Avg'}.get(t.name, t.name)
    ))
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    transactions = get_all_transactions()
    transactions['date'] = pd.to_datetime(transactions['date'])
    transactions['day_of_week'] = transactions['date'].dt.day_name()

    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_sales = transactions.groupby('day_of_week')['total_amount'].mean().reset_index()
    day_sales['day_of_week'] = pd.Categorical(day_sales['day_of_week'], categories=day_order, ordered=True)
    day_sales = day_sales.sort_values('day_of_week')

    fig = px.bar(
        day_sales,
        x='day_of_week',
        y='total_amount',
        labels={'total_amount': 'Avg Revenue (Rs.)', 'day_of_week': ''},
        color='day_of_week',
        color_discrete_sequence=CHART_COLORS
    )
    fig.update_layout(**chart_layout(dark_mode, height=360))
    fig.update_layout(showlegend=False)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Quick Stats ──────────────────────────────
render_section_title("Quick Statistics")

menu_items = get_all_menu_items()
trans_items = get_transaction_items()

col1, col2, col3 = st.columns(3)

with col1:
    render_stat_row("Total Menu Items", f"{len(menu_items)}")
    render_stat_row("Menu Categories", f"{menu_items['category'].nunique()}")

with col2:
    render_stat_row("Average Item Price", format_currency(menu_items['price'].mean()))
    render_stat_row("Menu Categories", f"{menu_items['category'].nunique()}")

with col3:
    avg_basket = trans_items.groupby('transaction_id').size().mean()
    render_stat_row("Avg Items per Order", f"{avg_basket:.1f}")
    render_stat_row("Total Items Sold", f"{trans_items['quantity'].sum():,}")

# ── Footer ───────────────────────────────────
render_footer()
