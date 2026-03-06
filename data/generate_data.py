"""
Synthetic data generator for the Menu Planning system.
Uses the authentic restaurant menu with realistic sales patterns.
Monthly revenue target: 230,000 - 250,000 INR
"""

import random
from datetime import datetime, timedelta
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_connection import (
    initialize_database, execute_many, execute_write,
    clear_all_data, get_connection
)
from config import DATA_CONFIG, CATEGORIES, CUSTOMER_TYPES, PREFERENCES, SEASONS

# ============================================================
# AUTHENTIC MENU ITEMS
# Format: (Name, Category, Price, Cost, is_popular)
# is_popular = 1 means marked with * in the original menu
# Cost is estimated at ~35-40% of price for a restaurant
# ============================================================
MENU_ITEMS = {
    "Snacks": [
        ("Tea", 40, 12, 1, 1),
        ("Nescafe", 55, 16, 1, 1),
        ("Hot Milk", 40, 12, 1, 1),
        ("Coffee", 55, 16, 1, 1),
        ("Upma", 70, 25, 1, 1),
        ("Poha", 70, 25, 1, 1),
        ("Potato Vada", 65, 22, 1, 1),
        ("Missal Pav", 110, 40, 1, 1),
        ("Usal Pav", 90, 32, 1, 1),
        ("Sabudana Wada", 110, 38, 1, 1),
        ("Sabudana Khichdi", 100, 35, 1, 1),
        ("Chole Puri", 170, 60, 1, 0),
        ("Puri Bhaji", 170, 60, 1, 0),
    ],
    "Pav Bhaji & Pulav": [
        ("Pav Bhaji", 130, 45, 1, 1),          # *
        ("Amul Pav Bhaji", 150, 52, 1, 0),
        ("Khada Pav Bhaji", 140, 48, 1, 0),
        ("Masala Pav", 160, 56, 1, 0),
        ("Paneer Pav Bhaji", 180, 63, 1, 0),
        ("Tawa Pulav", 240, 84, 1, 0),
        ("Mumbaiya Special Pav Bhaji", 220, 77, 1, 0),
    ],
    "South Indian": [
        ("Idli Sambar", 65, 22, 1, 1),          # *
        ("Medu Wada", 80, 28, 1, 1),             # *
        ("Dosa Sada", 90, 32, 1, 0),
        ("Dosa Masala", 100, 35, 1, 0),
        ("Uttapam Onion", 110, 38, 1, 0),
        ("Uttapam Mix", 130, 45, 1, 0),
        ("Dosa Rava Masala", 140, 49, 1, 0),
        ("Dosa Mysore Masala", 160, 56, 1, 0),
        ("Dosa Spring Masala", 170, 60, 1, 0),
    ],
    "Chaat": [
        ("Pani Puri", 45, 15, 1, 0),
        ("Shevpuri", 50, 17, 1, 0),
        ("Bhelpuri", 50, 17, 1, 0),
        ("Dahipuri", 80, 28, 1, 0),
        ("Ragda Patties", 85, 30, 1, 0),
        ("Aloo Chaat", 100, 35, 1, 0),
    ],
    "Sandwich": [
        ("Veg Sandwich", 70, 25, 1, 0),
        ("Veg Toast Sandwich", 85, 30, 1, 0),
        ("Masala Toast Sandwich", 95, 33, 1, 0),
        ("Veg Grill Sandwich", 150, 53, 1, 1),  # *
        ("Veg Cheese Sandwich", 160, 56, 1, 0),
        ("Paneer Tikka Sandwich", 190, 66, 1, 0),
        ("Corn Cheese Sandwich", 170, 60, 1, 0),
    ],
    "Pizza": [
        ("Margherita Pizza", 220, 77, 1, 1),    # *
        ("Veggie Overload Pizza", 280, 98, 1, 0),
        ("Corn Cheese Pizza", 260, 91, 1, 0),
        ("Cheesy Garlic Bread", 180, 63, 1, 0),
        ("Garlic Bread", 140, 49, 1, 0),
        ("Classic Thin Crust Pizza", 290, 102, 1, 1),  # *
        ("Farmhouse Pizza", 300, 105, 1, 0),
        ("Three Pepper Pizza", 310, 109, 1, 0),
        ("Mexi Cheese Pasta Pizza", 320, 112, 1, 0),
    ],
    "Quick Bites": [
        ("Classic French Fries", 150, 53, 1, 1),  # *
        ("Masala French Fries", 160, 56, 1, 0),
        ("Peri Peri French Fries", 170, 60, 1, 0),
        ("Cheesy French Fries", 180, 63, 1, 0),
        ("Classic Baked Nachos", 220, 77, 1, 0),
        ("Mexican Baked Nachos", 250, 88, 1, 0),
        ("Potato Nuggets", 240, 84, 1, 0),
        ("Jalapeno Poppers", 260, 91, 1, 0),
    ],
    "Pasta": [
        ("Arrabbiata Pasta", 280, 98, 1, 1),    # *
        ("Pesto Pasta", 280, 98, 1, 0),
        ("Pinky Pinky Pasta", 300, 105, 1, 0),
    ],
    "Starter": [
        ("Veg Manchurian Dry", 240, 84, 1, 1),  # *
        ("Veg Lollypop", 250, 88, 1, 0),
        ("Veg 65", 230, 81, 1, 0),
        ("Paneer Chilly", 280, 98, 1, 0),
        ("Honey Chilly Potato", 270, 95, 1, 0),
        ("Mushroom Chilly", 280, 98, 1, 0),
        ("Paneer Dragon", 300, 105, 1, 0),
        ("Paneer Satay", 320, 112, 1, 0),
        ("Paneer Hariyali Roast", 340, 119, 1, 1),  # *
        ("Spicy Sambal Paneer", 360, 126, 1, 1),    # *
    ],
    "Indian Starter": [
        ("Golden Coin", 320, 112, 1, 1),         # *
        ("Veg Pakoda", 160, 56, 1, 0),
        ("Paneer Pakoda", 240, 84, 1, 0),
        ("Hara Bhara Kebab", 260, 91, 1, 0),
        ("Galouti Kebab", 340, 119, 1, 0),
        ("Paneer Tikka", 260, 91, 1, 1),          # *
    ],
    "Platter & Sizzler": [
        ("Indian Platter", 630, 220, 1, 1),      # *
        ("Eastern/Mushroom Platter", 630, 220, 1, 1), # *
        ("Mix Grill Platter", 950, 333, 1, 0),
        ("Vegetable Chinese Sizzler", 500, 175, 1, 1),  # *
        ("Schezwan Paneer Chilli Sizzler", 550, 193, 1, 0),
    ],
    "Main Course": [
        ("Aloo Gobi", 200, 70, 1, 1),            # *
        ("Bhindi Masala", 210, 74, 1, 0),
        ("Chana Masala", 230, 81, 1, 0),
        ("Veg Kolhapuri", 230, 81, 1, 1),        # *
        ("Mix Veg", 240, 84, 1, 0),
        ("Veg Kadai", 250, 88, 1, 0),
        ("Paneer Butter Masala", 260, 91, 1, 0),
        ("Paneer Tikka Masala", 280, 98, 1, 0),
        ("Paneer Makhani", 280, 98, 1, 0),
        ("Dal Makhani", 230, 81, 1, 0),
        ("Paneer Bhurji", 320, 112, 1, 0),
        ("Veg Dilruba", 340, 119, 1, 1),          # *
        ("Veg Biryani", 250, 88, 1, 0),
        ("Hyderabadi Biryani", 260, 91, 1, 0),
    ],
    "Breads": [
        ("Soft Rumali", 90, 32, 1, 1),            # *
        ("Chapati", 25, 8, 1, 0),
        ("Roti", 30, 10, 1, 0),
        ("Naan", 55, 19, 1, 0),
        ("Butter Naan", 65, 23, 1, 0),
        ("Garlic Naan", 75, 26, 1, 0),
        ("Cheese Naan", 90, 32, 1, 0),
        ("Laccha Paratha", 80, 28, 1, 0),
    ],
    "Rice & Dal": [
        ("Steam Rice", 140, 49, 1, 1),            # *
        ("Jeera Rice", 170, 60, 1, 0),
        ("Dal Khichdi Tadka", 230, 81, 1, 1),     # *
        ("Veg Pulao", 240, 84, 1, 0),
        ("Dal Fry", 150, 53, 1, 1),               # *
        ("Dal Tadka", 170, 60, 1, 0),
        ("Dahi Kadhi", 160, 56, 1, 0),
    ],
    "Chinese": [
        ("Veg Fried Rice", 220, 77, 1, 1),        # *
        ("Hakka Noodle", 220, 77, 1, 1),           # *
        ("Burnt Garlic Fried Rice", 260, 91, 1, 0),
        ("Veg Singapore Rice", 250, 88, 1, 0),
        ("Lemon Fried Rice", 230, 81, 1, 0),
        ("Triple Schezwan Rice", 300, 105, 1, 1),  # *
        ("Veg Manchurian Rice", 300, 105, 1, 1),   # *
        ("Korean Rice", 420, 147, 1, 1),           # *
    ],
    "Thai Cuisine": [
        ("Thai Basil Chilly Dry", 300, 105, 1, 1),  # *
        ("Thai Chilly", 300, 105, 1, 0),
        ("Thai Curry", 380, 133, 1, 0),
        ("Thai Fried Rice", 320, 112, 1, 0),
    ],
    "Soups": [
        ("Veg Manchow Soup", 160, 56, 1, 1),      # *
        ("Cream of Tomato", 160, 56, 1, 0),
        ("Sweet Corn Soup", 180, 63, 1, 0),
        ("Hot & Sour Soup", 180, 63, 1, 0),
        ("Tom Yum Soup", 210, 74, 1, 0),
        ("Lemon Coriander Soup", 190, 67, 1, 0),
    ],
    "Dessert": [
        ("Gulab Jamun", 70, 25, 1, 1),             # *
        ("Chocolate Brownie", 110, 38, 1, 0),
        ("Sizzling Brownie with Icecream", 200, 70, 1, 0),
        ("Choco Lava Cake", 120, 42, 1, 0),
        ("Gadbad Icecream", 170, 60, 1, 0),
        ("Caramel Custard", 120, 42, 1, 0),
    ],
    "Mocktails": [
        ("Virgin Mojito", 210, 74, 1, 1),          # *
        ("Blue Lagoon", 230, 81, 1, 0),
        ("Pina Colada", 260, 91, 1, 0),
        ("Mango Shots", 240, 84, 1, 1),            # *
        ("Green Cool", 230, 81, 1, 0),
        ("Watermelon Blossom", 230, 81, 1, 0),
    ],
    "Beverages": [
        ("Mineral Water", 25, 8, 1, 1),            # *
        ("Butter Milk", 70, 25, 1, 0),
        ("Sweet Lassi", 80, 28, 1, 0),
        ("Cold Drink", 50, 18, 1, 0),
        ("Fresh Lime Soda", 90, 32, 1, 0),
    ],
    "Thali": [
        ("Deluxe Thali", 299, 105, 1, 1),          # *
        ("Special Thali", 349, 122, 1, 1),          # *
        ("Gujarati Thali", 409, 143, 1, 0),
    ],
    "Salad": [
        ("Green Salad", 120, 42, 1, 1),             # *
        ("Kachumber Salad", 120, 42, 1, 0),
        ("Caesar Salad", 260, 91, 1, 0),
    ],
    "Bao": [
        ("Paneer Chilly Bao", 260, 91, 1, 1),      # *
        ("Paneer Satay Bao", 280, 98, 1, 0),
        ("Mushroom Kung Pao Bao", 300, 105, 1, 0),
    ],
}

