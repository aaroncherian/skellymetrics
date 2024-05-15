from data_utils.data_builder import DataBuilder
from data_utils.combine_3d_dataframe import combine_3d_dataframes

from alignment.mocap_data_alignment import align_freemocap_and_qualisys_data_ransac  # Updated import
from alignment.transformations.apply_transformation import apply_transformation

from debug_plots.scatter_3d import plot_3d_scatter

from markers.mediapipe_markers import mediapipe_markers

from error_calculations.get_error_metrics import get_error_metrics

from dash_app.run_dash_app import run_dash_app
from models.mocap_data_model import MoCapData
from alignment.config import RecordingConfig
import numpy as np

def calculate_velocity(data_3d_array):
    return np.diff(data_3d_array, axis=0)

def prepare_data_builder(path_to_data, marker_list, markers_to_extract):
    databuilder = DataBuilder(path_to_data=path_to_data, marker_list=marker_list)
    return (databuilder.load_data()
            .extract_common_markers(markers_to_extract=markers_to_extract)
            .convert_extracted_data_to_dataframe()
            .build())

def get_aligned_data(freemocap_data, qualisys_data, frames_to_sample=100, initial_guess=[0,0,0,0,0,0,1], max_iterations=1000, inlier_threshold=0.5):
    best_transformation_matrix = align_freemocap_and_qualisys_data_ransac(
        freemocap_data['extracted_data_3d_array'],
        qualisys_data['extracted_data_3d_array'],
        frames_to_sample=frames_to_sample,
        initial_guess=initial_guess,
        max_iterations=max_iterations,
        inlier_threshold=inlier_threshold
    )

    aligned_freemocap_data = apply_transformation(best_transformation_matrix, freemocap_data['original_data_3d_array'])
    return aligned_freemocap_data

def save_error_metrics_to_csv(error_metrics_dict, path, prefix):
    error_metrics_dict['absolute_error_dataframe'].to_csv(path / f'{prefix}_absolute_error_dataframe.csv', index=False)
    error_metrics_dict['rmse_dataframe'].to_csv(path / f'{prefix}_rmse_dataframe.csv', index=False)

def process_and_save_data(freemocap_data_path, qualisys_data_path, frames_to_sample, qualisys_marker_list, markers_to_extract, path_to_recording_folder, create_scatter_plot=False):
    freemocap_position_data = prepare_data_builder(freemocap_data_path, mediapipe_markers, markers_to_extract)
    qualisys_position_data = prepare_data_builder(qualisys_data_path, qualisys_marker_list, markers_to_extract)

    aligned_freemocap_data = get_aligned_data(
        freemocap_position_data, 
        qualisys_position_data,
        frames_to_sample=frames_to_sample
    )

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

def get_data_arrays_and_dataframes(marker_list, markers_to_extract, path_to_data=None, data_array=None):
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
    return np.diff(data_dictionary['original_data_3d_array'], axis=0)

def combine_and_filter_dataframes(freemocap_dataframe, qualisys_dataframe):
    freemocap_dataframe['system'] = 'freemocap'
    qualisys_dataframe['system'] = 'qualisys'
    combined_dataframe = combine_3d_dataframes(dataframe_A=freemocap_dataframe, dataframe_B=qualisys_dataframe)
    return combined_dataframe

