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


def main(freemocap_data_path,qualisys_data_path,representative_frame, create_scatter_plot = False):
    freemocap_databuilder = DataBuilder(path_to_data=freemocap_data_path, marker_list=mediapipe_markers)
    freemocap_data_dict = (freemocap_databuilder
                .load_data()
                .extract_common_markers(markers_to_extract=markers_to_extract)
                .convert_extracted_data_to_dataframe()
                .build())
    
    qualisys_databuilder = DataBuilder(path_to_data=qualisys_data_path, marker_list=qualisys_markers)
    qualisys_data_dict = (qualisys_databuilder
                .load_data()
                .extract_common_markers(markers_to_extract=markers_to_extract)
                .convert_extracted_data_to_dataframe()
                .build())
    
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
    error_metrics_dict = get_error_metrics(dataframe_of_3d_data=combined_dataframe)

    run_dash_app(dataframe_of_3d_data=combined_dataframe, rmse_dataframe=error_metrics_dict['rmse_dataframe'], absolute_error_dataframe=error_metrics_dict['absolute_error_dataframe'])

    f = 2 



if __name__ == '__main__':

    from pathlib import Path
    import numpy as np

    qualisys_data_path = r"D:\2023-05-17_MDN_NIH_data\1.0_recordings\calib_3\qualisys_MDN_NIH_Trial3\output_data\clipped_qualisys_skel_3d.npy"
    freemocap_data_path = r"D:\2023-05-17_MDN_NIH_data\1.0_recordings\calib_3\sesh_2023-05-17_14_53_48_MDN_NIH_Trial3\output_data\mediapipe_body_3d_xyz.npy"
    freemocap_output_folder_path = Path(r"D:\2023-05-17_MDN_NIH_data\1.0_recordings\calib_3\sesh_2023-05-17_14_53_48_MDN_NIH_Trial3\output_data")

    # freemocap_data = np.load(freemocap_data_path)

    freemocap_databuilder = DataBuilder(path_to_data=freemocap_data_path, marker_list=mediapipe_markers)
    freemocap_data_dict = (freemocap_databuilder
                    .load_data()
                    .extract_common_markers(markers_to_extract=markers_to_extract)
                    .convert_extracted_data_to_dataframe()
                    .build())


    qualisys_data = np.load(qualisys_data_path)

    main(freemocap_data_path=freemocap_data_path,qualisys_data_path=qualisys_data_path,representative_frame=800)
