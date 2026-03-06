import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_connection import get_item_sales, get_all_menu_items
from modules.preprocessing import categorize_menu_items, calculate_profit_margin
from modules.classification import classify_item_popularity, get_category_performance

from utils.ui import (
    setup_page_config, setup_sidebar, apply_custom_css,
    get_chart_colors, chart_layout, render_section_title, render_footer
)

setup_page_config(page_title="Menu Optimization")

dark_mode = setup_sidebar()
colors = apply_custom_css(dark_mode)
CHART_COLORS = get_chart_colors()

render_section_title("Menu Optimization")
st.markdown(f"<p style='color:{colors['text_muted']};margin-top:-10px;margin-bottom:8px;'>Data-driven recommendations to improve menu profitability.</p>", unsafe_allow_html=True)


@st.cache_data
def load_menu_data():
    item_sales = get_item_sales()
    item_sales = calculate_profit_margin(item_sales)
    item_sales = categorize_menu_items(item_sales)
    return item_sales

item_sales = load_menu_data()

tab1, tab2, tab3, tab4 = st.tabs(["Menu Engineering", "Profitability", "Recommendations", "Action Plan"])

with tab1:
    st.subheader("Menu Engineering Matrix")
    
    st.markdown("""
    The Menu Engineering Matrix classifies items based on **Popularity** and **Profitability**:
    - **Stars**: High popularity, high profitability - Keep and promote
    - **Puzzles**: Low popularity, high profitability - Increase visibility
    - **Plowhorses**: High popularity, low profitability - Optimize cost/price
    - **Dogs**: Low popularity, low profitability - Consider removal
    """)
    
    category_counts = item_sales['menu_category'].value_counts().reset_index()
    category_counts.columns = ['Category', 'Count']
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Color mapping
        cat_colors = {'Star': '#2ECC71', 'Puzzle': '#3498DB', 'Plowhorse': '#F39C12', 'Dog': '#E74C3C'}
        
        for cat in ['Star', 'Puzzle', 'Plowhorse', 'Dog']:
            count = category_counts[category_counts['Category'] == cat]['Count'].values
            count = count[0] if len(count) > 0 else 0
            st.markdown(
                f"<div style='background-color: {cat_colors[cat]}; padding: 10px; border-radius: 5px; margin: 5px 0; color: white;'>"
                f"<strong>{cat}</strong>: {count} items</div>",
                unsafe_allow_html=True
            )
    
    with col2:
        fig = px.pie(
            category_counts,
            values='Count',
            names='Category',
            color='Category',
            color_discrete_map=cat_colors,
            title='Menu Item Distribution',
            hole=0.4
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=colors['text_color'])
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Scatter plot
    st.markdown("---")
    st.markdown("#### Menu Engineering Quadrant Chart")
    
    median_qty = item_sales['total_quantity'].median()
    median_profit = item_sales['total_profit'].median()
    
    fig = px.scatter(
        item_sales,
        x='total_quantity',
        y='total_profit',
        color='menu_category',
        color_discrete_map=cat_colors,
        hover_data=['item_name', 'category', 'price'],
        title='',
        labels={'total_quantity': 'Popularity (Quantity Sold)', 'total_profit': 'Total Profit (Rs.)'}
    )
    
    # Add quadrant lines
    fig.add_hline(y=median_profit, line_dash="dash", line_color="gray", opacity=0.5)
    fig.add_vline(x=median_qty, line_dash="dash", line_color="gray", opacity=0.5)
    
    fig.update_layout(
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=colors['text_color'])
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed table
    with st.expander("View All Items with Categories"):
        display_df = item_sales[['item_name', 'category', 'price', 'total_quantity', 
                                  'total_revenue', 'total_profit', 'profit_margin', 'menu_category']]
        st.dataframe(display_df.sort_values('menu_category'), use_container_width=True, hide_index=True)