# Popular combos for realistic ordering patterns
POPULAR_COMBOS = [
    ["Pav Bhaji", "Butter Milk"],
    ["Idli Sambar", "Tea"],
    ["Idli Sambar", "Medu Wada"],
    ["Veg Manchurian Dry", "Veg Fried Rice"],
    ["Veg Manchurian Dry", "Hakka Noodle"],
    ["Paneer Tikka", "Garlic Naan", "Dal Fry"],
    ["Paneer Butter Masala", "Butter Naan", "Steam Rice"],
    ["Triple Schezwan Rice", "Veg Manchow Soup"],
    ["Margherita Pizza", "Classic French Fries"],
    ["Dal Fry", "Steam Rice", "Roti"],
    ["Deluxe Thali", "Sweet Lassi"],
    ["Special Thali", "Butter Milk"],
    ["Indian Platter", "Garlic Naan"],
    ["Vegetable Chinese Sizzler", "Veg Manchow Soup"],
    ["Arrabbiata Pasta", "Garlic Bread"],
    ["Classic Thin Crust Pizza", "Virgin Mojito"],
    ["Korean Rice", "Veg Manchow Soup"],
    ["Thai Basil Chilly Dry", "Thai Fried Rice"],
    ["Gulab Jamun", "Mineral Water"],
    ["Missal Pav", "Tea"],
]


