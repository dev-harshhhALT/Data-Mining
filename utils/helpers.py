"""
Utility helper functions for the application.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go



def format_currency(value):
    return f"Rs. {value:,.2f}"


def format_percentage(value):
    return f"{value:.1f}%"


def create_pie_chart(data, values, names, title, hole=0.4):
    fig = px.pie(
        data, 
        values=values, 
        names=names, 
        title=title,
        hole=hole
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig


def create_bar_chart(data, x, y, title, color=None, orientation='v'):
    fig = px.bar(
        data,
        x=x,
        y=y,
        title=title,
        color=color,
        orientation=orientation
    )
    fig.update_layout(showlegend=bool(color))
    return fig


def create_line_chart(data, x, y, title, markers=True):
    return px.line(
        data,
        x=x,
        y=y,
        title=title,
        markers=markers
    )


def create_scatter_plot(data, x, y, title, color=None, size=None, hover_data=None):
    return px.scatter(
        data,
        x=x,
        y=y,
        title=title,
        color=color,
        size=size,
        hover_data=hover_data
    )


def create_heatmap(data, title):
    return px.imshow(
        data,
        title=title,
        aspect='auto',
        color_continuous_scale='Blues'
    )


def get_color_by_category(category):
    return {
        'Starter': '#FF6B6B',
        'Main Course': '#4ECDC4',
        'Dessert': '#FFE66D',
        'Beverage': '#95E1D3'
    }.get(category, '#95A5A6')


def get_color_by_menu_engineering(category):
    return {
        'Star': '#2ECC71',
        'Puzzle': '#3498DB',
        'Plowhorse': '#F39C12',
        'Dog': '#E74C3C'
    }.get(category, '#95A5A6')


def calculate_growth_rate(current, previous):
    if not previous:
        return 0
    return ((current - previous) / previous) * 100


def create_metric_card_style():
    return """
    <style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        padding: 20px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    .metric-value {
        font-size: 2em;
        font-weight: bold;
    }
    .metric-label {
        font-size: 0.9em;
        opacity: 0.9;
    }
    </style>
    """
