from alignment.config import RecordingConfig
from pathlib import Path


from marker_sets.prosthetic_study_marker_set import qualisys_markers, markers_to_extract
path_to_recording = Path(r'E:\prosthetic_validation\sesh_2023-06-07_12_06_15_TF01_flexion_neutral_trial_1')

flexion_neutral_mp_config = RecordingConfig(
    recording_name= 'Mediapipe Flexion Neutral',
    path_to_recording = path_to_recording,
    path_to_freemocap_output_data = path_to_recording/'mediapipe_output_data'/'mediapipe_body_3d_xyz.npy',
    path_to_qualisys_output_data = path_to_recording/'qualisys_data'/ 'qualisys_joint_centers_3d_xyz.npy',
    qualisys_marker_list= qualisys_markers,
    markers_to_compare_list= markers_to_extract,
    frame_for_comparison= 203,
    frame_range= None
)

flexion_neutral_mp_dlc_config = RecordingConfig(
    recording_name= 'Mediapipe + DLC Flexion Neutral',
    path_to_recording = path_to_recording,
    path_to_freemocap_output_data = path_to_recording/'mediapipe_dlc_output_data'/'mediapipe_body_3d_xyz.npy',
    path_to_qualisys_output_data = path_to_recording/'qualisys_data'/ 'qualisys_joint_centers_3d_xyz.npy',
    qualisys_marker_list= qualisys_markers,
    markers_to_compare_list= markers_to_extract,
    frame_for_comparison= 203,
    frame_range= None
)

flexion_neutral_mp_yolo_dlc_config = RecordingConfig(
    recording_name= 'Mediapipe/Yolo + DLC Flexion Neutral',
    path_to_recording = path_to_recording,
    path_to_freemocap_output_data = path_to_recording/'mediapipe_yolo_dlc_output_data'/'mediapipe_body_3d_xyz.npy',
    path_to_qualisys_output_data = path_to_recording/'qualisys_data'/ 'qualisys_joint_centers_3d_xyz.npy',
    qualisys_marker_list= qualisys_markers,
    markers_to_compare_list= markers_to_extract,
    frame_for_comparison= 203,
    frame_range= None
)



if __name__ == '__main__':
    from main import main
    import numpy as np


    saved_transformation_matrix = np.load(path_to_recording/'transformation_matrix.npy')
    # saved_transformation_matrix = None
    main(flexion_neutral_mp_yolo_dlc_config,
        create_scatter_plot=False,
        save_transformation_matrix=False,
        transformation_matrix_to_use=saved_transformation_matrix)