def main(recording_config: RecordingConfig, create_scatter_plot=False, save_transformation_matrix=False, transformation_matrix_to_use=None):
    freemocap_position_dict = get_data_arrays_and_dataframes(
        marker_list=mediapipe_markers,
        markers_to_extract=recording_config.markers_to_compare_list,
        path_to_data=recording_config.path_to_freemocap_output_data
    )
    qualisys_position_dict = get_data_arrays_and_dataframes(
        marker_list=recording_config.qualisys_marker_list,
        markers_to_extract=recording_config.markers_to_compare_list,
        path_to_data=recording_config.path_to_qualisys_output_data
    )

    qualisys_velocity_array = calculate_velocity(qualisys_position_dict)
    qualisys_velocity_dict = get_data_arrays_and_dataframes(
        marker_list=recording_config.qualisys_marker_list,
        markers_to_extract=recording_config.markers_to_compare_list,
        data_array=qualisys_velocity_array
    )

    if transformation_matrix_to_use is None:
        aligned_freemocap_position_data = get_aligned_data(
            freemocap_position_dict,
            qualisys_position_dict,
            frames_to_sample=recording_config.frames_to_sample,
            max_iterations=recording_config.max_iterations,
            inlier_threshold=recording_config.inlier_threshold
        )
        # print('Transformation matrix: ', transformation_matrix)
    else:
        aligned_freemocap_position_data = apply_transformation(
            transformation_matrix=transformation_matrix_to_use,
            data=freemocap_position_dict['original_data_3d_array']
        )
        print('Transformation matrix: ', transformation_matrix_to_use)

    # if save_transformation_matrix:
    #     np.save(recording_config.path_to_recording / 'transformation_matrix.npy', transformation_matrix)

    aligned_freemocap_position_dict = get_data_arrays_and_dataframes(
        marker_list=mediapipe_markers,
        markers_to_extract=recording_config.markers_to_compare_list,
        data_array=aligned_freemocap_position_data
    )
    aligned_freemocap_velocity_array = calculate_velocity(aligned_freemocap_position_dict)
    aligned_freemocap_velocity_dict = get_data_arrays_and_dataframes(
        marker_list=mediapipe_markers,
        markers_to_extract=recording_config.markers_to_compare_list,
        data_array=aligned_freemocap_velocity_array
    )

    if create_scatter_plot:
        plot_3d_scatter(
            freemocap_data=aligned_freemocap_position_data,
            qualisys_data=qualisys_position_dict['original_data_3d_array']
        )

    start_frame, end_frame = recording_config.frame_range if recording_config.frame_range else (None, None)

    path_to_save_csvs = recording_config.path_to_freemocap_output_data.parent / 'metrics'
    path_to_save_csvs.mkdir(parents=True, exist_ok=True)

    combined_position_dataframe = combine_and_filter_dataframes(
        freemocap_dataframe=aligned_freemocap_position_dict['dataframe_of_extracted_3d_data'],
        qualisys_dataframe=qualisys_position_dict['dataframe_of_extracted_3d_data']
    )

    if start_frame is not None:
        combined_position_dataframe = combined_position_dataframe[combined_position_dataframe['frame'] >= start_frame]
    if end_frame is not None:
        combined_position_dataframe = combined_position_dataframe[combined_position_dataframe['frame'] <= end_frame]

    position_error_metrics_dict = get_error_metrics(dataframe_of_3d_data=combined_position_dataframe)
    # position_error_metrics_dict['absolute_error_dataframe'].to_csv(path_to_save_csvs / 'position_absolute_error_dataframe.csv', index=False)
    # position_error_metrics_dict['rmse_dataframe'].to_csv(path_to_save_csvs / 'position_rmse_dataframe.csv', index=False)

    combined_velocity_dataframe = combine_and_filter_dataframes(
        freemocap_dataframe=aligned_freemocap_velocity_dict['dataframe_of_extracted_3d_data'],
        qualisys_dataframe=qualisys_velocity_dict['dataframe_of_extracted_3d_data']
    )

    if start_frame is not None:
        combined_velocity_dataframe = combined_velocity_dataframe[combined_velocity_dataframe['frame'] >= start_frame]
    if end_frame is not None:
        combined_velocity_dataframe = combined_velocity_dataframe[combined_velocity_dataframe['frame'] <= end_frame]

    velocity_error_metrics_dict = get_error_metrics(dataframe_of_3d_data=combined_velocity_dataframe)
    # velocity_error_metrics_dict['absolute_error_dataframe'].to_csv(path_to_save_csvs / 'velocity_absolute_error_dataframe.csv', index=False)
    # velocity_error_metrics_dict['rmse_dataframe'].to_csv(path_to_save_csvs / 'velocity_rmse_dataframe.csv', index=False)

    # aligned_freemocap_position_dict['dataframe_of_extracted_3d_data'].to_csv(path_to_save_csvs / 'freemocap_position_data.csv', index=False)
    # qualisys_position_dict['dataframe_of_extracted_3d_data'].to_csv(path_to_save_csvs / 'qualisys_position_data.csv', index=False)

    position_data = MoCapData(
        joint_dataframe=combined_position_dataframe,
        rmse_dataframe=position_error_metrics_dict['rmse_dataframe'],
        absolute_error_dataframe=position_error_metrics_dict['absolute_error_dataframe']
    )

    velocity_data = MoCapData(
        joint_dataframe=combined_velocity_dataframe,
        rmse_dataframe=velocity_error_metrics_dict['rmse_dataframe'],
        absolute_error_dataframe=velocity_error_metrics_dict['absolute_error_dataframe']
    )

    run_dash_app(position_data, velocity_data, recording_config)


if __name__ == '__main__':
    from pathlib import Path
    import numpy as np

    saved_transformation_matrix = None

    from prosthetic_validation_configs.leg_length_neg_5_configs import leg_length_neg_5_mp_dlc_config

    freemocap_data_transformed = main(
        recording_config=leg_length_neg_5_mp_dlc_config,
        create_scatter_plot=False, 
        save_transformation_matrix=True, 
        transformation_matrix_to_use=saved_transformation_matrix
    )
