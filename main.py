from data_utils.data_builder import DataBuilder
from data_utils.combine_3d_dataframe import combine_3d_dataframes

from alignment.mocap_data_alignment import align_freemocap_and_qualisys_data
from alignment.transformations.apply_transformation import apply_transformation

from debug_plots.scatter_3d import plot_3d_scatter

from markers.mediapipe_markers import mediapipe_markers
# from markers.markers_to_extract import markers_to_extract
# from markers.qualisys_markers import qualisys_markers

from error_calculations.get_error_metrics import get_error_metrics

from dash_app.run_dash_app import run_dash_app

def calculate_velocity(data_3d_array):
    return np.diff(data_3d_array, axis=0)

def prepare_data_builder(path_to_data, marker_list, markers_to_extract):
    databuilder = DataBuilder(path_to_data=path_to_data, marker_list=marker_list)
    return (databuilder.load_data()
            .extract_common_markers(markers_to_extract=markers_to_extract)
            .convert_extracted_data_to_dataframe()
            .build())

def get_aligned_data(freemocap_data, qualisys_data, representative_frame):
    transformation_matrix = align_freemocap_and_qualisys_data(freemocap_data['extracted_data_3d_array'],
                                                              qualisys_data['extracted_data_3d_array'],
                                                              representative_frame)
    return apply_transformation(transformation_matrix, freemocap_data['original_data_3d_array'])

def save_error_metrics_to_csv(error_metrics_dict, path, prefix):
    error_metrics_dict['absolute_error_dataframe'].to_csv(path / f'{prefix}_absolute_error_dataframe.csv', index=False)
    error_metrics_dict['rmse_dataframe'].to_csv(path / f'{prefix}_rmse_dataframe.csv', index=False)

def process_and_save_data(freemocap_data_path, qualisys_data_path, representative_frame, qualisys_marker_list, markers_to_extract, path_to_recording_folder, create_scatter_plot=False):
    freemocap_position_data = prepare_data_builder(freemocap_data_path, mediapipe_markers, markers_to_extract)
    qualisys_position_data = prepare_data_builder(qualisys_data_path, qualisys_marker_list, markers_to_extract)

    aligned_freemocap_data = get_aligned_data(freemocap_position_data, qualisys_position_data, representative_frame)

    qualisys_velocity_data = calculate_velocity(qualisys_position_data['original_data_3d_array'])
    freemocap_velocity_data = calculate_velocity(aligned_freemocap_data)

    combined_position_dataframe = combine_and_filter_dataframes(freemocap_position_data['dataframe_of_extracted_3d_data'],
                                                                qualisys_position_data['dataframe_of_extracted_3d_data'])
    position_error_metrics = get_error_metrics(combined_position_dataframe)
    save_error_metrics_to_csv(position_error_metrics, path_to_recording_folder, 'position')

    combined_velocity_dataframe = combine_and_filter_dataframes(freemocap_velocity_data, qualisys_velocity_data)
    velocity_error_metrics = get_error_metrics(combined_velocity_dataframe)
    save_error_metrics_to_csv(velocity_error_metrics, path_to_recording_folder, 'velocity')

    if create_scatter_plot:
        plot_3d_scatter(aligned_freemocap_data, qualisys_position_data['original_data_3d_array'])

def get_data_arrays_and_dataframes( marker_list, markers_to_extract, path_to_data = None, data_array = None):
    """
    Loads the data from the specified path and returns a DataBuilder object after extracting the common markers and converting the data to a DataFrame.
    Returns:
    A dictionary with the original data array, extracted data array with just the common markers, and dataframes for the extracted data
    """

    if path_to_data is None and data_array is None:
        raise ValueError("Either path_to_data or data_array must be provided.")
    elif path_to_data is not None:
        print(f"Loading data from {path_to_data}.")
        run_method = 'load_from_path'
    elif data_array is not None:
        print(f"Loading data from array.")
        run_method = 'load_from_array'

    match run_method:
        case 'load_from_path':
            databuilder = DataBuilder(path_to_data=path_to_data, marker_list=marker_list)
            return (databuilder.load_data()
                .extract_common_markers(markers_to_extract=markers_to_extract)
                .convert_extracted_data_to_dataframe()
                .build())
        case 'load_from_array':
            databuilder = DataBuilder(data_array=data_array, marker_list=marker_list)
            return (databuilder
                .extract_common_markers(markers_to_extract=markers_to_extract)
                .convert_extracted_data_to_dataframe()
                .build())

