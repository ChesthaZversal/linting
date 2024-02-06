def merge_two_dataframes(master_df, slave_df, on_columns):
    """
    Merges two DataFrames based on the merge column.
    It merges the dataframes in such a way that it follows the outer join in SQL.

    Args:
        master_dataframe (pd.DataFrame): First input dataframe
        slave_dataframe (pd.DataFrame): Second input datframe
        on_column (list) : Column on which the dataframes will be merged

    Returns:
        merged_df (pd.DataFrame): The merged DataFrame.
    """

    if master_df is None and slave_df is None:
        return master_df
    elif (master_df is None or len(master_df) == 0) and (
        slave_df is not None and len(slave_df) != 0
    ):
        print("Master DataFrame is None, returning Slave DataFrame.")
        return slave_df
    elif (slave_df is None or len(slave_df) == 0) and (
        master_df is not None and len(master_df) != 0
    ):
        print("Slave DataFrame is None, returning Master DataFrame.")
        return master_df
    elif master_df is not None and slave_df is not None:
        if len(master_df) == 0 and len(slave_df) == 0:
            print("Both DataFrames are not None, but both have empty lengths.")
            return master_df

    # Merge slave_df to master_df on on_column
    merged_df = master_df.merge(
        slave_df, how="outer", on=on_columns, suffixes=("", "_left")
    )

    # Remove extra columns generated with suffix "_left" in the process of merging
    merged_df = merged_df[[c for c in merged_df.columns if not c.endswith("_left")]]

    return merged_df
