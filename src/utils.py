from IPython.display import display
import pandas as pd


def inspect_datasets(dfs_dict):
    """
    Iterates through a dictionary of DataFrames and displays 
    shape, head, missing values, and duplicate counts for each.

    Args:
        dfs_dict (dict): A dictionary where keys are titles (str) 
                         and values are pandas DataFrames.
    """
    for title, df in dfs_dict.items():
        print(f"\n{'='*20} {title} {'='*20}")
        print(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")

        # Show only first 3 rows for a quick look
        display(df.head(3))

        # Compute missing values stats
        missing_counts = df.isnull().sum()
        missing_percent = (df.isnull().mean() * 100).round(2)

        # Create a summary dataframe for missing values
        missing_df = pd.DataFrame({
            "Missing Count": missing_counts,
            "Missing %": missing_percent
        })

        missing_df = missing_df[missing_df["Missing Count"] > 0]
        if missing_df.empty:
            print("No missing values found.")
        else:
            print("\nMissing values per column:")
            display(missing_df)

        # Compute duplicates
        duplicate_count = df.duplicated().sum()
        print(f"Duplicate rows: {duplicate_count}")

        print("-" * 60)
