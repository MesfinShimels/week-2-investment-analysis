# user_overview_analysis.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA

def aggregate_user_behavior(df):
    """
    Aggregates user behavior data for specified applications.
    """
    app_columns = {
        "Social Media": ["Social Media DL (Bytes)", "Social Media UL (Bytes)"],
        "Google": ["Google DL (Bytes)", "Google UL (Bytes)"],
        "Email": ["Email DL (Bytes)", "Email UL (Bytes)"],
        "YouTube": ["Youtube DL (Bytes)", "Youtube UL (Bytes)"],
        "Netflix": ["Netflix DL (Bytes)", "Netflix UL (Bytes)"],
        "Gaming": ["Gaming DL (Bytes)", "Gaming UL (Bytes)"],
        "Other": ["Other DL (Bytes)", "Other UL (Bytes)"],
    }
    
    # Group by IMSI and perform the main aggregations
    user_agg = df.groupby("IMSI").agg(
        total_xDR_sessions=("Bearer Id", "count"),
        total_session_duration=("Dur. (ms)", "sum"),
    ).reset_index()
    
    # Add total data for each application by summing the respective columns
    for app, cols in app_columns.items():
        # Sum the download and upload bytes for each application
        total_data = df.groupby("IMSI")[cols].sum().sum(axis=1).reset_index(drop=True)
        user_agg[f"total_{app}_data"] = total_data

    return user_agg




# Task 1.2 - Exploratory Data Analysis
def describe_variables(df):
    """
    Prints description of variables and their data types.
    """
    print(df.info())
    print(df.describe())

import pandas as pd

import pandas as pd

def handle_missing_values(df, strategy="mean"):
    """
    Handles missing values in the dataset by filling numeric columns with a specified strategy
    (mean, median, or mode) and categorical columns with their mode (most frequent value).
    
    Parameters:
    - df: pandas DataFrame to process
    - strategy: Strategy for filling missing values in numeric columns. Default is 'mean'.
    
    Returns:
    - df: pandas DataFrame with missing values handled
    """
    
    if df.empty:
        print("DataFrame is empty. No action taken.")
        return df  # Return the empty dataframe if no data is available
    
    # Handling numeric columns
    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns
    if strategy == "mean":
        for col in numeric_cols:
            if df[col].isnull().any():
                df[col] = df[col].fillna(df[col].mean())  # Fill with column mean
    elif strategy == "median":
        for col in numeric_cols:
            if df[col].isnull().any():
                df[col] = df[col].fillna(df[col].median())  # Fill with column median
    else:
        print("Unsupported strategy for numeric columns. Use 'mean' or 'median'.")
    
    # Handling categorical columns
    categorical_cols = df.select_dtypes(include=["object"]).columns
    for col in categorical_cols:
        if df[col].isnull().any():
            # Safely handle mode by checking if mode exists
            mode_value = df[col].mode()
            if not mode_value.empty:
                df[col] = df[col].fillna(mode_value[0])  # Fill with the most frequent value
            else:
                df[col] = df[col].fillna('Unknown')  # Fill with a default value if no mode is found
    
    return df



def perform_variable_transformations(df):
    """
    Segments users into decile classes based on session duration and calculates total data usage.
    """
    # Check if the expected columns exist in the DataFrame, handle missing columns
    if 'Total DL (Bytes)' not in df.columns or 'Total UL (Bytes)' not in df.columns:
        raise KeyError("Missing required columns: 'Total DL (Bytes)' or 'Total UL (Bytes)'")
    
    # Segment users into decile classes based on session duration
    df['decile'] = pd.qcut(df['total_session_duration'], 10, labels=False) + 1

    # Create a new column for total data usage (DL + UL)
    df['total_data'] = df['Total DL (Bytes)'] + df['Total UL (Bytes)']
    
    # Summarize data by decile
    decile_summary = df.groupby('decile')[['total_data']].sum().reset_index()
    
    return decile_summary


# Statistical Analysis
def compute_dispersion(df):
    """
    Computes dispersion metrics for quantitative variables.
    """
    metrics = df.describe().T
    print(metrics[['mean', 'std', 'min', '25%', '50%', '75%', 'max']])

# Graphical Analysis
def plot_graphical_analysis(df):
    """
    Generates suitable plots for variables.
    """
    plt.figure(figsize=(10, 6))
    sns.histplot(df['total_session_duration'], kde=True)
    plt.title("Distribution of Session Durations")
    plt.show()

def correlation_analysis(df, columns):
    """
    Computes and visualizes a correlation matrix.
    """
    corr_matrix = df[columns].corr()
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm')
    plt.title("Correlation Matrix")
    plt.show()

# Dimensionality Reduction
def perform_pca(df, columns):
    """
    Performs PCA on specified columns and interprets results.
    """
    pca = PCA()
    principal_components = pca.fit_transform(df[columns])
    explained_variance = pca.explained_variance_ratio_
    print(f"Explained Variance: {explained_variance}")
    return principal_components

# Main Executionif __name__ == "__main__":
    # Load data
    # df = pd.read_csv("telecom_data.csv")  # Replace with your actual file path

    # # Preprocessing
    # df = handle_missing_values(df)

    # # Task 1.1 - Aggregation
    # user_behavior = aggregate_user_behavior(df)
    # print(user_behavior.head())

    # # Task 1.2 - EDA
    # describe_variables(df)
    # decile_summary = perform_variable_transformations(user_behavior)
    # print(decile_summary)

    # # Graphical Analysis
    # plot_graphical_analysis(user_behavior)

    # # Correlation Analysis
    # app_columns = [
    #     "Social Media DL (Bytes)", "Social Media UL (Bytes)", 
    #     "Google DL (Bytes)", "Google UL (Bytes)", 
    #     "Email DL (Bytes)", "Email UL (Bytes)", 
    #     "Youtube DL (Bytes)", "Youtube UL (Bytes)",
    #     "Netflix DL (Bytes)", "Netflix UL (Bytes)",
    #     "Gaming DL (Bytes)", "Gaming UL (Bytes)",
    #     "Other DL (Bytes)", "Other UL (Bytes)"
    # ]
    # correlation_analysis(df, app_columns)

    # # Dimensionality Reduction
    # principal_components = perform_pca(df, app_columns)
