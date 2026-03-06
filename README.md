# Data Mining Menu Planning System

A comprehensive data mining and analytics solution for menu optimization in the hospitality industry. This system leverages machine learning techniques to provide actionable insights for restaurant management.

## Features

- **Data Overview**: Interactive dashboard for menu items, transactions, and sales KPIs.
- **Association Rule Mining**: Discover frequently purchased item combinations (Market Basket Analysis) using Apriori/FP-Growth.
- **Customer Segmentation**: Segment customers using RFM (Recency, Frequency, Monetary) analysis and K-Means clustering.
- **Demand Forecasting**: Predict future sales and item demand using time series analysis and regression models.
- **Menu Optimization**: Classify menu items (Star, Puzzle, Plowhorse, Dog) using the Menu Engineering Matrix and get AI-driven recommendations.

## Tech Stack

- **Frontend**: Streamlit
- **Database**: PostgreSQL (NeonDB)
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: Scikit-learn, MLxtend
- **Visualization**: Plotly Express, Plotly Graph Objects
- **Containerization**: Docker

## Installation & Setup

### Prerequisites

- Python 3.9+
- PostgreSQL Database (or NeonDB account)
- Docker (optional)

### 1. Clone the Repository

```bash
git clone https://github.com/dev-harshhhALT/Data-Mining
cd DataMining-MenuPlanning
```

### 2. Environment Setup

Create a virtual environment:

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Database Configuration

Create a `.env` file in the root directory with your PostgreSQL credentials:

```ini
DB_HOST=your-neon-db-host.neon.tech
DB_PORT=5432
DB_NAME=neondb
DB_USER=your-db-user
DB_PASSWORD=your-db-password
```

### 4. Initialize & Generate Data

Run the data generation script to initialize the database schema and populate it with synthetic data (10,000+ records):

```bash
python data/generate_data.py
```

*Note: This script will clear existing data in the configured database and generate fresh sample data.*

### 5. Run the Application

Start the Streamlit dashboard:

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Docker Support

Build and run the application using Docker:

### Build Image
```bash
docker build -t menu-planning .
```

### Run Container
```bash
docker run -p 8501:8501 --env-file .env menu-planning
```

*Ensure your `.env` file is present in the root directory before running.*

---

## Project Structure

```
DataMining-MenuPlanning/
├── app.py                  # Main Streamlit dashboard entry point
├── config.py               # Global configuration & settings
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (DB credentials)
├── Dockerfile              # Docker build instructions
├── data/
│   └── generate_data.py    # Synthetic data generation script
├── database/
│   ├── db_connection.py    # Database connection & query utilities
│   └── schema_postgres.sql # PostgreSQL database schema
├── modules/
│   ├── preprocessing.py    # Data cleaning & feature engineering
│   ├── classification.py   # Menu item classification logic
│   ├── clustering.py       # K-Means clustering algorithms
│   ├── association_rules.py # Apriori/FP-Growth implementation
│   └── prediction.py       # Demand forecasting models
├── pages/                  # Streamlit multi-page application pages
│   ├── 1_Data_Overview.py
│   ├── 2_Association_Rules.py
│   ├── 3_Customer_Segments.py
│   ├── 4_Demand_Forecast.py
│   └── 5_Menu_Optimization.py
└── utils/
    ├── helpers.py          # General helper functions
    └── ui.py               # UI components & styling
```

## Data Mining Techniques Details

### Association Rule Mining
- **Algorithm**: FP-Growth / Apriori
- **Goal**: Identify items that are frequently bought together (e.g., "Burger" and "Fries").
- **Metric**: Support, Confidence, Lift.

### Customer Segmentation
- **Method**: RFM Analysis + K-Means Clustering.
- **Segments**:
    - **Champions**: High spending, frequent, recent.
    - **loyal customers**: Regular buyers.
    - **At Risk**: Haven't purchased recently.
    - **Lost**: No recent activity, low value.

### Demand Prediction
- **Model**: Linear Regression / Random Forest (configurable).
- **Features**: Lagged sales, Moving averages (7-day, 30-day), Day of week, Seasonality.
- **Output**: 30-day revenue and item-level demand forecast.

### Menu Engineering
- **Matrix**: Evaluates items based on **Volume** (Popularity) and **Margin** (Profitability).
- **Categories**:
    - **Star**: High Volume, High Margin.
    - **Puzzle**: Low Volume, High Margin.
    - **Plowhorse**: High Volume, Low Margin.
    - **Dog**: Low Volume, Low Margin.

## License

> [!CAUTION]
> **This is a Closed Source Project.**
> All rights reserved. Unauthorized copying, distribution, modification, or use of this codebase — in whole or in part — is strictly prohibited without explicit written permission from the author.

This project is developed for academic purposes (TYBCA Sem-VI) and is **not** open for public contribution or redistribution.

---

## Developer

Built & maintained by **[dev-harshhh19](https://github.com/dev-harshhh19)**
