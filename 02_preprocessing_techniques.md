# Data Preprocessing Techniques

## 1. Introduction to Data Preprocessing

### 1.1 Definition

Data preprocessing is the process of transforming raw data into a clean, consistent, and usable format suitable for analysis. It is a critical step in the data mining process, as the quality of results directly depends on the quality of input data.

### 1.2 Importance of Data Preprocessing

- **Improves Data Quality**: Removes errors and inconsistencies
- **Enhances Analysis Accuracy**: Clean data produces reliable results
- **Reduces Processing Time**: Optimized data improves algorithm efficiency
- **Enables Feature Engineering**: Creates meaningful attributes for modeling

### 1.3 Common Data Quality Issues

| Issue | Description | Example |
|-------|-------------|---------|
| Missing Values | Absent data entries | Null customer age |
| Duplicate Records | Repeated entries | Same transaction recorded twice |
| Inconsistent Data | Conflicting information | Different date formats |
| Noisy Data | Random errors or outliers | Negative quantity values |
| Irrelevant Data | Non-useful attributes | Unused columns |

---

## 2. Data Cleaning

### 2.1 Handling Missing Values

**Strategies:**

1. **Deletion Methods**
   - Listwise deletion: Remove entire record
   - Pairwise deletion: Remove only affected attributes

2. **Imputation Methods**
   - Mean/Median/Mode substitution
   - Forward/Backward fill (for time series)
   - Regression imputation
   - K-Nearest Neighbors imputation

3. **Indicator Method**
   - Create binary indicator for missing values

**Python Example:**
```python
import pandas as pd
from sklearn.impute import SimpleImputer

# Mean imputation
imputer = SimpleImputer(strategy='mean')
df['price'] = imputer.fit_transform(df[['price']])

# Mode imputation for categorical
df['category'].fillna(df['category'].mode()[0], inplace=True)
```

### 2.2 Handling Duplicate Records

**Detection and Removal:**
```python
# Identify duplicates
duplicates = df.duplicated()

# Remove duplicates
df_clean = df.drop_duplicates()

# Keep first/last occurrence
df_clean = df.drop_duplicates(keep='first')
```

### 2.3 Handling Outliers

**Detection Methods:**
- Z-Score method (values beyond 3 standard deviations)
- Interquartile Range (IQR) method
- Visualization (box plots, scatter plots)

**Treatment Options:**
- Remove outliers
- Cap/Floor values (winsorization)
- Transform data (log transformation)
- Treat as separate category

**Python Example:**
```python
import numpy as np

# IQR method
Q1 = df['price'].quantile(0.25)
Q3 = df['price'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Remove outliers
df_clean = df[(df['price'] >= lower_bound) & (df['price'] <= upper_bound)]
```

### 2.4 Correcting Inconsistencies

**Common Issues:**
- Inconsistent capitalization ("Pizza" vs "pizza")
- Different date formats ("01/02/2024" vs "2024-02-01")
- Abbreviation variations ("St." vs "Street")

**Solutions:**
```python
# Standardize text
df['item_name'] = df['item_name'].str.lower().str.strip()

# Standardize dates
df['date'] = pd.to_datetime(df['date'], format='mixed')

# Replace inconsistent values
df['category'].replace({'veg': 'Vegetarian', 'Veg': 'Vegetarian'}, inplace=True)
```

---

## 3. Data Integration

### 3.1 Definition

Data integration combines data from multiple sources into a unified dataset.

### 3.2 Challenges

- **Schema Integration**: Different attribute names for same concept
- **Entity Identification**: Matching records across sources
- **Handling Redundancy**: Avoiding duplicate information
- **Value Conflicts**: Resolving contradictory data

### 3.3 Techniques

1. **Data Warehousing**: Centralized repository for integrated data
2. **Schema Matching**: Aligning attributes from different sources
3. **Entity Resolution**: Identifying same entities across datasets

---

## 4. Data Transformation

