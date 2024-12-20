import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def explore_data(df):
    """
    Performs basic exploratory data analysis (EDA) on the given DataFrame.

    :param df: pandas DataFrame to explore.
    :return: None
    """
    try:
        # 1. Basic Information about the Dataset
        print("Basic Info:")
        print(df.info())
        print("\nSummary Statistics:")
        print(df.describe())

        # 2. Display the first few rows of the dataset
        print("\nFirst 5 rows of the dataset:")
        print(df.head())

        # 3. Check for Missing Values
        print("\nMissing Values:")
        print(df.isnull().sum())

        # 4. Visualize Distribution of Numerical Features
        print("\nVisualizing Distribution of Numerical Features...")
        numerical_cols = df.select_dtypes(include=["number"]).columns
        df[numerical_cols].hist(bins=15, figsize=(15, 10))
        plt.suptitle("Histograms of Numerical Features", fontsize=16)
        plt.show()

        # 5. Visualize Correlation Matrix
        print("\nVisualizing Correlation Matrix...")
        correlation_matrix = df.corr()
        plt.figure(figsize=(10, 6))
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
        plt.title("Correlation Matrix", fontsize=16)
        plt.show()

        # 6. Check for Duplicates
        print("\nDuplicate Rows:")
        print(df.duplicated().sum())

        # 7. Visualize Categorical Variables (if any)
        print("\nVisualizing Categorical Features...")
        categorical_cols = df.select_dtypes(include=["object", "category"]).columns
        for col in categorical_cols:
            plt.figure(figsize=(8, 6))
            sns.countplot(x=col, data=df)
            plt.title(f"Count plot for {col}", fontsize=14)
            plt.xticks(rotation=45)
            plt.show()

    except Exception as e:
        print(f"An error occurred during data exploration: {e}")
