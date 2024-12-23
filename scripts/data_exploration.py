import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def explore_data(df):
    """
    Performs exploratory data analysis (EDA) on a DataFrame.

    Parameters:
        df (pd.DataFrame): The DataFrame to explore.

    Returns:
        None: Outputs key findings and visualizations.
    """
    # 1. Basic Information
    print("### Dataset Info ###")
    print(df.info())
    print("\n### Dataset Shape ###")
    print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
    
    # 2. Summary Statistics
    print("\n### Summary Statistics ###")
    print(df.describe(include='all'))
    
    # 3. Check for Missing Values
    print("\n### Missing Values ###")
    missing_values = df.isnull().sum().sort_values(ascending=False)
    print(missing_values[missing_values > 0])
    
    # 4. Check for Duplicates
    print("\n### Duplicate Rows ###")
    duplicates = df.duplicated().sum()
    print(f"Duplicate Rows: {duplicates}")
    
    # 5. Correlation Matrix (Numerical Columns)
    print("\n### Correlation Matrix ###")
    try:
        # Select only numeric columns for correlation
        numeric_cols = df.select_dtypes(include=[np.number])
        if not numeric_cols.empty:
            correlation_matrix = numeric_cols.corr()
            plt.figure(figsize=(12, 8))
            sns.heatmap(correlation_matrix, annot=False, cmap='coolwarm')
            plt.title("Correlation Matrix")
            plt.show()
        else:
            print("No numeric columns available for correlation matrix.")
    except Exception as e:
        print(f"An error occurred while computing the correlation matrix: {e}")
    
    # 6. Visualizations
    print("\n### Visualizations ###")
    
    # Distribution of Numeric Columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols[:5]:  # Limit to first 5 for brevity
        sns.histplot(df[col].dropna(), kde=True, bins=30)
        plt.title(f"Distribution of {col}")
        plt.xlabel(col)
        plt.ylabel("Frequency")
        plt.show()

    # Bar plot for Categorical Columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols[:5]:  # Limit to first 5 for brevity
        sns.countplot(data=df, y=col, order=df[col].value_counts().index)
        plt.title(f"Value Counts for {col}")
        plt.xlabel("Count")
        plt.ylabel(col)
        plt.show()
    
    # Pair Plot for Numerical Columns
    if len(numeric_cols) > 1:
        print("\n### Pair Plot (First 5 Numeric Columns) ###")
        sns.pairplot(df[numeric_cols[:5]])
        plt.show()
