import matplotlib.pyplot as plt
import seaborn as sns

def plot_xdr_sessions(df):
    """
    Plots the number of xDR sessions (proxy: Activity Duration DL) for each application.
    """
    data = df.groupby('Handset Type')['Activity Duration DL (ms)'].sum().sort_values(ascending=False)
    top_10_data = data.head(10)  # Ensure top 10 selection
    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_10_data.index, y=top_10_data.values, palette="viridis")
    plt.title("Number of xDR Sessions per Application (Top 10)", fontsize=16)
    plt.xlabel("Handset Type", fontsize=12)
    plt.ylabel("Activity Duration DL (ms)", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def plot_session_duration(df):
    """
    Plots session duration for each application.
    """
    data = df.groupby('Handset Type')['Dur. (ms)'].sum().sort_values(ascending=False)
    top_10_data = data.head(10)  # Ensure top 10 selection
    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_10_data.index, y=top_10_data.values, palette="coolwarm")
    plt.title("Session Duration per Application (Top 10)", fontsize=16)
    plt.xlabel("Handset Type", fontsize=12)
    plt.ylabel("Duration (ms)", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def plot_dl_ul_data(df):
    """
    Plots total download (DL) and upload (UL) data for each application.
    """
    data = df.groupby('Handset Type')[['Total DL (Bytes)', 'Total UL (Bytes)']].sum()
    top_10_data = data.sort_values(by='Total DL (Bytes)', ascending=False).head(10)
    # Stacked bar chart: Sum of DL and UL
    top_10_data.plot(kind='bar', stacked=True, figsize=(12, 6), colormap="cividis")
    plt.title("Total DL and UL Data per Application (Top 10)", fontsize=16)
    plt.xlabel("Handset Type", fontsize=12)
    plt.ylabel("Data Volume (Bytes)", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def plot_total_data_volume(df):
    """
    Plots total data volume (DL + UL) for each application.
    """
    df['Total Data Volume (Bytes)'] = df['Total DL (Bytes)'] + df['Total UL (Bytes)']
    data = df.groupby('Handset Type')['Total Data Volume (Bytes)'].sum().sort_values(ascending=False)
    top_10_data = data.head(10)  # Ensure top 10 selection
    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_10_data.index, y=top_10_data.values, palette="viridis")
    plt.title("Total Data Volume per Application (Top 10)", fontsize=16)
    plt.xlabel("Handset Type", fontsize=12)
    plt.ylabel("Total Data Volume (Bytes)", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def plot_top_10_handsets(df):
    """
    Plots the top 10 handsets used by customers.
    """
    data = df['Handset Type'].value_counts().head(10)
    plt.figure(figsize=(12, 6))
    sns.barplot(x=data.index, y=data.values, palette="magma")
    plt.title("Top 10 Handsets", fontsize=16)
    plt.xlabel("Handset Type", fontsize=12)
    plt.ylabel("Count", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def plot_top_3_manufacturers(df):
    """
    Plots the top 3 handset manufacturers based on usage.
    """
    data = df['Handset Manufacturer'].value_counts().head(3)
    plt.figure(figsize=(8, 5))
    sns.barplot(x=data.index, y=data.values, palette="cool")
    plt.title("Top 3 Handset Manufacturers", fontsize=16)
    plt.xlabel("Handset Manufacturer", fontsize=12)
    plt.ylabel("Count", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


import pandas as pd

def clean_and_aggregate(df):
    """
    Ensures that the relevant columns are numeric and handles missing data.
    """
    # List of columns that should be numeric for aggregation
    numeric_columns = [
        'Dur. (ms)', 'Activity Duration DL (ms)', 'Activity Duration UL (ms)', 
        'Avg RTT DL (ms)', 'Avg RTT UL (ms)', 'Avg Bearer TP DL (kbps)', 
        'Avg Bearer TP UL (kbps)', 'TCP DL Retrans. Vol (Bytes)', 
        'TCP UL Retrans. Vol (Bytes)', 'HTTP DL (Bytes)', 'HTTP UL (Bytes)', 
        'Social Media DL (Bytes)', 'Social Media UL (Bytes)', 'Google DL (Bytes)', 
        'Google UL (Bytes)', 'Email DL (Bytes)', 'Email UL (Bytes)', 
        'Youtube DL (Bytes)', 'Youtube UL (Bytes)', 'Netflix DL (Bytes)', 
        'Netflix UL (Bytes)', 'Gaming DL (Bytes)', 'Gaming UL (Bytes)', 
        'Other DL (Bytes)', 'Other UL (Bytes)', 'Total UL (Bytes)', 'Total DL (Bytes)'
    ]
    
    # Convert all relevant columns to numeric, setting errors='coerce' to handle non-numeric values
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors='coerce')
    
    # Drop rows with NaN values in any of the numeric columns
    df_cleaned = df.dropna(subset=numeric_columns)
    
    return df_cleaned

def plot_xdr_sessions(df):
    """
    Plots the number of xDR sessions (proxy: Activity Duration DL) for each application.
    """
    df_cleaned = clean_and_aggregate(df)  # Clean the data before plotting
    data = df_cleaned.groupby('Handset Type')['Activity Duration DL (ms)'].sum().sort_values(ascending=False)
    top_10_data = data.head(10)
    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_10_data.index, y=top_10_data.values, palette="viridis")
    plt.title("Number of xDR Sessions per Application (Top 10)", fontsize=16)
    plt.xlabel("Handset Type", fontsize=12)
    plt.ylabel("Activity Duration DL (ms)", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# Example for another plot:
def plot_session_duration(df):
    """
    Plots session duration for each application.
    """
    df_cleaned = clean_and_aggregate(df)  # Clean the data before plotting
    data = df_cleaned.groupby('Handset Type')['Dur. (ms)'].sum().sort_values(ascending=False)
    top_10_data = data.head(10)
    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_10_data.index, y=top_10_data.values, palette="coolwarm")
    plt.title("Session Duration per Application (Top 10)", fontsize=16)
    plt.xlabel("Handset Type", fontsize=12)
    plt.ylabel("Duration (ms)", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# Add similar cleaning steps for other plotting functions...