def get_season(date):
    month = date.month
    if month in [3, 4, 5]:
        return "Summer"
    elif month in [6, 7, 8, 9]:
        return "Monsoon"
    elif month in [10, 11]:
        return "Autumn"
    return "Winter"


def get_day_of_week(date):
    return date.strftime("%A")


def generate_menu_items():
    """Insert authentic menu items into database."""
    all_items = []
    for category, item_list in MENU_ITEMS.items():
        for row in item_list:
            name, price, cost, is_veg, is_popular = row
            all_items.append((name, category, price, cost, is_veg))

    query = """
    INSERT INTO menu_items (item_name, category, price, cost, is_veg)
    VALUES (%s, %s, %s, %s, %s)
    """
    execute_many(query, all_items)
    print(f"Generated {len(all_items)} menu items across {len(MENU_ITEMS)} categories")
    return len(all_items)


def generate_customers():
    """Generate customer records."""
    num_customers = DATA_CONFIG["num_customers"]
    customers = []

    for _ in range(num_customers):
        customer_type = random.choices(
            CUSTOMER_TYPES,
            weights=[50, 30, 20]
        )[0]
        preference = random.choices(
            PREFERENCES,
            weights=[35, 25, 40]
        )[0]
        customers.append((customer_type, preference))

    query = "INSERT INTO customers (customer_type, preference) VALUES (%s, %s)"
    execute_many(query, customers)
    print(f"Generated {num_customers} customers")
    return num_customers


