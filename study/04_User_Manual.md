# User Manual

## 1. Getting Started

### Prerequisites

*   Python 3.9+
*   PostgreSQL Server (e.g., NeonDB)
*   Web Browser (Chrome, Firefox, Safari)

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/DataMining-MenuPlanning.git
    cd DataMining-MenuPlanning
    ```

2.  Create virtual environment:
    ```bash
    python -m venv .venv
    .venv\Scripts\activate
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4.  Configure Database:
    Create a `.env` file in the root folder with the following:
    ```ini
    DB_HOST=...
    DB_PORT=5432
    DB_NAME=neondb
    DB_USER=...
    DB_PASSWORD=...
    ```

5.  Generate Data:
    ```bash
    python data/generate_data.py
    ```

6.  Run the application:
    ```bash
    streamlit run app.py
    ```

## 2. Using the Dashboard

### A. Dashboard Overview
Upon login, you will see the **Dashboard Overview**.
*   **Key Metrics**: Total Transactions, Revenue, Avg Transaction Value, Unique Customers.
*   **Top 10 Selling Items**: Bar chart visualization.
*   **Revenue by Category**: Pie chart breakdown.
*   **Daily Revenue Trend**: Line chart showing sales over time with moving average.
*   **Sales by Day of Week**: Bar chart showing weekly patterns.

### B. Navigation (Sidebar)

Use the sidebar to navigate between different modules:
1.  **Data Overview**: Detailed view of raw data tables (Transactions, Items).
2.  **Association Rules**: Discover hidden patterns in customer orders.
3.  **Customer Segments**: Analyze customer groups based on RFM scores.
4.  **Demand Forecast**: View sales predictions for the next 30 days.
5.  **Menu Optimization**: Get AI-driven recommendations for menu changes.

### C. Features Explained

#### **1. Association Rules**
*   **Select Metric**: Choose between Lift, Confidence, or Support.
*   **Minimum Threshold**: Adjust the slider to filter rules.
*   **View Rules**: See table of antecedent -> consequent relationships.

#### **2. Customer Segments**
*   **Cluster Visualization**: 3D scatter plot of customer groups.
*   **Segment Analysis**: Detailed breakdown of "Champions", "Loyal", "At Risk", etc.

#### **3. Demand Forecast**
*   **Select Item**: Choose a specific menu item to see its predicted demand.
*   **Forecast Chart**: View historical vs. predicted sales.

#### **4. Menu Optimization**
*   **Matrix View**: See items plotted on Popularity vs. Profitability chart.
*   **Recommendations**:
    *   **Keep**: High profit, high volume items.
    *   **Promote**: Low volume, high profit items.
    *   **Monitor**: High volume, low profit items.
    *   **Remove**: Low volume, low profit items.

## 3. Troubleshooting

*   **App not loading**: Ensure the database server is running and reachable.
*   **"No data found"**: Run `python data/generate_data.py` to populate the database.
*   **Docker errors**: Verify Docker is installed and running.