with tab2:
    st.subheader("Profitability Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Top 10 Most Profitable Items")
        top_profit = item_sales.nlargest(10, 'total_profit')
        
        fig = px.bar(
            top_profit,
            x='total_profit',
            y='item_name',
            orientation='h',
            color='profit_margin',
            color_continuous_scale='Greens',
            title=''
        )
        fig.update_layout(
            yaxis={'categoryorder':'total ascending'},
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=colors['text_color'])
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Lowest Profit Margin Items")
        low_margin = item_sales.nsmallest(10, 'profit_margin')
        
        fig = px.bar(
            low_margin,
            x='profit_margin',
            y='item_name',
            orientation='h',
            color='profit_margin',
            color_continuous_scale='Reds_r',
            title=''
        )
        fig.update_layout(
            yaxis={'categoryorder':'total descending'},
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=colors['text_color'])
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Category profitability
    st.markdown("---")
    st.markdown("#### Profitability by Category")
    
    category_profit = item_sales.groupby('category').agg({
        'total_revenue': 'sum',
        'total_profit': 'sum',
        'total_quantity': 'sum'
    }).reset_index()
    
    # Safe division
    category_profit['profit_margin'] = category_profit.apply(
        lambda row: (row['total_profit'] / row['total_revenue'] * 100) if row['total_revenue'] > 0 else 0,
        axis=1
    ).round(2)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            category_profit,
            x='category',
            y='total_profit',
            color='category',
            title='Total Profit by Category',
            color_discrete_sequence=CHART_COLORS
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=colors['text_color'])
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(
            category_profit,
            x='category',
            y='profit_margin',
            color='category',
            title='Profit Margin by Category (%)',
            color_discrete_sequence=CHART_COLORS
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=colors['text_color'])
        )
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("AI-Powered Recommendations")
    
    # Stars - Promote
    st.markdown("### Stars - Maintain and Promote")
    stars = item_sales[item_sales['menu_category'] == 'Star']
    if len(stars) > 0:
        st.success(f"{len(stars)} items are performing excellently!")
        st.dataframe(
            stars[['item_name', 'category', 'total_quantity', 'total_profit']].head(5),
            use_container_width=True, hide_index=True
        )
        st.info("**Action**: Feature prominently, maintain quality, consider slight price increase")
    
    st.markdown("---")
    
    # Puzzles - Increase Visibility
    st.markdown("### Puzzles - Increase Visibility")
    puzzles = item_sales[item_sales['menu_category'] == 'Puzzle']
    if len(puzzles) > 0:
        st.warning(f"{len(puzzles)} items have potential but low sales")
        st.dataframe(
            puzzles[['item_name', 'category', 'total_quantity', 'profit_margin']].head(5),
            use_container_width=True, hide_index=True
        )
        st.info("**Action**: Better menu placement, staff recommendations, promotional offers")
    
    st.markdown("---")
    
    # Plowhorses - Optimize
    st.markdown("### Plowhorses - Cost Optimization Needed")
    plowhorses = item_sales[item_sales['menu_category'] == 'Plowhorse']
    if len(plowhorses) > 0:
        st.warning(f"{len(plowhorses)} popular items with low profit margins")
        st.dataframe(
            plowhorses[['item_name', 'category', 'total_quantity', 'profit_margin', 'price']].head(5),
            use_container_width=True, hide_index=True
        )
        st.info("**Action**: Reduce portion size, increase price, optimize ingredient costs")
    
    st.markdown("---")
    
    # Dogs - Consider Removal
    st.markdown("### Dogs - Consider Removal")
    dogs = item_sales[item_sales['menu_category'] == 'Dog']
    if len(dogs) > 0:
        st.error(f"{len(dogs)} items underperforming in both sales and profit")
        st.dataframe(
            dogs[['item_name', 'category', 'total_quantity', 'total_profit']].head(5),
            use_container_width=True, hide_index=True
        )
        st.info("**Action**: Remove from menu, replace with new items, or completely redesign")

with tab4:
    st.subheader("Actionable Menu Changes")
    
    # Summary metrics
    col1, col2, col3 = st.columns(3)
    
    total_revenue = item_sales['total_revenue'].sum()
    total_profit = item_sales['total_profit'].sum()
    
    with col1:
        st.metric("Current Total Revenue", f"Rs. {total_revenue:,.2f}")
    with col2:
        st.metric("Current Total Profit", f"Rs. {total_profit:,.2f}")
    with col3:
        st.metric("Overall Margin", f"{(total_profit/total_revenue*100):.1f}%")
    
    st.markdown("---")
    
    # Action items
    st.markdown("### Recommended Actions")
    
    action_items = []
    
    # Remove dogs
    dogs = item_sales[item_sales['menu_category'] == 'Dog']
    if len(dogs) > 0:
        low_performers = dogs.nsmallest(3, 'total_profit')
        for _, item in low_performers.iterrows():
            action_items.append({
                'Priority': 'High',
                'Action': 'Remove',
                'Item': item['item_name'],
                'Reason': f"Low profit (Rs. {item['total_profit']:.2f})",
                'Expected Impact': 'Reduce waste, simplify menu'
            })
    
    # Price increase for plowhorses
    plowhorses = item_sales[item_sales['menu_category'] == 'Plowhorse']
    if len(plowhorses) > 0:
        for _, item in plowhorses.head(3).iterrows():
            suggested_price = item['price'] * 1.1  # 10% increase
            action_items.append({
                'Priority': 'Medium',
                'Action': 'Price Increase',
                'Item': item['item_name'],
                'Reason': f"High volume, low margin ({item['profit_margin']:.1f}%)",
                'Expected Impact': f"New price: Rs. {suggested_price:.2f}"
            })
    
    # Promote puzzles
    puzzles = item_sales[item_sales['menu_category'] == 'Puzzle']
    if len(puzzles) > 0:
        for _, item in puzzles.head(3).iterrows():
            action_items.append({
                'Priority': 'Medium',
                'Action': 'Promote',
                'Item': item['item_name'],
                'Reason': f"High margin ({item['profit_margin']:.1f}%), low sales",
                'Expected Impact': 'Increased visibility and sales'
            })
    
    if action_items:
        action_df = pd.DataFrame(action_items)
        st.dataframe(action_df, use_container_width=True, hide_index=True)
    
    # Estimated impact
    st.markdown("---")
    st.markdown("### Estimated Impact of Recommendations")
    
    col1, col2, col3 = st.columns(3)
    
    # Conservative estimates
    dog_savings = dogs['total_profit'].sum() * 0.5 if len(dogs) > 0 else 0
    plowhorse_increase = plowhorses['total_profit'].sum() * 0.1 if len(plowhorses) > 0 else 0
    puzzle_increase = puzzles['total_profit'].sum() * 0.2 if len(puzzles) > 0 else 0
    
    with col1:
        st.metric("Cost Savings (Dogs)", f"Rs. {abs(dog_savings):,.2f}")
    with col2:
        st.metric("Profit Increase (Plowhorses)", f"Rs. {plowhorse_increase:,.2f}")
    with col3:
        st.metric("Sales Increase (Puzzles)", f"Rs. {puzzle_increase:,.2f}")
    
    total_impact = dog_savings + plowhorse_increase + puzzle_increase
    st.success(f"**Total Estimated Annual Impact**: Rs. {total_impact:,.2f}")