def generate_transactions():
    """
    Generate transactions targeting 230,000–250,000 INR monthly revenue.
    Over 12 months: target = 230k-250k/month * 12 = 2.76M–3M total.
    With 10,000 transactions, avg order value needs to be ~276–300 INR.
    We achieve this by: items avg price ~220 INR + 1-2 items per order avg ~280-300.
    """
    num_transactions = DATA_CONFIG["num_transactions"]
    num_months = DATA_CONFIG["date_range_months"]

    # Build flat lookup from DB
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT item_id, item_name, category, price, is_veg FROM menu_items"
        )
        menu_items_db = cursor.fetchall()
        cursor.execute("SELECT customer_id, preference FROM customers")
        customers = cursor.fetchall()

    # Build popularity-weighted item pool
    popular_names = set()
    for item_list in MENU_ITEMS.values():
        for row in item_list:
            if row[4] == 1:  # is_popular
                popular_names.add(row[0])

    item_by_name = {item['item_name']: item for item in menu_items_db}
    all_items = list(menu_items_db)

    # Build weight list: popular items get 5x weight
    veg_items = [i for i in all_items if i['is_veg'] == 1]
    if not veg_items:
        veg_items = all_items  # fallback: all items treated as veg

    veg_weights = [
        2.5 if i['item_name'] in popular_names else 1.0
        for i in veg_items
    ]

    # Default pool (all items since menu is 100% veg)
    all_weights = [
        2.5 if i['item_name'] in popular_names else 1.0
        for i in all_items
    ]

    # Date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=num_months * 30)

    transactions = []
    transaction_items_list = []

    for i in range(num_transactions):
        random_days = random.randint(0, (end_date - start_date).days)
        trans_date = start_date + timedelta(days=random_days)

        # Restaurant hours 10:30 - 22:30; peak at 12-14 and 19-21
        hour_choices = list(range(10, 23))
        hour_weights = [1, 2, 5, 6, 5, 3, 2, 2, 3, 5, 6, 4, 1]  # peak lunch/dinner
        hour = random.choices(hour_choices, weights=hour_weights)[0]
        minute = random.randint(0, 59)
        trans_time = f"{hour:02d}:{minute:02d}:00"

        customer = random.choice(customers)
        customer_id = customer['customer_id']
        preference = customer['preference']

        # Item pool (all items in this menu are vegetarian)
        pool = veg_items
        pool_weights = veg_weights
        if not pool or not pool_weights:
            pool = all_items
            pool_weights = all_weights

        selected_items = []

        # 15% chance of using a popular combo (capped at 2 items to avoid inflating revenue)
        if random.random() < 0.15:
            combo = random.choice(POPULAR_COMBOS)
            for item_name in combo:
                if item_name in item_by_name and len(selected_items) < 2:
                    selected_items.append(item_by_name[item_name])

        # Fill to 1–3 items total (keeps avg order 250-320 INR)
        # Heavily favor single-item orders (avg ~1.3 items → ~240-250 Rs avg order)
        target_items = random.choices([1, 2, 3], weights=[75, 22, 3])[0]
        attempts = 0
        while len(selected_items) < target_items and attempts < 20:
            item = random.choices(pool, weights=pool_weights)[0]
            if item not in selected_items:
                selected_items.append(item)
            attempts += 1

        if not selected_items:
            selected_items = [random.choice(pool)]

        total_amount = sum(item['price'] for item in selected_items)

        season = get_season(trans_date)
        day_of_week = get_day_of_week(trans_date)

        transactions.append((
            trans_date.strftime("%Y-%m-%d"),
            trans_time,
            customer_id,
            total_amount,
            season,
            day_of_week
        ))

        # Transaction items
        trans_id = i + 1
        for item in selected_items:
            quantity = random.choices([1, 2], weights=[90, 10])[0]
            subtotal = item['price'] * quantity
            transaction_items_list.append(
                (trans_id, item['item_id'], quantity, subtotal)
            )

    # Insert transactions
    trans_query = """
    INSERT INTO transactions (date, time, customer_id, total_amount, season, day_of_week)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    execute_many(trans_query, transactions)

    items_query = """
    INSERT INTO transaction_items (transaction_id, item_id, quantity, subtotal)
    VALUES (%s, %s, %s, %s)
    """
    execute_many(items_query, transaction_items_list)

    # Report stats
    total_revenue = sum(t[3] for t in transactions)
    monthly_avg = total_revenue / num_months
    print(f"Generated {num_transactions} transactions with {len(transaction_items_list)} items")
    print(f"  Total Revenue (12 mo): Rs. {total_revenue:,.0f}")
    print(f"  Avg Monthly Revenue:   Rs. {monthly_avg:,.0f}  (Target: 230k–250k)")
    print(f"  Avg Order Value:       Rs. {total_revenue/num_transactions:,.1f}")
    return num_transactions, len(transaction_items_list)


def generate_all_data():
    """Generate all synthetic data."""
    print("=" * 50)
    print("Starting Data Generation")
    print("=" * 50)

    initialize_database()

    print("\nClearing existing data...")
    clear_all_data()

    print("\nGenerating menu items...")
    generate_menu_items()

    print("\nGenerating customers...")
    generate_customers()

    print("\nGenerating transactions...")
    generate_transactions()

    print("\n" + "=" * 50)
    print("Data Generation Complete!")
    print("=" * 50)


if __name__ == "__main__":
    generate_all_data()
