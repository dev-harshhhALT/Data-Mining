"""
Configuration settings for the Data Mining Menu Planning application.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database configuration
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Data generation settings
DATA_CONFIG = {
    "num_menu_items": 50,
    "num_customers": 2374,
    "num_transactions": 21476,
    "avg_items_per_transaction": 3,
    "date_range_months": 12
}

# Analysis parameters
ANALYSIS_CONFIG = {
    "min_support": 0.02,
    "min_confidence": 0.3,
    "num_clusters": 4,
    "forecast_days": 30
}

# Menu categories
CATEGORIES = ["Starter", "Main Course", "Dessert", "Beverage"]

# Customer types
CUSTOMER_TYPES = ["Regular", "New", "VIP"]

# Dietary preferences
PREFERENCES = ["Vegetarian", "Non-Vegetarian", "Both"]

# Seasons
SEASONS = ["Summer", "Monsoon", "Autumn", "Winter"]
