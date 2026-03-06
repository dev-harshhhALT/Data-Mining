"""
Association Rules Page - Discover item combinations.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_connection import get_transaction_items, get_basket_data
from modules.association_rules import (
    create_basket_matrix, mine_frequent_itemsets,
    generate_association_rules, get_top_associations,
    get_combo_recommendations, get_rule_statistics
)

from utils.ui import (
    setup_page_config, setup_sidebar, apply_custom_css,
    get_chart_colors, chart_layout, render_section_title, render_footer
)

setup_page_config(page_title="Association Rules")

dark_mode = setup_sidebar()
colors = apply_custom_css(dark_mode)
CHART_COLORS = get_chart_colors()

render_section_title("Association Rule Mining")
st.markdown(f"<p style='color:{colors['text_muted']};margin-top:-10px;margin-bottom:8px;'>Discover items frequently purchased together.</p>", unsafe_allow_html=True)


# Parameters
st.sidebar.header("Mining Parameters")
min_support = st.sidebar.slider(
    "Minimum Support",
    min_value=0.005,
    max_value=0.20,
    value=0.01,
    step=0.005,
    help="Minimum frequency for an itemset to be considered frequent"
)

min_confidence = st.sidebar.slider(
    "Minimum Confidence",
    min_value=0.1,
    max_value=0.9,
    value=0.2,
    step=0.05,
    help="Minimum probability of consequent given antecedent"
)

# Load and process data
@st.cache_data
def load_association_data(min_sup, min_conf):
    trans_items = get_transaction_items()
    basket = create_basket_matrix(trans_items)
    frequent_itemsets = mine_frequent_itemsets(basket, min_support=min_sup)
    
    if len(frequent_itemsets) > 0:
        rules = generate_association_rules(frequent_itemsets, min_confidence=min_conf)
    else:
        rules = pd.DataFrame()
    
    return basket, frequent_itemsets, rules

with st.spinner("Mining association rules..."):
    basket, frequent_itemsets, rules = load_association_data(min_support, min_confidence)

# Display results
if len(rules) == 0:
    st.warning("No association rules found with current parameters. Try lowering the thresholds.")
else:
    # Statistics
    stats = get_rule_statistics(rules)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Rules", stats['total_rules'])
    with col2:
        st.metric("Avg Confidence", f"{stats['avg_confidence']:.2%}")
    with col3:
        st.metric("Avg Lift", f"{stats['avg_lift']:.2f}")
    with col4:
        st.metric("High Confidence Rules", stats['rules_with_high_confidence'])
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["Top Rules", "Combo Recommendations", "Visualization"])
    
    with tab1:
        st.subheader("Top Association Rules")
        
        n_rules = st.slider("Number of rules to display", 5, 30, 15)
        top_rules = get_top_associations(rules, n=n_rules)
        
        # Format for display
        display_rules = top_rules.copy()
        display_rules['support'] = display_rules['support'].apply(lambda x: f"{x:.2%}")
        display_rules['confidence'] = display_rules['confidence'].apply(lambda x: f"{x:.2%}")
        display_rules['lift'] = display_rules['lift'].apply(lambda x: f"{x:.2f}")
        display_rules.columns = ['If Customer Orders', 'They Also Order', 'Support', 'Confidence', 'Lift']
        
        st.dataframe(display_rules, use_container_width=True, hide_index=True)
        
        # Explanation
        with st.expander("Understanding the Metrics"):
            st.markdown("""
            - **Support**: How often the combination appears in all transactions
            - **Confidence**: Probability of ordering the consequent given the antecedent was ordered
            - **Lift**: How much more likely the consequent is ordered when antecedent is present (>1 = positive association)
            """)
    
    with tab2:
        st.subheader("Combo Meal Recommendations")
        
        combos = get_combo_recommendations(rules, n=8)
        
        if combos:
            for i, combo in enumerate(combos, 1):
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**Combo {i}**: {combo['description']}")
                        st.caption(f"Items: {', '.join(combo['items'])}")
                    with col2:
                        st.metric("Confidence", f"{combo['confidence']}%")
                    st.divider()
        else:
            st.info("No strong combos found. Try adjusting parameters.")
    
    with tab3:
        st.subheader("Association Network")
        
        # Create network graph
        if len(rules) > 0:
            G = nx.DiGraph()
            
            # Add edges from top rules
            top_rules_raw = rules.head(20)
            for _, rule in top_rules_raw.iterrows():
                for ant in rule['antecedents']:
                    for cons in rule['consequents']:
                        G.add_edge(ant, cons, weight=rule['lift'])
            
            if len(G.nodes()) > 0:
                # Create positions
                pos = nx.spring_layout(G, k=2, iterations=50)
                
                # Create edge traces
                edge_x = []
                edge_y = []
                for edge in G.edges():
                    x0, y0 = pos[edge[0]]
                    x1, y1 = pos[edge[1]]
                    edge_x.extend([x0, x1, None])
                    edge_y.extend([y0, y1, None])
                
                edge_trace = go.Scatter(
                    x=edge_x, y=edge_y,
                    line=dict(width=1, color='#888'),
                    hoverinfo='none',
                    mode='lines'
                )
                
                # Create node traces
                node_x = [pos[node][0] for node in G.nodes()]
                node_y = [pos[node][1] for node in G.nodes()]
                
                node_trace = go.Scatter(
                    x=node_x, y=node_y,
                    mode='markers+text',
                    hoverinfo='text',
                    text=list(G.nodes()),
                    textposition="top center",
                    marker=dict(
                        size=20,
                        color=colors['accent_color'],
                        line_width=2
                    )
                )
                
                fig = go.Figure(data=[edge_trace, node_trace],
                               layout=go.Layout(
                                   showlegend=False,
                                   hovermode='closest',
                                   xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                   yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                   height=500,
                                   plot_bgcolor='rgba(0,0,0,0)',
                                   paper_bgcolor='rgba(0,0,0,0)',
                                   font=dict(color=colors['text_color'])
                               ))
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Not enough data to create network visualization.")
        
        # Bar chart of lift values
        st.subheader("Top Rules by Lift")
        top_10 = get_top_associations(rules, n=10)
        if len(top_10) > 0:
            top_10['rule'] = top_10['antecedents'] + ' → ' + top_10['consequents']
            fig = px.bar(
                top_10,
                x='lift',
                y='rule',
                orientation='h',
                color='confidence',
                color_continuous_scale='Viridis',
                title=''
            )
            fig.update_layout(
                yaxis={'categoryorder':'total ascending'}, 
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color=colors['text_color'])
            )
            st.plotly_chart(fig, use_container_width=True)
