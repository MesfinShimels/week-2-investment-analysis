import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Database connection details
DB_CONFIG = {
    "dbname": "xdr_data_db",
    "user": "postgres",
    "password": "your_password",
    "host": "localhost",
    "port": "5432"
}

# Function to create a database connection
def create_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

# Task 1.1 - User Behavior Overview
def get_user_behavior_data():
    query = """
    SELECT 
        "MSISDN/Number" AS user_id,
        COUNT(*) AS num_sessions,
        SUM("Dur. (ms)") AS total_duration,
        SUM("Total DL (Bytes)") AS total_download,
        SUM("Total UL (Bytes)") AS total_upload,
        SUM("Total DL (Bytes)" + "Total UL (Bytes)") AS total_volume,
        SUM("Social Media DL (Bytes)" + "Social Media UL (Bytes)") AS social_media_volume,
        SUM("Google DL (Bytes)" + "Google UL (Bytes)") AS google_volume,
        SUM("Email DL (Bytes)" + "Email UL (Bytes)") AS email_volume,
        SUM("Youtube DL (Bytes)" + "Youtube UL (Bytes)") AS youtube_volume,
        SUM("Netflix DL (Bytes)" + "Netflix UL (Bytes)") AS netflix_volume,
        SUM("Gaming DL (Bytes)" + "Gaming UL (Bytes)") AS gaming_volume,
        SUM("Other DL (Bytes)" + "Other UL (Bytes)") AS other_volume
    FROM public.xdr_data
    GROUP BY "MSISDN/Number";
    """
    conn = create_connection()
    if conn:
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    else:
        return None

# Task 1.2 - Handling Missing Values
def handle_missing_values(df):
    return df.fillna(df.mean(numeric_only=True))

# Task 1.2 - Exploratory Data Analysis
def exploratory_analysis(df):
    print("Basic Metrics:")
    print(df.describe())
    print("\nMissing Values:")
    print(df.isnull().sum())

    # Plot distribution of session duration
    plt.figure(figsize=(10, 6))
    sns.histplot(df['total_duration'], kde=True, bins=30)
    plt.title('Distribution of Total Session Duration')
    plt.xlabel('Total Duration (ms)')
    plt.ylabel('Frequency')
    plt.show()

# Task 1.2 - Variable Transformation and Segmentation
def segment_users_by_decile(df):
    df['decile'] = pd.qcut(df['total_duration'], 10, labels=False)
    decile_summary = df.groupby('decile').agg(
        total_data_volume=('total_volume', 'sum'),
        avg_session_duration=('total_duration', 'mean')
    ).reset_index()
    return decile_summary

# Task 1.2 - Correlation Analysis
def correlation_analysis(df):
    correlation_columns = [
        'social_media_volume', 'google_volume', 'email_volume',
        'youtube_volume', 'netflix_volume', 'gaming_volume', 'other_volume'
    ]
    correlation_matrix = df[correlation_columns].corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
    plt.title("Correlation Matrix")
    plt.show()
    return correlation_matrix

# Task 1.2 - Dimensionality Reduction
def perform_pca(df):
    features = [
        'social_media_volume', 'google_volume', 'email_volume',
        'youtube_volume', 'netflix_volume', 'gaming_volume', 'other_volume'
    ]
    x = df[features].fillna(0).values
    x_scaled = StandardScaler().fit_transform(x)
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(x_scaled)
    explained_variance = pca.explained_variance_ratio_
    print("Explained Variance Ratios:", explained_variance)
    return pd.DataFrame(principal_components, columns=['PC1', 'PC2'])

