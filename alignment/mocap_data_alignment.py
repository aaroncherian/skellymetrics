import numpy as np

from .markers.marker_extraction import extract_specific_markers

from .markers.markers_to_extract import markers_to_extract
from .markers.qualisys_markers import qualisys_markers
from .markers.mediapipe_markers import mediapipe_markers

from .transformations.least_squares_optimization import run_least_squares_optimization
from .transformations.apply_transformation import apply_transformation


def align_freemocap_and_qualisys_data(freemocap_data:np.ndarray, qualisys_data:np.ndarray, representative_frame):

    freemocap_representative_frame = freemocap_data[representative_frame, :, :]
    qualisys_representative_frame = qualisys_data[representative_frame, :, :]

    freemocap_extracted_frame = extract_specific_markers(data_marker_dimension=freemocap_representative_frame, list_of_markers=mediapipe_markers, markers_to_extract=markers_to_extract)
    qualisys_extracted_frame = extract_specific_markers(data_marker_dimension=qualisys_representative_frame, list_of_markers=qualisys_markers, markers_to_extract=markers_to_extract)

    transformation = run_least_squares_optimization(data_to_transform=freemocap_extracted_frame, reference_data=qualisys_extracted_frame)

    freemocap_data_transformed = apply_transformation(transformation_matrix=transformation, data_to_transform=freemocap_data)

    # plot_3d_scatter(freemocap_data_transformed, qualisys_data)

    return freemocap_data_transformed

if __name__ == "__main__":
    from pathlib import Path

    qualisys_data_path = r"D:\2023-05-17_MDN_NIH_data\1.0_recordings\calib_3\qualisys_MDN_NIH_Trial3\output_data\clipped_qualisys_skel_3d.npy"
    freemocap_data_path = r"D:\2023-05-17_MDN_NIH_data\1.0_recordings\calib_3\sesh_2023-05-17_14_53_48_MDN_NIH_Trial3\output_data\mediapipe_body_3d_xyz.npy"
    freemocap_output_folder_path = Path(r"D:\2023-05-17_MDN_NIH_data\1.0_recordings\calib_3\sesh_2023-05-17_14_53_48_MDN_NIH_Trial3\output_data")

    freemocap_data = np.load(freemocap_data_path)
    qualisys_data = np.load(qualisys_data_path)


    freemocap_data_transformed = align_freemocap_and_qualisys_data(freemocap_data=freemocap_data, qualisys_data=qualisys_data, representative_frame=800)
    # np.save(freemocap_output_folder_path/'mediapipe_body_3d_xyz_transformed.npy', freemocap_data_transformed)




    



