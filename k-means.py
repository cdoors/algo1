import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv('sp500.csv', parse_dates=['date'], index_col=['date', 'ticker'])

# Ensure the DataFrame isn't empty after loading
if df.empty:
    raise ValueError("DataFrame is empty. Check the CSV file path and contents.")

# Specify the features to be used for clustering
features = ['MACD', 'MACD_signal', 'MACD_hist', 'prev_day_change']

# Convert features to numeric, handling non-numeric values by converting them to NaN
for feature in features:
    df[feature] = pd.to_numeric(df[feature], errors='coerce')

# Instead of dropping NaN values, fill them with the mean of their respective columns
for feature in features:
    df[feature].fillna(df[feature].mean(), inplace=True)

# Ensure there's enough data after preprocessing
if df[features].shape[0] == 0:
    raise ValueError("No data left after preprocessing! Check your data cleaning steps.")

# Data normalization
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df[features])

# Apply K-Means clustering
n_clusters = 5  # Number of clusters can be adjusted
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
clusters = kmeans.fit_predict(df_scaled)

# Adding cluster labels to the DataFrame
df['cluster'] = clusters

# Visualization: Distribution of Stocks in Clusters
plt.figure(figsize=(10, 6))
sns.countplot(x=df['cluster'])
plt.title('Distribution of Stocks in Clusters')
plt.xlabel('Cluster')
plt.ylabel('Number of Stocks')
plt.show()

# Advanced Visualization: Pairplot for Feature Relationships by Cluster
# Note: This can be computationally intensive for large datasets
sns.pairplot(df[features + ['cluster']], hue='cluster', palette='viridis', corner=True)
plt.suptitle('Pairplot of Features by Cluster', size=20, y=1.02)
plt.show()

# Save the clustered data to a new CSV file
df.to_csv('sp500_clustered.csv')