### 4.1 Normalization

Scaling numerical values to a standard range.

**Min-Max Normalization:**
```
x' = (x - min) / (max - min)
```

**Z-Score Normalization:**
```
x' = (x - mean) / standard_deviation
```

**Python Example:**
```python
from sklearn.preprocessing import MinMaxScaler, StandardScaler

# Min-Max scaling
scaler = MinMaxScaler()
df['price_normalized'] = scaler.fit_transform(df[['price']])

# Z-Score scaling
std_scaler = StandardScaler()
df['price_standardized'] = std_scaler.fit_transform(df[['price']])
```

### 4.2 Encoding Categorical Variables

**Label Encoding:**
```python
from sklearn.preprocessing import LabelEncoder

encoder = LabelEncoder()
df['category_encoded'] = encoder.fit_transform(df['category'])
```

**One-Hot Encoding:**
```python
df_encoded = pd.get_dummies(df, columns=['category'], prefix='cat')
```

### 4.3 Feature Extraction

Creating new features from existing data.

**Examples:**
```python
# Extract day of week
df['day_of_week'] = df['date'].dt.dayofweek

# Create price category
df['price_category'] = pd.cut(df['price'], bins=[0, 100, 300, 500], 
                               labels=['Low', 'Medium', 'High'])

# Calculate total amount
df['total'] = df['quantity'] * df['unit_price']
```

### 4.4 Aggregation

Summarizing data at higher levels.

```python
# Daily sales aggregation
daily_sales = df.groupby('date').agg({
    'quantity': 'sum',
    'total': 'sum',
    'transaction_id': 'count'
}).reset_index()

# Item-level aggregation
item_summary = df.groupby('item_name').agg({
    'quantity': ['sum', 'mean'],
    'total': 'sum'
}).reset_index()
```

---

## 5. Data Reduction

### 5.1 Purpose

Reducing dataset size while maintaining analytical integrity.

### 5.2 Techniques

**1. Dimensionality Reduction:**
- Principal Component Analysis (PCA)
- Feature selection methods

**2. Numerosity Reduction:**
- Sampling (random, stratified)
- Histogram-based methods
- Clustering-based compression

**3. Data Compression:**
- Lossless compression
- Lossy compression

**Python Example (PCA):**
```python
from sklearn.decomposition import PCA

pca = PCA(n_components=5)
reduced_features = pca.fit_transform(df_numerical)
```

---

## 6. Data Discretization

### 6.1 Definition

Converting continuous attributes into categorical intervals.

### 6.2 Methods

**Equal-Width Binning:**
```python
df['price_bin'] = pd.cut(df['price'], bins=5)
```

**Equal-Frequency Binning:**
```python
df['price_bin'] = pd.qcut(df['price'], q=5)
```

**Custom Binning:**
```python
bins = [0, 50, 150, 300, 500, float('inf')]
labels = ['Very Low', 'Low', 'Medium', 'High', 'Premium']
df['price_category'] = pd.cut(df['price'], bins=bins, labels=labels)
```

---

## 7. Preprocessing Pipeline

### 7.1 Creating a Complete Pipeline

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

# Define transformers
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(handle_unknown='ignore'))
])

# Combine transformers
preprocessor = ColumnTransformer(transformers=[
    ('num', numeric_transformer, ['price', 'quantity']),
    ('cat', categorical_transformer, ['category', 'season'])
])

# Apply pipeline
X_processed = preprocessor.fit_transform(df)
```

---

## 8. Summary

Data preprocessing is essential for successful data mining projects. The key steps include:

1. **Data Cleaning**: Handle missing values, duplicates, and outliers
2. **Data Integration**: Combine data from multiple sources
3. **Data Transformation**: Normalize, encode, and derive features
4. **Data Reduction**: Reduce dimensionality and size
5. **Data Discretization**: Convert continuous to categorical

Proper preprocessing ensures that subsequent analysis produces accurate and reliable results for menu planning optimization.
