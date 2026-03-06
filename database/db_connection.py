"""
Database connection and utility functions for SQLite database.
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import os
import pandas as pd
from contextlib import contextmanager
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT

# Get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA_PATH = os.path.join(PROJECT_ROOT, "database", "schema_postgres.sql")


@contextmanager
def get_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT,
            cursor_factory=RealDictCursor,
            sslmode='require',
            channel_binding='require'
        )
        yield conn
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        raise e
    finally:
        if 'conn' in locals() and conn:
            conn.close()


def initialize_database():
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                with open(SCHEMA_PATH, 'r') as f:
                    cursor.execute(f.read())
            conn.commit()
        print("Database schema initialized.")
    except Exception as e:
        print(f"Failed to initialize database: {e}")


def execute_query(query, params=None):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                if cursor.description is None:
                    return pd.DataFrame()
                
                columns = [desc[0] for desc in cursor.description]
                data = cursor.fetchall()
                
                if not data:
                    return pd.DataFrame(columns=columns)
                
                df = pd.DataFrame(data, columns=columns) # Ensure column names are set
                return df
    except Exception as e:
        print(f"Query execution failed: {e}")
        import traceback
        traceback.print_exc()
        return pd.DataFrame()


def execute_write(query, params=None):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
            conn.commit()
            return True
    except Exception as e:
        print(f"Write operation failed: {e}")
        return False


from psycopg2.extras import RealDictCursor, execute_batch

def execute_many(query, data):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Use execute_batch for faster performance with NeonDB
                execute_batch(cursor, query, data, page_size=100)
            conn.commit()
            return cursor.rowcount
    except Exception as e:
        print(f"Bulk write failed: {e}")
        return 0


def get_all_menu_items():
    """Retrieve all menu items."""
    df = execute_query("SELECT * FROM menu_items ORDER BY category, item_name")
    # Ensure numeric types
    for col in ['price', 'cost', 'is_veg']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df


def get_all_transactions():
    """Retrieve all transactions with details."""
    query = """
    SELECT 
        t.transaction_id,
        t.date,
        t.time,
        t.customer_id,
        t.total_amount,
        t.season,
        t.day_of_week,
        c.customer_type,
        c.preference
    FROM transactions t
    LEFT JOIN customers c ON t.customer_id = c.customer_id
    ORDER BY t.date DESC, t.time DESC
    """
    df = execute_query(query)
    # Ensure numeric types
    for col in ['total_amount']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df


def get_transaction_items():
    """Retrieve all transaction items with details."""
    query = """
    SELECT 
        ti.transaction_id,
        ti.item_id,
        ti.quantity,
        ti.subtotal,
        m.item_name,
        m.category,
        m.price,
        m.is_veg
    FROM transaction_items ti
    JOIN menu_items m ON ti.item_id = m.item_id
    """
    df = execute_query(query)
    # Ensure numeric types
    for col in ['quantity', 'subtotal', 'price']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df


def get_sales_summary():
    """Get sales summary statistics."""
    query = """
    SELECT 
        COUNT(DISTINCT transaction_id) as total_transactions,
        COALESCE(SUM(total_amount), 0) as total_revenue,
        COALESCE(AVG(total_amount), 0) as avg_transaction_value,
        COUNT(DISTINCT customer_id) as unique_customers
    FROM transactions
    """
    df = execute_query(query)
    # Ensure numeric types
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df


def get_item_sales():
    """Get sales by menu item."""
    query = """
    SELECT 
        m.item_id,
        m.item_name,
        m.category,
        m.price,
        m.cost,
        m.is_veg,
        COALESCE(SUM(ti.quantity), 0) as total_quantity,
        COALESCE(SUM(ti.subtotal), 0) as total_revenue,
        COALESCE(SUM(ti.quantity * (m.price - m.cost)), 0) as total_profit
    FROM menu_items m
    LEFT JOIN transaction_items ti ON m.item_id = ti.item_id
    GROUP BY m.item_id
    ORDER BY total_quantity DESC
    """
    df = execute_query(query)
    
    # Ensure numeric types
    for col in ['total_quantity', 'total_revenue', 'total_profit', 'price', 'cost']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    return df


def get_daily_sales():
    """Get daily sales summary."""
    query = """
    SELECT 
        date,
        COUNT(*) as num_transactions,
        SUM(total_amount) as daily_revenue
    FROM transactions
    GROUP BY date
    ORDER BY date
    """
    df = execute_query(query)
    # Ensure numeric types
    for col in ['num_transactions', 'daily_revenue']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df


def get_basket_data():
    """Get transaction-item matrix for association rule mining."""
    query = """
    SELECT 
        ti.transaction_id,
        m.item_name
    FROM transaction_items ti
    JOIN menu_items m ON ti.item_id = m.item_id
    """
    return execute_query(query)


def clear_all_data():
    """Clear all data from tables (for regeneration)."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("TRUNCATE TABLE transaction_items, transactions, customers, menu_items RESTART IDENTITY CASCADE")
        conn.commit()


if __name__ == "__main__":
    initialize_database()
    print("Database setup complete!")
