# 🎓 Project Viva Questions & Answers

## 1. Project Overview

**Q: What is the main objective of your project?**
**A:** The main objective is to provide a data-driven menu planning solution for restaurants using Data Mining techniques. It helps in identifying profitable items, understanding customer behavior, and predicting future demand to optimize inventory and increase revenue.

**Q: Which technologies did you use?**
**A:** I used **Python** for the backend logic, **Streamlit** for the frontend dashboard, **PostgreSQL (NeonDB)** for the database, and **Docker** for containerization. Key libraries include **Pandas** for data manipulation, **Scikit-learn** for machine learning, and **Plotly** for visualization.

## 2. Technical Concepts

**Q: Why did you choose PostgreSQL over SQLite?**
**A:** PostgreSQL is a more robust, scalable, and production-ready relational database management system (RDBMS) compared to SQLite, which is file-based and limited in concurrency. PostgreSQL supports advanced features like connection pooling and is better suited for a multi-user web application.

**Q: Explain the database schema.**
**A:** The schema consists of four main tables:
1.  `menu_items`: Details of food items.
2.  `customers`: Customer profiles and preferences.
3.  `transactions`: Header information for each sale.
4.  `transaction_items`: Line items for each transaction (normalizing the many-to-many relationship).

**Q: What is the difference between Apriori and FP-Growth?**
**A:** Both are Association Rule Mining algorithms. **Apriori** uses a "generate-and-test" approach, scanning the database multiple times to find frequent itemsets, which can be slow. **FP-Growth (Frequent Pattern Growth)** builds a compact tree structure (FP-Tree) and scans the database only twice, making it much faster and more memory-efficient for large datasets.

**Q: How does K-Means clustering work?**
**A:** K-Means partitions data into *K* clusters. It starts by randomly selecting *K* centroids. Then, it assigns each data point to the nearest centroid and recalculates the centroids based on the mean of the points in that cluster. This process repeats until the centroids stabilize.

**Q: How do you evaluate the performance of your demand prediction model?**
**A:** We use metrics like **Mean Absolute Error (MAE)** and **Root Mean Squared Error (RMSE)** to measure the difference between the predicted sales values and the actual historical sales values.

## 3. Implementation Details

**Q: How did you handle missing data?**
**A:** In the preprocessing stage, we check for null values. For numerical sales data, we might fill missing values with 0 or the mean. For categorical data, we might use a placeholder like "Unknown". We also ensure robust type conversion when reading from the database to prevent errors.

**Q: What is the benefit of Dockerizing the application?**
**A:** Docker ensures consistency across different environments (dev, test, prod). It packages the application with all its dependencies (Python libraries, OS settings) into a single container, eliminating "it works on my machine" issues.

**Q: How does the "Menu Engineering Matrix" help the restaurant owner?**
**A:** It categorizes items into four quadrants:
*   **Stars**: High Profit, High Popularity -> Keep them standards.
*   **Plowhorses**: Low Profit, High Popularity -> Increase price or reduce portion.
*   **Puzzles**: High Profit, Low Popularity -> Market them more.
*   **Dogs**: Low Profit, Low Popularity -> Remove from menu.
