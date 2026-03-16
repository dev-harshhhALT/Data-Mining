# Data Mining Algorithms

## 1. Classification Algorithms

### 1.1 Decision Tree

#### Definition
A Decision Tree is a tree-structured classifier where internal nodes represent attribute tests, branches represent test outcomes, and leaf nodes represent class labels.

#### Algorithm: ID3 (Iterative Dichotomizer 3)

**Steps:**
1. Calculate entropy of the target variable
2. Calculate information gain for each attribute
3. Select attribute with highest information gain as root
4. Partition data based on attribute values
5. Recursively apply to subsets until stopping criteria

**Key Formulas:**

**Entropy:**
```
H(S) = -Σ p(i) * log2(p(i))
```
Where p(i) is the probability of class i.

**Information Gain:**
```
IG(S, A) = H(S) - Σ (|Sv| / |S|) * H(Sv)
```
Where Sv is the subset where attribute A has value v.

#### Python Implementation
```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

# Prepare data
X = df[['price', 'quantity', 'category_encoded']]
y = df['popularity']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
clf = DecisionTreeClassifier(max_depth=5, criterion='entropy')
clf.fit(X_train, y_train)

# Predict
predictions = clf.predict(X_test)
```

#### Advantages
- Easy to understand and interpret
- Handles both numerical and categorical data
- Requires minimal data preparation

#### Disadvantages
- Prone to overfitting
- Sensitive to small data changes
- Can create biased trees with imbalanced data

---

### 1.2 Naive Bayes Classifier

#### Definition
A probabilistic classifier based on Bayes' theorem, assuming independence between features.

**Bayes' Theorem:**
```
P(C|X) = P(X|C) * P(C) / P(X)
```

Where:
- P(C|X) = Posterior probability of class C given features X
- P(X|C) = Likelihood of features given class
- P(C) = Prior probability of class
- P(X) = Evidence

#### Python Implementation
```python
from sklearn.naive_bayes import GaussianNB

# Train model
nb_classifier = GaussianNB()
nb_classifier.fit(X_train, y_train)

# Predict
predictions = nb_classifier.predict(X_test)
```

#### Advantages
- Fast training and prediction
- Works well with high-dimensional data
- Effective for text classification

#### Disadvantages
- Assumes feature independence (rarely true)
- Sensitive to irrelevant features

---

### 1.3 K-Nearest Neighbors (KNN)

#### Definition
A non-parametric algorithm that classifies data points based on the majority class of their K nearest neighbors.

**Distance Metrics:**

**Euclidean Distance:**
```
d(x, y) = sqrt(Σ (xi - yi)^2)
```

**Manhattan Distance:**
```
d(x, y) = Σ |xi - yi|
```

#### Python Implementation
```python
from sklearn.neighbors import KNeighborsClassifier

# Train model
knn = KNeighborsClassifier(n_neighbors=5, metric='euclidean')
knn.fit(X_train, y_train)

# Predict
predictions = knn.predict(X_test)
```

---

## 2. Clustering Algorithms

### 2.1 K-Means Clustering

#### Definition
An unsupervised algorithm that partitions data into K clusters by minimizing within-cluster variance.

#### Algorithm Steps
1. Initialize K cluster centroids randomly
2. Assign each point to nearest centroid
3. Recalculate centroids as mean of assigned points
4. Repeat steps 2-3 until convergence

#### Objective Function
```
J = Σ Σ ||x - μk||^2
```
Where μk is the centroid of cluster k.

#### Python Implementation
```python
from sklearn.cluster import KMeans

# Apply K-Means
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df['cluster'] = kmeans.fit_predict(X)

# Get centroids
centroids = kmeans.cluster_centers_
```

#### Choosing K (Elbow Method)
```python
import matplotlib.pyplot as plt

inertias = []
K_range = range(1, 11)

for k in K_range:
    km = KMeans(n_clusters=k, random_state=42)
    km.fit(X)
    inertias.append(km.inertia_)

plt.plot(K_range, inertias, 'bx-')
plt.xlabel('Number of Clusters (K)')
plt.ylabel('Inertia')
plt.title('Elbow Method')
plt.show()
```

#### Advantages
- Simple and efficient
- Scales well to large datasets
- Guaranteed convergence

#### Disadvantages
- Requires specifying K in advance
- Sensitive to initial centroid placement
- Assumes spherical clusters

---

### 2.2 Hierarchical Clustering

#### Definition
Builds a hierarchy of clusters using either agglomerative (bottom-up) or divisive (top-down) approach.

#### Agglomerative Algorithm Steps
1. Treat each point as individual cluster
2. Find two closest clusters
3. Merge them into one cluster
4. Repeat until single cluster remains

#### Linkage Methods
- **Single Linkage**: Minimum distance between points
- **Complete Linkage**: Maximum distance between points
- **Average Linkage**: Average distance between all pairs
- **Ward's Method**: Minimize variance increase

