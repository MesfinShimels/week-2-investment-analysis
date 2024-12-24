import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Task 1: Aggregate engagement metrics
def aggregate_engagement_metrics(df):
    """
    Aggregates session metrics: session frequency, duration, and total traffic for each user.
    """
    metrics = df.groupby('IMSI').agg({
        'Dur. (ms)': 'sum',
        'Total UL (Bytes)': 'sum',
        'Total DL (Bytes)': 'sum'
    }).rename(columns={
        'Dur. (ms)': 'Total_Duration',
        'Total UL (Bytes)': 'Total_UL',
        'Total DL (Bytes)': 'Total_DL'
    })
    metrics['Total_Traffic'] = metrics['Total_UL'] + metrics['Total_DL']
    metrics['Session_Frequency'] = df.groupby('IMSI')['Bearer Id'].count()
    return metrics

# Task 2: Perform user clustering
def perform_user_clustering(engagement_metrics):
    """
    Applies k-means clustering to segment users into engagement groups.
    """
    data = engagement_metrics[['Session_Frequency', 'Total_Duration', 'Total_Traffic']]
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)

    # Optimal number of clusters (for now, we use 3 clusters)
    kmeans = KMeans(n_clusters=3, random_state=42)
    engagement_metrics['Cluster'] = kmeans.fit_predict(scaled_data)

    return engagement_metrics

# Task 3: Visualize top engaged users
def plot_top_engaged_users(engagement_metrics):
    """
    Plots the top 10 engaged users based on total traffic.
    """
    top_users = engagement_metrics.sort_values(by='Total_Traffic', ascending=False).head(10)
    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_users.index, y=top_users['Total_Traffic'], palette="coolwarm")
    plt.title("Top 10 Engaged Users by Total Traffic")
    plt.xlabel("User IMSI")
    plt.ylabel("Total Traffic (Bytes)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Task 4: Visualize most used applications
def plot_most_used_applications(df):
    """
    Plots the total data volume (DL + UL) for each application.
    """
    app_data = df[['Social Media DL (Bytes)', 'Social Media UL (Bytes)',
                   'Youtube DL (Bytes)', 'Youtube UL (Bytes)',
                   'Gaming DL (Bytes)', 'Gaming UL (Bytes)',
                   'Email DL (Bytes)', 'Email UL (Bytes)']]

    app_data = app_data.sum()
    app_data = app_data[::2] + app_data[1::2]  # Combine DL and UL for each application
    app_data.index = ['Social Media', 'YouTube', 'Gaming', 'Email']

    plt.figure(figsize=(12, 6))
    sns.barplot(x=app_data.index, y=app_data.values, palette="viridis")
    plt.title("Most Used Applications by Total Data Volume")
    plt.xlabel("Application")
    plt.ylabel("Total Data Volume (Bytes)")
    plt.tight_layout()
    plt.show()