def calculate_velocity(data_dictionary):
    """
    Calculates the velocity from the data dictionary that is returned from the DataBuilder object 
    """
    return np.diff(data_dictionary['original_data_3d_array'], axis = 0)

def combine_and_filter_dataframes(freemocap_dataframe, qualisys_dataframe):
    freemocap_dataframe['system'] = 'freemocap'
    qualisys_dataframe['system'] = 'qualisys'
    combined_dataframe = combine_3d_dataframes(dataframe_A=freemocap_dataframe, dataframe_B=qualisys_dataframe)
    return combined_dataframe


def main(path_to_recording_folder,freemocap_data_path,qualisys_data_path,representative_frame, qualisys_marker_list, markers_to_extract, create_scatter_plot = False):
    
    #create a dictionary of the original data, extracted data, and dataframes for the position data for both systems
    freemocap_position_dict = get_data_arrays_and_dataframes(marker_list=mediapipe_markers, markers_to_extract=markers_to_extract, path_to_data=freemocap_data_path)
    qualisys_position_dict = get_data_arrays_and_dataframes(marker_list=qualisys_marker_list, markers_to_extract=markers_to_extract, path_to_data=qualisys_data_path)

    #create a dictionary of the original data, extracted data, and dataframes for the velocity data for qualisys (we'll calculate the velocity for freemocap after its been aligned)
    qualisys_velocity_array = calculate_velocity(data_dictionary=qualisys_position_dict)
    qualisys_velocity_dict = get_data_arrays_and_dataframes(marker_list=qualisys_marker_list, markers_to_extract=markers_to_extract, data_array=qualisys_velocity_array)

    #align the freemocap data to the qualisys data
    transformation_matrix = align_freemocap_and_qualisys_data(freemocap_position_dict['extracted_data_3d_array'],qualisys_position_dict['extracted_data_3d_array'],representative_frame)
    aligned_freemocap_position_data = apply_transformation(transformation_matrix=transformation_matrix, data_to_transform=freemocap_position_dict['original_data_3d_array'])

    #create a dictionary of the original data, extracted data, and dataframes for the velocity data for newly aligned freemocap data
    aligned_freemocap_position_dict = get_data_arrays_and_dataframes(marker_list=mediapipe_markers, markers_to_extract=markers_to_extract, data_array=aligned_freemocap_position_data)
    aligned_freemocap_velocity_array = calculate_velocity(data_dictionary=aligned_freemocap_position_dict)
    aligned_freemocap_velocity_dict = get_data_arrays_and_dataframes(marker_list=mediapipe_markers, markers_to_extract=markers_to_extract, data_array=aligned_freemocap_velocity_array)


    # plot_3d_scatter(freemocap_data=freemocap_data_dict['extracted_data_3d_array'], qualisys_data=qualisys_data_dict['original_data_3d_array'])
    if create_scatter_plot:
        plot_3d_scatter(freemocap_data=aligned_freemocap_position_data, qualisys_data=qualisys_position_dict['original_data_3d_array'])

    combined_position_dataframe = combine_and_filter_dataframes(freemocap_dataframe=aligned_freemocap_position_dict['dataframe_of_extracted_3d_data'], qualisys_dataframe=qualisys_position_dict['dataframe_of_extracted_3d_data'])
    combined_position_dataframe = combined_position_dataframe[(combined_position_dataframe['frame'] >= 1150) & (combined_position_dataframe['frame'] <= 3550)]
    position_error_metrics_dict = get_error_metrics(dataframe_of_3d_data=combined_position_dataframe)
    position_error_metrics_dict['absolute_error_dataframe'].to_csv(path_to_recording_folder/'output_data'/'position_absolute_error_dataframe.csv', index = False)
    position_error_metrics_dict['rmse_dataframe'].to_csv(path_to_recording_folder/'output_data'/'position_rmse_dataframe.csv', index = False)


    combined_velocity_dataframe = combine_and_filter_dataframes(freemocap_dataframe=aligned_freemocap_velocity_dict['dataframe_of_extracted_3d_data'], qualisys_dataframe=qualisys_velocity_dict['dataframe_of_extracted_3d_data'])
    combined_velocity_dataframe = combined_velocity_dataframe[(combined_velocity_dataframe['frame'] >= 1150) & (combined_velocity_dataframe['frame'] <= 3550)]
    velocity_error_metrics_dict = get_error_metrics(dataframe_of_3d_data=combined_velocity_dataframe)
    velocity_error_metrics_dict['absolute_error_dataframe'].to_csv(path_to_recording_folder/'output_data'/'velocity_absolute_error_dataframe.csv', index = False)
    velocity_error_metrics_dict['rmse_dataframe'].to_csv(path_to_recording_folder/'output_data'/'velocity_rmse_dataframe.csv', index = False)


    run_dash_app(dataframe_of_3d_data=combined_position_dataframe, rmse_dataframe=position_error_metrics_dict['rmse_dataframe'], absolute_error_dataframe=position_error_metrics_dict['absolute_error_dataframe'])

    f = 2 



