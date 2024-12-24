import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

# Task 3.1: Aggregate customer experience metrics
def aggregate_customer_experience(df):
    # Handle missing values and outliers by replacing with mean/mode
    df['TCP DL Retrans. Vol (Bytes)'] = df['TCP DL Retrans. Vol (Bytes)'].fillna(df['TCP DL Retrans. Vol (Bytes)'].mean())
    df['TCP UL Retrans. Vol (Bytes)'] = df['TCP UL Retrans. Vol (Bytes)'].fillna(df['TCP UL Retrans. Vol (Bytes)'].mean())
    df['Avg RTT DL (ms)'] = df['Avg RTT DL (ms)'].fillna(df['Avg RTT DL (ms)'].mean())
    df['Avg RTT UL (ms)'] = df['Avg RTT UL (ms)'].fillna(df['Avg RTT UL (ms)'].mean())
    df['Avg Bearer TP DL (kbps)'] = df['Avg Bearer TP DL (kbps)'].fillna(df['Avg Bearer TP DL (kbps)'].mean())
    df['Avg Bearer TP UL (kbps)'] = df['Avg Bearer TP UL (kbps)'].fillna(df['Avg Bearer TP UL (kbps)'].mean())
    df['Handset Type'] = df['Handset Type'].fillna(df['Handset Type'].mode()[0])

    # Aggregate metrics per customer
    aggregated = df.groupby('MSISDN/Number').agg({
        'TCP DL Retrans. Vol (Bytes)': 'mean',
        'TCP UL Retrans. Vol (Bytes)': 'mean',
        'Avg RTT DL (ms)': 'mean',
        'Avg RTT UL (ms)': 'mean',
        'Handset Type': lambda x: x.mode()[0],
        'Avg Bearer TP DL (kbps)': 'mean',
        'Avg Bearer TP UL (kbps)': 'mean'
    }).reset_index()
    return aggregated

# Task 3.2: Top, bottom, and most frequent values
def compute_top_bottom_frequent(df, column, n=10):
    top_values = df[column].nlargest(n)
    bottom_values = df[column].nsmallest(n)
    frequent_values = df[column].value_counts().head(n)
    return top_values, bottom_values, frequent_values

# Task 3.3: Distribution of throughput and TCP retransmission per handset type
def analyze_distribution(df):
    throughput_dist = df.groupby('Handset Type')[['Avg Bearer TP DL (kbps)', 'Avg Bearer TP UL (kbps)']].mean().sort_values(by='Avg Bearer TP DL (kbps)')
    tcp_retransmission_dist = df.groupby('Handset Type')[['TCP DL Retrans. Vol (Bytes)', 'TCP UL Retrans. Vol (Bytes)']].mean().sort_values(by='TCP DL Retrans. Vol (Bytes)')

    # Plotting throughput distribution with horizontal bar plots for better readability
    plt.figure(figsize=(12, 6))
    throughput_dist[['Avg Bearer TP DL (kbps)', 'Avg Bearer TP UL (kbps)']].plot(kind='barh', stacked=True, width=0.8, figsize=(12, 6), colormap="Blues")
    plt.title('Throughput Distribution per Handset Type')
    plt.xlabel('Throughput (kbps)')
    plt.ylabel('Handset Type')
    plt.tight_layout()
    plt.show()

    # Plotting TCP retransmission distribution with horizontal bar plots for better readability
    plt.figure(figsize=(12, 6))
    tcp_retransmission_dist[['TCP DL Retrans. Vol (Bytes)', 'TCP UL Retrans. Vol (Bytes)']].plot(kind='barh', stacked=True, width=0.8, figsize=(12, 6), colormap="Reds")
    plt.title('TCP Retransmission Distribution per Handset Type')
    plt.xlabel('Retransmission Volume (Bytes)')
    plt.ylabel('Handset Type')
    plt.tight_layout()
    plt.show()

    return throughput_dist, tcp_retransmission_dist

# Task 3.4: K-means clustering for user segmentation
def perform_kmeans_clustering(df, n_clusters=3):
    # Select relevant features for clustering
    features = df[['TCP DL Retrans. Vol (Bytes)', 'TCP UL Retrans. Vol (Bytes)', 'Avg RTT DL (ms)', 'Avg RTT UL (ms)', 'Avg Bearer TP DL (kbps)', 'Avg Bearer TP UL (kbps)']]
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df['Cluster'] = kmeans.fit_predict(features)

    # Cluster descriptions
    cluster_summary = df.groupby('Cluster').mean()
    return kmeans, df, cluster_summary

# Visualization helper function
def plot_distributions(data, column, title):
    plt.figure(figsize=(10, 6))
    sns.histplot(data[column], kde=True, bins=30)
    plt.title(title)
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.show()

# Task 3.5: Visualizing top, bottom, and frequent values
def plot_top_bottom_frequent_values(df, column, n=10):
    # Top values
    top_values, bottom_values, frequent_values = compute_top_bottom_frequent(df, column, n)

    # Plotting top values
    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_values.index, y=top_values.values, palette="viridis")
    plt.title(f"Top {n} {column}")
    plt.xlabel(column)
    plt.ylabel('Value')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Plotting bottom values
    plt.figure(figsize=(12, 6))
    sns.barplot(x=bottom_values.index, y=bottom_values.values, palette="plasma")
    plt.title(f"Bottom {n} {column}")
    plt.xlabel(column)
    plt.ylabel('Value')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Plotting frequent values
    plt.figure(figsize=(12, 6))
    sns.barplot(x=frequent_values.index, y=frequent_values.values, palette="coolwarm")
    plt.title(f"Most Frequent {column}")
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

