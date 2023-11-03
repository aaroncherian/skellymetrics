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


def main(path_to_recording_folder,freemocap_data_path,qualisys_data_path,representative_frame, qualisys_marker_list, markers_to_extract, create_scatter_plot = False):
    freemocap_databuilder = DataBuilder(path_to_data=freemocap_data_path, marker_list=mediapipe_markers)
    freemocap_data_dict = (freemocap_databuilder
                .load_data()
                .extract_common_markers(markers_to_extract=markers_to_extract)
                .convert_extracted_data_to_dataframe()
                .build())
    
    qualisys_databuilder = DataBuilder(path_to_data=qualisys_data_path, marker_list=qualisys_marker_list)
    qualisys_data_dict = (qualisys_databuilder
                .load_data()
                .extract_common_markers(markers_to_extract=markers_to_extract)
                .convert_extracted_data_to_dataframe()
                .build())
    
    # plot_3d_scatter(freemocap_data=freemocap_data_dict['extracted_data_3d_array'], qualisys_data=qualisys_data_dict['original_data_3d_array'])
    
    transformation_matrix = align_freemocap_and_qualisys_data(freemocap_data_dict['extracted_data_3d_array'],qualisys_data_dict['extracted_data_3d_array'],representative_frame)
    aligned_freemocap_data = apply_transformation(transformation_matrix=transformation_matrix, data_to_transform=freemocap_data_dict['original_data_3d_array'])
    
    aligned_freemocap_data_builder = DataBuilder(data_array=aligned_freemocap_data, marker_list=mediapipe_markers)
    aligned_freemocap_data_dict = (aligned_freemocap_data_builder
                                .extract_common_markers(markers_to_extract=markers_to_extract)
                                .convert_extracted_data_to_dataframe()
                                .build())

    if create_scatter_plot:
        plot_3d_scatter(freemocap_data=aligned_freemocap_data, qualisys_data=qualisys_data_dict['original_data_3d_array'])

    freemocap_dataframe = aligned_freemocap_data_dict['dataframe_of_extracted_3d_data']
    qualisys_dataframe = qualisys_data_dict['dataframe_of_extracted_3d_data']

    freemocap_dataframe['system'] = 'freemocap'
    qualisys_dataframe['system'] = 'qualisys'

    combined_dataframe = combine_3d_dataframes(dataframe_A=freemocap_dataframe, dataframe_B=qualisys_dataframe)


    combined_dataframe = combined_dataframe[(combined_dataframe['frame'] >= 1150) & (combined_dataframe['frame'] <= 3550)]
    error_metrics_dict = get_error_metrics(dataframe_of_3d_data=combined_dataframe)

    error_metrics_dict['absolute_error_dataframe'].to_csv(path_to_recording_folder/'output_data'/'absolute_error_dataframe.csv', index = False)
    error_metrics_dict['rmse_dataframe'].to_csv(path_to_recording_folder/'output_data'/'rmse_dataframe.csv', index = False)

    run_dash_app(dataframe_of_3d_data=combined_dataframe, rmse_dataframe=error_metrics_dict['rmse_dataframe'], absolute_error_dataframe=error_metrics_dict['absolute_error_dataframe'])

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
