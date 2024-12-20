import pandas as pd

def clean_data(df):
    """
    Cleans the input DataFrame by handling missing values, removing duplicates, 
    standardizing text, correcting data types, and dropping unnecessary columns.

    :param df: pandas DataFrame to clean.
    :return: Cleaned pandas DataFrame.
    """
    try:
        # 1. Handle Missing Values
        df = df.dropna(subset=["column_name"])  # Drop rows with missing critical values
        df["numerical_column"] = df["numerical_column"].fillna(df["numerical_column"].mean())  # Fill with mean

        # 2. Remove Duplicates
        df = df.drop_duplicates()

        # 3. Standardize Text
        if "text_column" in df.columns:
            df["text_column"] = df["text_column"].str.strip().str.lower()

        # 4. Correct Data Types
        if "date_column" in df.columns:
            df["date_column"] = pd.to_datetime(df["date_column"], errors="coerce")
        if "categorical_column" in df.columns:
            df["categorical_column"] = df["categorical_column"].astype("category")

        # 5. Handle Outliers (Example: Capping numerical values)
        if "numerical_column" in df.columns:
            upper_limit = df["numerical_column"].quantile(0.95)
            lower_limit = df["numerical_column"].quantile(0.05)
            df["numerical_column"] = df["numerical_column"].clip(lower=lower_limit, upper=upper_limit)

        # 6. Rename Columns
        df.rename(columns={"old_name": "new_name"}, inplace=True)

        # 7. Drop Unnecessary Columns
        unnecessary_columns = ["unnecessary_column"]  # Add columns to drop
        df.drop(columns=[col for col in unnecessary_columns if col in df.columns], inplace=True)

        return df

    except Exception as e:
        print(f"An error occurred during cleaning: {e}")
        return None
