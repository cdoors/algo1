import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Load the cleaned data
df = pd.read_csv('sp500.csv', parse_dates=['date'], index_col=['date', 'ticker'])

# Select features for clustering
# It's assumed that relevant financial indicators (e.g., MACD features, prev_day_change) are included
features = ['MACD', 'MACD_signal', 'MACD_hist', 'prev_day_change']
X = df[features].values

# Normalize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply K-Means clustering
kmeans = KMeans(n_clusters=5, random_state=42)  # Adjust n_clusters as needed
clusters = kmeans.fit_predict(X_scaled)

# Add cluster labels to the DataFrame
df['cluster'] = clusters

# Example: Save the DataFrame with cluster labels for further analysis
df.to_csv('sp500_clustered.csv')
