import os
import numpy as np
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns

# Load environment variables from .env file
load_dotenv()

# Fetch database connection parameters from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def satisfaction_analysis(df):
    # Separate numeric and non-numeric columns
    numeric_columns = df.select_dtypes(include=['number']).columns
    non_numeric_columns = df.select_dtypes(exclude=['number']).columns

    # Handle missing values in numeric columns using SimpleImputer
    imputer = SimpleImputer(strategy='mean')
    df[numeric_columns] = imputer.fit_transform(df[numeric_columns])

    # For non-numeric columns, fill missing values with a placeholder
    df[non_numeric_columns] = df[non_numeric_columns].fillna('missing')

    # Step 1: Engagement Score (Cluster for less engaged users)
    engagement_features = ['Total UL (Bytes)', 'Total DL (Bytes)', 'Dur. (ms)']
    kmeans_engagement = KMeans(n_clusters=2, random_state=42).fit(df[engagement_features])
    df['engagement_cluster'] = kmeans_engagement.labels_

    # Identify the less engaged cluster (smaller centroid sum)
    cluster_centroids = kmeans_engagement.cluster_centers_
    less_engaged_cluster = np.argmin(np.sum(cluster_centroids, axis=1))

    # Calculate engagement scores (Euclidean distance to less engaged cluster)
    df['engagement_score'] = np.linalg.norm(
        df[engagement_features] - cluster_centroids[less_engaged_cluster], axis=1
    )

    # Step 2: Experience Score (Cluster for worst experience)
    experience_features = ['Youtube DL (Bytes)', 'Netflix DL (Bytes)', 'Gaming DL (Bytes)']
    kmeans_experience = KMeans(n_clusters=2, random_state=42).fit(df[experience_features])
    df['experience_cluster'] = kmeans_experience.labels_

    # Identify the worst experience cluster
    experience_centroids = kmeans_experience.cluster_centers_
    worst_experience_cluster = np.argmin(np.sum(experience_centroids, axis=1))

    # Calculate experience scores (Euclidean distance to worst experience cluster)
    df['experience_score'] = np.linalg.norm(
        df[experience_features] - experience_centroids[worst_experience_cluster], axis=1
    )

    # Step 3: Satisfaction Score
    df['satisfaction_score'] = (df['engagement_score'] + df['experience_score']) / 2

    # Step 4: Top 10 Satisfied Customers
    top_10_satisfied = df.nlargest(10, 'satisfaction_score')

    # Step 5: Regression Model
    regression_features = engagement_features + experience_features
    model = LinearRegression()
    model.fit(df[regression_features], df['satisfaction_score'])

    # Step 6: K-Means Clustering on Engagement & Experience Scores
    kmeans_satisfaction = KMeans(n_clusters=2, random_state=42).fit(
        df[['engagement_score', 'experience_score']]
    )
    df['satisfaction_cluster'] = kmeans_satisfaction.labels_

    # Step 7: Cluster Aggregates
    cluster_aggregates = df.groupby('satisfaction_cluster')[
        ['satisfaction_score', 'experience_score']
    ].mean()

    # Visualization of Engagement and Experience Clusters
    plt.figure(figsize=(12, 6))
    plt.scatter(df['Total UL (Bytes)'], df['Total DL (Bytes)'], c=df['engagement_cluster'], cmap='viridis')
    plt.title('Engagement Clusters')
    plt.xlabel('Total UL (Bytes)')
    plt.ylabel('Total DL (Bytes)')
    plt.colorbar(label='Cluster')
    plt.show()

    # Visualization of Experience Clusters
    plt.figure(figsize=(12, 6))
    plt.scatter(df['Youtube DL (Bytes)'], df['Netflix DL (Bytes)'], c=df['experience_cluster'], cmap='plasma')
    plt.title('Experience Clusters')
    plt.xlabel('Youtube DL (Bytes)')
    plt.ylabel('Netflix DL (Bytes)')
    plt.colorbar(label='Cluster')
    plt.show()

    # Visualization of Satisfaction Scores Distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(df['satisfaction_score'], kde=True, bins=30, color='blue')
    plt.title('Satisfaction Score Distribution')
    plt.xlabel('Satisfaction Score')
    plt.ylabel('Frequency')
    plt.show()

    # Visualization of Top 10 Satisfied Customers
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_10_satisfied['Bearer Id'], y=top_10_satisfied['satisfaction_score'], palette="Blues_d")
    plt.title('Top 10 Satisfied Customers')
    plt.xlabel('Bearer Id')
    plt.ylabel('Satisfaction Score')
    plt.xticks(rotation=45)
    plt.show()

    # Visualization of Cluster Aggregates
    plt.figure(figsize=(10, 6))
    cluster_aggregates.plot(kind='bar', figsize=(12, 6), colormap="coolwarm")
    plt.title('Cluster Aggregates for Satisfaction Score and Experience Score')
    plt.xlabel('Cluster')
    plt.ylabel('Score')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()

    # Step 8: Export Results
    try:
        engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        df[['Bearer Id', 'engagement_score', 'experience_score', 'satisfaction_score']].to_sql(
            'satisfaction_analysis', engine, if_exists='replace', index=False
        )
        print("Data successfully exported to PostgreSQL table 'satisfaction_analysis'.")
    except Exception as e:
        print(f"An error occurred during export: {e}")

    return {
        'top_10_satisfied': top_10_satisfied,
        'regression_model': model,
        'cluster_aggregates': cluster_aggregates
    }

