import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_connection import (
    get_all_menu_items, get_all_transactions,
    get_transaction_items, get_item_sales
)

from utils.helpers import format_currency
from utils.ui import (
    setup_page_config, setup_sidebar, apply_custom_css,
    get_chart_colors, chart_layout, render_section_title, render_footer
)

setup_page_config(page_title="Data Overview")

dark_mode = setup_sidebar()
colors = apply_custom_css(dark_mode)
CHART_COLORS = get_chart_colors()
text_color = colors['text_color']

render_section_title("Data Overview")
st.markdown(
    f"<p style='color:{colors['text_muted']};margin-top:-10px;margin-bottom:16px;'>"
    "Explore the data powering your analytics.</p>",
    unsafe_allow_html=True
)

tab1, tab2, tab3, tab4 = st.tabs([
    "Menu Catalog",
    "Order History",
    "Item Performance",
    "Dataset Summary",
])

# ── Tab 1: Menu Catalog ───────────────────────────────────────────────────────
with tab1:
    menu_items = get_all_menu_items()

    col1, col2 = st.columns([2, 1])
    with col1:
        category_filter = st.multiselect(
            "Filter by Category",
            options=sorted(menu_items['category'].unique()),
            default=sorted(menu_items['category'].unique()),
            key="cat_filter"
        )
    with col2:
        price_range = st.slider(
            "Price Range (Rs.)",
            min_value=int(menu_items['price'].min()),
            max_value=int(menu_items['price'].max()),
            value=(int(menu_items['price'].min()), int(menu_items['price'].max())),
            key="price_filter"
        )

    filtered_items = menu_items[
        menu_items['category'].isin(category_filter) &
        menu_items['price'].between(price_range[0], price_range[1])
    ]

    # Display clean table — no is_veg column (all veg)
    display_df = filtered_items[['item_name', 'category', 'price', 'cost']].copy()
    display_df.columns = ['Item Name', 'Category', 'Price (Rs.)', 'Cost (Rs.)']
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Items", len(filtered_items))
    with col2:
        st.metric("Avg Price", f"Rs. {filtered_items['price'].mean():.0f}")
    with col3:
        valid = filtered_items[filtered_items['price'] > 0]
        margin = ((valid['price'] - valid['cost']) / valid['price'] * 100).mean() if not valid.empty else 0
        st.metric("Avg Profit Margin", f"{margin:.1f}%")
    with col4:
        st.metric("Categories Shown", filtered_items['category'].nunique())

# ── Tab 2: Order History ─────────────────────────────────────────────────────
with tab2:
    transactions = get_all_transactions()
    transactions['date'] = pd.to_datetime(transactions['date'])

    col1, col2, col3 = st.columns(3)
    with col1:
        start_date = st.date_input(
            "From",
            value=transactions['date'].min(),
            min_value=transactions['date'].min(),
            max_value=transactions['date'].max(),
            key="start_d"
        )
    with col2:
        end_date = st.date_input(
            "To",
            value=transactions['date'].max(),
            min_value=transactions['date'].min(),
            max_value=transactions['date'].max(),
            key="end_d"
        )
    with col3:
        ctype_opts = ["All"] + sorted(transactions['customer_type'].dropna().unique().tolist())
        ctype = st.selectbox("Customer Type", options=ctype_opts, key="ctype")

    mask = (
        (transactions['date'] >= pd.Timestamp(start_date)) &
        (transactions['date'] <= pd.Timestamp(end_date))
    )
    filtered_trans = transactions[mask]
    if ctype != "All":
        filtered_trans = filtered_trans[filtered_trans['customer_type'] == ctype]

    display_t = filtered_trans[['transaction_id', 'date', 'time', 'total_amount',
                                 'season', 'day_of_week', 'customer_type']].head(200).copy()
    display_t.columns = ['Order ID', 'Date', 'Time', 'Amount (Rs.)', 'Season', 'Day', 'Customer Type']
    st.dataframe(display_t, use_container_width=True, hide_index=True)
    st.caption(f"Showing 200 of {len(filtered_trans):,} orders in selected range")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Orders", f"{len(filtered_trans):,}")
    with col2:
        st.metric("Revenue", f"Rs. {filtered_trans['total_amount'].sum():,.0f}")
    with col3:
        st.metric("Avg Order Value", f"Rs. {filtered_trans['total_amount'].mean():.0f}")
    with col4:
        st.metric("Peak Order", f"Rs. {filtered_trans['total_amount'].max():.0f}")

