from dataclasses import dataclass
import pandas as pd

@dataclass
class MoCapData:
    joint_dataframe: pd.DataFrame
    rmse_dataframe: pd.DataFrame
    absolute_error_dataframe: pd.DataFrame
