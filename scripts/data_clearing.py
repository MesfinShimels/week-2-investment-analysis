import pandas as pd
import numpy as np

def clean_large_dataframe(df):
    """
    Cleans a large DataFrame by:
    1. Removing duplicate rows.
    2. Filling missing numeric values with the column mean.
    3. Filling missing categorical values with the mode.
    
    Parameters:
        df (pd.DataFrame): The DataFrame to clean.
    
    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    # Remove duplicate rows
    df_cleaned = df.drop_duplicates()

    # Handle missing numeric values: Replace with column mean
    numeric_cols = df_cleaned.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        mean_value = df_cleaned[col].mean()
        df_cleaned[col].fillna(mean_value, inplace=True)

    # Handle missing categorical values: Replace with column mode
    categorical_cols = df_cleaned.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        mode_value = df_cleaned[col].mode()[0] if not df_cleaned[col].mode().empty else "Unknown"
        df_cleaned[col].fillna(mode_value, inplace=True)
    
    return df_cleaned