if __name__ == '__main__':

    from pathlib import Path
    import numpy as np
    # from markers.qualisys_markers import qualisys_markers

    #prosthetic data
    # path_to_recording_folder = Path(r"D:\2023-06-07_TF01\1.0_recordings\treadmill_calib\sesh_2023-06-07_12_06_15_TF01_flexion_neutral_trial_1")
    # qualisys_markers = [
    #     'right_hip',
    #     'left_hip',
    #     'right_knee',
    #     'left_knee',
    #     'right_ankle',
    #     'left_ankle',
    #     'right_heel',
    #     'left_heel',
    #     'right_foot_index',
    #     'left_foot_index',
    # ]

    # markers_to_extract = [
    #     'right_hip',
    #     'left_hip',
    #     'right_knee',
    #     'left_knee',
    #     'right_ankle',
    #     'left_ankle',
    #     'right_heel',
    #     'left_heel',
    #     'right_foot_index',
    #     'left_foot_index',
    # ]

    #full body treadmill data
    path_to_recording_folder = Path(r"D:\2023-05-17_MDN_NIH_data\1.0_recordings\calib_3\sesh_2023-05-17_13_48_44_MDN_treadmill_2")
    from markers.markers_to_extract import markers_to_extract
    qualisys_markers = [
        'head',
        'right_shoulder',
        'left_shoulder',
        'right_elbow',
        'left_elbow',
        'right_wrist',
        'left_wrist',
        'right_hand',
        'left_hand',
        'right_hip',
        'left_hip',
        'right_knee',
        'left_knee',
        'right_ankle',
        'left_ankle',
        'right_heel',
        'left_heel',
        'right_foot_index',
        'left_foot_index',
    ]
        



    freemocap_data_path = path_to_recording_folder/'output_data'/'mediapipe_body_3d_xyz.npy'
    qualisys_data_path = path_to_recording_folder/'qualisys'/'qualisys_joint_centers_3d_xyz.npy'
    freemocap_output_folder_path = path_to_recording_folder/'output_data'

    # qualisys_data_path = r"D:\2023-06-07_TF01\1.0_recordings\treadmill_calib\sesh_2023-06-07_12_06_15_TF01_flexion_neutral_trial_1\qualisys\qualisys_joint_centers_3d_xyz.npy"
    # freemocap_data_path = r"D:\2023-06-07_TF01\1.0_recordings\treadmill_calib\sesh_2023-06-07_12_06_15_TF01_flexion_neutral_trial_1\qualisys\qualisys_joint_centers_3d_xyz.npy"
    # freemocap_output_folder_path = Path(r"D:\2023-06-07_TF01\1.0_recordings\treadmill_calib\sesh_2023-06-07_12_06_15_TF01_flexion_neutral_trial_1\output_data")

    freemocap_data = np.load(freemocap_data_path)
    qualisys_data = np.load(qualisys_data_path)


    freemocap_data_transformed = main(path_to_recording_folder=path_to_recording_folder, freemocap_data_path=freemocap_data_path, qualisys_data_path=qualisys_data_path, representative_frame=800, qualisys_marker_list=qualisys_markers, markers_to_extract=markers_to_extract, create_scatter_plot=False)