#### Python Implementation
```python
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage

# Perform clustering
hc = AgglomerativeClustering(n_clusters=4, linkage='ward')
df['cluster'] = hc.fit_predict(X)

# Create dendrogram
Z = linkage(X, method='ward')
dendrogram(Z)
plt.show()
```

---

## 3. Association Rule Mining

### 3.1 Apriori Algorithm

#### Definition
Discovers frequent itemsets and generates association rules from transactional data.

#### Key Concepts

**Support:**
```
Support(A) = (Transactions containing A) / (Total Transactions)
```

**Confidence:**
```
Confidence(A → B) = Support(A ∪ B) / Support(A)
```

**Lift:**
```
Lift(A → B) = Confidence(A → B) / Support(B)
```

#### Algorithm Steps
1. Set minimum support threshold
2. Generate frequent 1-itemsets
3. Use frequent (k-1)-itemsets to generate k-itemsets
4. Prune itemsets below minimum support
5. Generate rules from frequent itemsets
6. Filter rules by minimum confidence

#### Python Implementation
```python
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

# Prepare transaction data
transactions = [
    ['Pizza', 'Cold Drink', 'Fries'],
    ['Burger', 'Cold Drink'],
    ['Pizza', 'Burger', 'Cold Drink'],
    ['Pizza', 'Fries']
]

# Encode transactions
te = TransactionEncoder()
te_array = te.fit_transform(transactions)
df_trans = pd.DataFrame(te_array, columns=te.columns_)

# Find frequent itemsets
frequent_itemsets = apriori(df_trans, min_support=0.5, use_colnames=True)

# Generate rules
rules = association_rules(frequent_itemsets, metric='confidence', min_threshold=0.7)
print(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']])
```

#### Interpreting Results
| Rule | Support | Confidence | Lift | Interpretation |
|------|---------|------------|------|----------------|
| Pizza → Cold Drink | 0.50 | 0.75 | 1.2 | 75% who buy Pizza also buy Cold Drink |
| Burger → Fries | 0.30 | 0.80 | 1.5 | Strong positive association |

---

### 3.2 FP-Growth Algorithm

#### Definition
A more efficient alternative to Apriori that uses a compressed data structure (FP-Tree) to find frequent patterns without candidate generation.

#### Advantages over Apriori
- Scans database only twice
- No candidate generation required
- More memory efficient
- Faster for large datasets

#### Python Implementation
```python
from mlxtend.frequent_patterns import fpgrowth

# Find frequent itemsets using FP-Growth
frequent_itemsets = fpgrowth(df_trans, min_support=0.5, use_colnames=True)
```

---

## 4. Prediction Algorithms

### 4.1 Linear Regression

#### Definition
Models the relationship between dependent variable and one or more independent variables.

**Equation:**
```
y = β0 + β1*x1 + β2*x2 + ... + ε
```

#### Python Implementation
```python
from sklearn.linear_model import LinearRegression

# Train model
lr = LinearRegression()
lr.fit(X_train, y_train)

# Coefficients
print(f"Intercept: {lr.intercept_}")
print(f"Coefficients: {lr.coef_}")

# Predict
predictions = lr.predict(X_test)
```

### 4.2 Time Series Forecasting

#### Moving Average
```python
df['MA_7'] = df['sales'].rolling(window=7).mean()
```

#### Exponential Smoothing
```python
from statsmodels.tsa.holtwinters import ExponentialSmoothing

model = ExponentialSmoothing(df['sales'], trend='add', seasonal='add', seasonal_periods=7)
fitted = model.fit()
forecast = fitted.forecast(steps=30)
```

---

## 5. Model Evaluation Metrics

### 5.1 Classification Metrics

| Metric | Formula | Description |
|--------|---------|-------------|
| Accuracy | (TP + TN) / Total | Overall correctness |
| Precision | TP / (TP + FP) | Positive predictive value |
| Recall | TP / (TP + FN) | Sensitivity |
| F1-Score | 2 * (Precision * Recall) / (Precision + Recall) | Harmonic mean |

```python
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

print(f"Accuracy: {accuracy_score(y_test, predictions)}")
print(f"Precision: {precision_score(y_test, predictions)}")
print(f"Recall: {recall_score(y_test, predictions)}")
print(f"F1-Score: {f1_score(y_test, predictions)}")
```

### 5.2 Clustering Metrics

| Metric | Description |
|--------|-------------|
| Silhouette Score | Measures cluster cohesion and separation (-1 to 1) |
| Inertia | Within-cluster sum of squares |
| Davies-Bouldin Index | Average similarity between clusters |

```python
from sklearn.metrics import silhouette_score

score = silhouette_score(X, labels)
print(f"Silhouette Score: {score}")
```

---

## 6. Summary

This chapter covered the fundamental data mining algorithms:

1. **Classification**: Decision Tree, Naive Bayes, KNN
2. **Clustering**: K-Means, Hierarchical Clustering
3. **Association Rules**: Apriori, FP-Growth
4. **Prediction**: Linear Regression, Time Series

These algorithms form the core analytical foundation for the menu planning system, enabling pattern discovery, customer segmentation, and demand forecasting.
