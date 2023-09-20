import numpy as np


from .transformations.least_squares_optimization import run_least_squares_optimization
from .transformations.apply_transformation import apply_transformation


def align_freemocap_and_qualisys_data(freemocap_data: np.ndarray, qualisys_data: np.ndarray, representative_frame):
    """
    Align FreeMoCap and Qualisys data using a representative frame and least squares optimization. FreeMoCap and Qualisys data should come in with the same number of markers, in the same order.

    Parameters:
    - freemocap_data (numpy.ndarray): 3D array of FreeMoCap data of shape (num_frames, num_markers, 3).
    - qualisys_data (numpy.ndarray): 3D array of Qualisys data of shape (num_frames, num_markers, 3).
    - representative_frame (int): Index of the frame to be used for alignment.

    Returns:
    - freemocap_data_transformed (numpy.ndarray): Aligned FreeMoCap data.
    """

    if freemocap_data.shape[1] != qualisys_data.shape[1]:
        raise ValueError("The number of markers in freemocap_data and qualisys_data must be the same.")
 

    freemocap_representative_frame = freemocap_data[representative_frame, :, :]
    qualisys_representative_frame = qualisys_data[representative_frame, :, :]

    transformation_matrix = run_least_squares_optimization(
        data_to_transform=freemocap_representative_frame, 
        reference_data=qualisys_representative_frame
    )

    # freemocap_data_transformed = apply_transformation(
    #     transformation_matrix=transformation, 
    #     data_to_transform=freemocap_data
    # )

    return transformation_matrix

if __name__ == "__main__":
    from pathlib import Path

    qualisys_data_path = r"D:\2023-05-17_MDN_NIH_data\1.0_recordings\calib_3\qualisys_MDN_NIH_Trial3\output_data\clipped_qualisys_skel_3d.npy"
    freemocap_data_path = r"D:\2023-05-17_MDN_NIH_data\1.0_recordings\calib_3\sesh_2023-05-17_14_53_48_MDN_NIH_Trial3\output_data\mediapipe_body_3d_xyz.npy"
    freemocap_output_folder_path = Path(r"D:\2023-05-17_MDN_NIH_data\1.0_recordings\calib_3\sesh_2023-05-17_14_53_48_MDN_NIH_Trial3\output_data")

    freemocap_data = np.load(freemocap_data_path)
    qualisys_data = np.load(qualisys_data_path)


    freemocap_data_transformed = align_freemocap_and_qualisys_data(freemocap_data=freemocap_data, qualisys_data=qualisys_data, representative_frame=800)
    # np.save(freemocap_output_folder_path/'mediapipe_body_3d_xyz_transformed.npy', freemocap_data_transformed)




    



