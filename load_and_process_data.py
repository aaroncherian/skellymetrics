from markers.mediapipe_markers import mediapipe_markers
from markers.qualisys_markers import qualisys_markers
from .data_utils.data_builder import DataFrameBuilder
import pandas as pd

def load_and_process_data(path_to_freemocap_data, path_to_qualisys_data):
    """
    Load and process 3D motion capture data from FreeMoCap and Qualisys systems with just a specific set of markers

    Parameters:
    - path_to_freemocap_data (Path or str): The path to FreeMoCap 3D data file.
    - path_to_qualisys_data (Path or str): The path to Qualisys 3D data file.

    Returns:
    - combined_dataframe (pd.DataFrame): DataFrame containing the combined 3D data from both systems.
    """
    # Load and process FreeMoCap data
    freemocap_builder = DataFrameBuilder(path_to_data=path_to_freemocap_data, marker_list=mediapipe_markers)
    freemocap_data_dict = (freemocap_builder
                    .load_data()
                    .extract_common_markers(markers_to_extract=config.markers_to_extract)
                    .convert_to_dataframe(use_extracted=True)
                    .build())
    freemocap_dataframe = freemocap_data_dict['dataframe_of_3d_data']

    # Load and process Qualisys data
    qualisys_builder = DataFrameBuilder(path_to_data=path_to_qualisys_data, marker_list=qualisys_markers)
    qualisys_data_dict = (qualisys_builder
                        .load_data()
                        .extract_common_markers(markers_to_extract=config.markers_to_extract)
                        .convert_to_dataframe(use_extracted=True)
                        .build())
    qualisys_dataframe = qualisys_data_dict['dataframe_of_3d_data']

    # Add system identifier columns
    freemocap_dataframe['system'] = 'freemocap'
    qualisys_dataframe['system'] = 'qualisys'

    # Combine both dataframes
    combined_dataframe = combine_3d_dataframes(dataframe_A=freemocap_dataframe, dataframe_B=qualisys_dataframe)

    return combined_dataframe   


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