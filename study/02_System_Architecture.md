# System Architecture

## 1. Overview

The Data Mining Menu Planning System follows a modern web application architecture, utilizing a client-server model with a relational database backend.

- **Frontend**: Streamlit (Python-based web interface).
- **Backend Logic**: Python modules for data processing and machine learning.
- **Database**: PostgreSQL (NeonDB) for structured data storage.
- **Infrastructure**: Docker for containerization and deployment.

## 2. Components

### A. Data Layer (PostgreSQL)
The system stores all transactional data in a relational database.
*   **Tables**:
    *   `menu_items`: Stores item details (ID, Name, Category, Price, Cost, Veg/Non-Veg).
    *   `customers`: Stores customer profiles (ID, Type, Preference).
    *   `transactions`: Log of all sales (ID, Date, Time, Customer ID, Total Amount).
    *   `transaction_items`: Junction table linking transactions to menu items (Transaction ID, Item ID, Quantity).

### B. Application Layer (Python Modules)
*   **`app.py`**: The main entry point for the Streamlit application.
*   **`database/db_connection.py`**: Handles database connections using `psycopg2`, executes SQL queries, and returns Pandas DataFrames.
*   **`modules/preprocessing.py`**: Cleans data, handles missing values, and prepares features for ML models.
*   **`modules/association_rules.py`**: Implements Apriori/FP-Growth algorithms to find frequent itemsets.
*   **`modules/clustering.py`**: Groups customers using K-Means clustering based on RFM scores.
*   **`modules/prediction.py`**: Uses linear regression/time series models for sales forecasting.

### C. Presentation Layer (Streamlit)
*   Provides an interactive dashboard for users.
*   Visualizes data using charts (Plotly).
*   Displays tables and actionable insights.

## 3. Data Flow

1.  **User Interaction**: The restaurant manager accesses the dashboard via a web browser.
2.  **Request**: The Streamlit app sends a request to the backend Python logic.
3.  **Data Retrieval**: Python scripts query the PostgreSQL database for relevant data (sales, customer info).
4.  **Processing**: Data is processed (cleaned, aggregated) and fed into ML models if needed.
5.  **Visualization**: Results (charts, tables, recommendations) are rendered on the frontend.

## 4. Technologies Used

*   **Language**: Python 3.9+
*   **Framework**: Streamlit
*   **Database**: PostgreSQL
*   **Libraries**: Pandas, NumPy, Scikit-learn, MLxtend, Plotly, Psycopg2
*   **Tools**: Docker, Git
