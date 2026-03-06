# Machine Learning Techniques Explained

## 1. Association Rule Mining (Apriori/FP-Growth)

### **What is it?**
A technique used to find interesting relationships ("rules") between variables in large databases. It's best known for finding "frequent itemsets" (items bought together).

### **How it Works (Simple Terms)**
*   **Support**: How often an itemset appears in transactions (e.g., Burger + Fries happen in 10% of orders).
*   **Confidence**: How likely item Y is purchased when item X is purchased (e.g., if someone buys a Burger, there's an 80% chance they buy Fries).
*   **Lift**: Strength of a rule over random chance (Lift > 1 implies a positive correlation).

### **Application in Menu Planning**
*   **Recommendation**: Suggest complementary items to customers (Upselling/Cross-selling).
*   **Layout**: Place combo items together on the physical/digital menu.

## 2. Customer Segmentation (RFM + K-Means)

### **What is it?**
Grouping customers based on shared characteristics to tailor marketing strategies.

### **How it Works (Simple Terms)**
*   **Recency (R)**: Days since last purchase (Lower is better).
*   **Frequency (F)**: Total number of purchases (Higher is better).
*   **Monetary (M)**: Total amount spent (Higher is better).
*   **K-Means Clustering**: An algorithm that partitions customers into *K* groups (clusters) where customers in the same group are more similar to each other than to those in other groups.

### **Application in Menu Planning**
*   **Targeted Offers**: Send discounts to "at-risk" customers or exclusive deals to "champions".
*   **Retention**: Identify loyal customers and reward them.

## 3. Demand Forecasting (Time Series / Regression)

### **What is it?**
Predicting future values based on historical data patterns.

### **How it Works (Simple Terms)**
*   **Moving Average**: Smooths out short-term fluctuations to highlight longer-term trends or cycles.
*   **Linear Regression**: Finds a linear relationship between time (or other features like day of week) and sales volume.
*   **Seasonality**: Accounts for recurring patterns (e.g., higher sales on weekends).

### **Application in Menu Planning**
*   **Inventory**: Order the right amount of ingredients to minimize waste.
*   **Staffing**: Schedule enough staff for predicted busy days.

## 4. Menu Engineering Matrix

### **What is it?**
A strategic framework to analyze menu item performance based on two dimensions: **Popularity** (Volume) and **Profitability** (Contribution Margin).

### **How it Works (Simple Terms)**
*   **Star**: High Popularity, High Profit. Keep and promote.
*   **Puzzle**: Low Popularity, High Profit. Make more visible or rename.
*   **Plowhorse**: High Popularity, Low Profit. Increase price or reduce cost.
*   **Dog**: Low Popularity, Low Profit. Remove from menu.

### **Application in Menu Planning**
*   **Optimization**: Directly tells the manager which items to keep, change, or remove.