# ── Tab 3: Item Performance ──────────────────────────────────────────────────
with tab3:
    item_sales = get_item_sales()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<p style='font-weight:600;color:{text_color}'>Revenue by Category</p>", unsafe_allow_html=True)
        cat_stats = item_sales.groupby('category').agg(
            total_qty=('total_quantity', 'sum'),
            total_rev=('total_revenue', 'sum')
        ).reset_index().sort_values('total_rev', ascending=False)

        fig = px.bar(
            cat_stats, x='category', y='total_rev',
            color='category', color_discrete_sequence=CHART_COLORS,
            labels={'total_rev': 'Revenue (Rs.)', 'category': ''}
        )
        fig.update_layout(**chart_layout(dark_mode, height=340))
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown(f"<p style='font-weight:600;color:{text_color}'>Price vs Sales Volume</p>", unsafe_allow_html=True)
        fig = px.scatter(
            item_sales, x='price', y='total_quantity',
            color='category', size='total_revenue',
            hover_data=['item_name'],
            color_discrete_sequence=CHART_COLORS,
            labels={'price': 'Price (Rs.)', 'total_quantity': 'Units Sold'}
        )
        fig.update_layout(**chart_layout(dark_mode, height=340))
        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<p style='font-weight:600;color:{text_color}'>Top 10 Items by Revenue</p>", unsafe_allow_html=True)
        top10 = item_sales.nlargest(10, 'total_revenue')[['item_name', 'category', 'total_quantity', 'total_revenue']]
        top10.columns = ['Item', 'Category', 'Qty Sold', 'Revenue (Rs.)']
        st.dataframe(top10, use_container_width=True, hide_index=True)

    with col2:
        st.markdown(f"<p style='font-weight:600;color:{text_color}'>Least Performing Items</p>", unsafe_allow_html=True)
        bot10 = item_sales.nsmallest(10, 'total_revenue')[['item_name', 'category', 'total_quantity', 'total_revenue']]
        bot10.columns = ['Item', 'Category', 'Qty Sold', 'Revenue (Rs.)']
        st.dataframe(bot10, use_container_width=True, hide_index=True)

# ── Tab 4: Dataset Summary ───────────────────────────────────────────────────
with tab4:
    menu_items    = get_all_menu_items()
    transactions  = get_all_transactions()
    trans_items   = get_transaction_items()

    transactions['date'] = pd.to_datetime(transactions['date'])
    days_covered = (transactions['date'].max() - transactions['date'].min()).days

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<p style='font-weight:600;color:{text_color}'>Record Counts</p>", unsafe_allow_html=True)
        summary_df = pd.DataFrame({
            'Table': ['Menu Items', 'Orders', 'Order Line Items', 'Unique Customers'],
            'Count': [
                len(menu_items),
                len(transactions),
                len(trans_items),
                transactions['customer_id'].nunique()
            ]
        })
        st.dataframe(summary_df, use_container_width=True, hide_index=True)

    with col2:
        st.markdown(f"<p style='font-weight:600;color:{text_color}'>Data Completeness</p>", unsafe_allow_html=True)
        quality_df = pd.DataFrame({
            'Table': ['Menu Items', 'Orders', 'Order Items'],
            'Missing Values': [
                menu_items.isnull().sum().sum(),
                transactions.isnull().sum().sum(),
                trans_items.isnull().sum().sum()
            ],
            'Status': [
                '✓ Clean' if menu_items.isnull().sum().sum() == 0 else 'Has Missing',
                '✓ Clean' if transactions.isnull().sum().sum() == 0 else 'Has Missing',
                '✓ Clean' if trans_items.isnull().sum().sum() == 0 else 'Has Missing',
            ]
        })
        st.dataframe(quality_df, use_container_width=True, hide_index=True)

    st.markdown(f"<p style='font-weight:600;color:{text_color};margin-top:12px;'>Date Coverage</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Start Date", transactions['date'].min().strftime('%d %b %Y'))
    with col2:
        st.metric("End Date", transactions['date'].max().strftime('%d %b %Y'))
    with col3:
        st.metric("Days Covered", f"{days_covered} days")

render_footer()
