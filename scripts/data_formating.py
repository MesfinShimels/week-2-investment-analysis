import pandas as pd

def format_data(df):
    """
    Formats the input DataFrame by correcting data types, standardizing formats, 
    and performing text and numerical formatting.

    :param df: pandas DataFrame to format.
    :return: Formatted pandas DataFrame.
    """
    try:
        # 1. Convert Columns to Correct Data Types
        if "date_column" in df.columns:
            df["date_column"] = pd.to_datetime(df["date_column"], errors="coerce")  # Convert to datetime
        
        if "numerical_column" in df.columns:
            df["numerical_column"] = pd.to_numeric(df["numerical_column"], errors="coerce")  # Convert to numeric

        # 2. Standardize Date Format (if a date column exists)
        if "date_column" in df.columns:
            df["date_column"] = df["date_column"].dt.strftime('%Y-%m-%d')  # Standardize date format

        # 3. Text Formatting (Trim whitespaces, convert to lowercase)
        if "text_column" in df.columns:
            df["text_column"] = df["text_column"].str.strip().str.lower()  # Trim spaces and lowercase text
        
        # 4. Handle Categorical Data
        if "categorical_column" in df.columns:
            df["categorical_column"] = df["categorical_column"].astype("category")  # Convert to category type

        # 5. Format Numerical Columns (e.g., with thousands separator or 2 decimal places)
        if "numerical_column" in df.columns:
            df["numerical_column"] = df["numerical_column"].apply(lambda x: f"{x:,.2f}")  # Format with 2 decimals

        # 6. Remove Unnecessary Columns (if any)
        unnecessary_columns = ["unnecessary_column"]  # Add any columns you wish to remove
        df.drop(columns=[col for col in unnecessary_columns if col in df.columns], inplace=True)

        return df

    except Exception as e:
        print(f"An error occurred during data formatting: {e}")
        return None
