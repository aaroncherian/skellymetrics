from data_utils.data_builder import DataBuilder
from data_utils.combine_3d_dataframe import combine_3d_dataframes

from alignment.mocap_data_alignment import align_freemocap_and_qualisys_data
from alignment.transformations.apply_transformation import apply_transformation

from debug_plots.scatter_3d import plot_3d_scatter

from markers.mediapipe_markers import mediapipe_markers
from markers.markers_to_extract import markers_to_extract
from markers.qualisys_markers import qualisys_markers

from error_calculations.get_error_metrics import get_error_metrics

from dash_app.run_dash_app import run_dash_app

from models.mocap_data_model import MoCapData



def main(original_freemocap_data_path,filtered_freemocap_data_path,representative_frame, recording_config, create_scatter_plot = False):
    original_freemocap_databuilder = DataBuilder(path_to_data=original_freemocap_data_path, marker_list=mediapipe_markers)
    original_freemocap_data_dict = (original_freemocap_databuilder
                .load_data()
                .extract_common_markers(markers_to_extract=markers_to_extract)
                .convert_extracted_data_to_dataframe()
                .build())
    
    filtered_freemocap_data_path = DataBuilder(path_to_data=filtered_freemocap_data_path, marker_list=mediapipe_markers)
    filtered_freemocap_data_path = (filtered_freemocap_data_path
                .load_data()
                .extract_common_markers(markers_to_extract=markers_to_extract)
                .convert_extracted_data_to_dataframe()
                .build())
    
    
    transformation_matrix = align_freemocap_and_qualisys_data(filtered_freemocap_data_path['extracted_data_3d_array'],original_freemocap_data_dict['extracted_data_3d_array'],representative_frame)
    aligned_freemocap_data = apply_transformation(transformation_matrix=transformation_matrix, data_to_transform=filtered_freemocap_data_path['original_data_3d_array'])
    
    aligned_filtered_freemocap_data_builder = DataBuilder(data_array=aligned_freemocap_data, marker_list=mediapipe_markers)
    aligned_filtered_freemocap_data_dict = (aligned_filtered_freemocap_data_builder
                                .extract_common_markers(markers_to_extract=markers_to_extract)
                                .convert_extracted_data_to_dataframe()
                                .build())

    if create_scatter_plot:
        plot_3d_scatter(freemocap_data=aligned_freemocap_data, qualisys_data=original_freemocap_data_dict['extracted_data_3d_array'])

    aligned_filtered_freemocap_dataframe = aligned_filtered_freemocap_data_dict['dataframe_of_extracted_3d_data']
    original_freemocap_dataframe = original_freemocap_data_dict['dataframe_of_extracted_3d_data']

    aligned_filtered_freemocap_dataframe['system'] = 'rigid_bones_freemocap'
    original_freemocap_dataframe['system'] = 'original_freemocap'


    combined_dataframe = combine_3d_dataframes(dataframe_A=original_freemocap_dataframe, dataframe_B=aligned_filtered_freemocap_dataframe)
    error_metrics_dict = get_error_metrics(dataframe_of_3d_data=combined_dataframe)

    position_data = MoCapData(
        joint_dataframe=combined_dataframe,
        rmse_dataframe=error_metrics_dict['rmse_dataframe'],
        absolute_error_dataframe=error_metrics_dict['absolute_error_dataframe']
    )

    velocity_data = MoCapData(
        joint_dataframe=combined_dataframe,
        rmse_dataframe=error_metrics_dict['rmse_dataframe'],
        absolute_error_dataframe=error_metrics_dict['absolute_error_dataframe']
    )


    run_dash_app(position_data_and_error=position_data, velocity_data_and_error=velocity_data, recording_config=recording_config)

    run_dash_app()
    # run_dash_app(dataframe_of_3d_data=combined_dataframe, rmse_dataframe=error_metrics_dict['rmse_dataframe'], absolute_error_dataframe=error_metrics_dict['absolute_error_dataframe'])

    f = 2 



if __name__ == '__main__':

    from pathlib import Path
    import numpy as np
    from alignment.config import RecordingConfig 

    original_freemocap_data_path = Path(r'D:\2023-05-17_MDN_NIH_data\1.0_recordings\calib_3\sesh_2023-05-17_13_48_44_MDN_treadmill_2\mediapipe_output_data\mediapipe_body_3d_xyz.npy')
    filtered_freemocap_data_path = Path(r"D:\2023-05-17_MDN_NIH_data\1.0_recordings\calib_3\sesh_2023-05-17_13_48_44_MDN_treadmill_2\mediapipe_output_data\rigid_mediapipe_body_3d_xyz.npy")
    # freemocap_output_folder_path = Path(r"D:\2023-07-26_SBT002\1.0_recordings\calib_1\reprojection_filtered\sesh_2023-07-26_14_40_40_STB002_NIH_Trial2\output_data")

    recording_config = RecordingConfig(
        recording_name= 'Rigid Bones Test',
        path_to_recording= None,
        path_to_freemocap_output_data= None,
        path_to_qualisys_output_data= None,
        qualisys_marker_list= None,
        markers_to_compare_list= None,
        frame_for_comparison= None,
        frame_range= None
    )

    main(original_freemocap_data_path=original_freemocap_data_path,filtered_freemocap_data_path=filtered_freemocap_data_path, recording_config=recording_config, representative_frame=300)
