import pandas as pd
def combine_3d_dataframes(dataframe_A, dataframe_B):
    """
    Combine two dataframes containing 3D motion capture data.

    Parameters:
    - dataframe_A (pd.DataFrame): The first dataframe to be combined.
    - dataframe_B (pd.DataFrame): The second dataframe to be combined.

    Returns:
    - pd.DataFrame: A combined dataframe.
    """
    return pd.concat([dataframe_A, dataframe_B], ignore_index=True)