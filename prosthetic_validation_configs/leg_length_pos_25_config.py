from alignment.config import RecordingConfig
from pathlib import Path


from marker_sets.prosthetic_study_marker_set import qualisys_markers, markers_to_extract
path_to_recording = Path(r'D:\2023-06-07_TF01\1.0_recordings\treadmill_calib\sesh_2023-06-07_12_50_56_TF01_leg_length_pos_25_trial_1')

#standard mediapipe with dlc
leg_length_pos_25_mp_dlc_config = RecordingConfig(
    recording_name= 'Mediaipipe + DLC, +.25in leg length',
    path_to_recording = path_to_recording,
    path_to_freemocap_output_data = path_to_recording/'mediapipe_dlc_output_data'/'mediapipe_body_3d_xyz.npy',
    path_to_qualisys_output_data = path_to_recording/'qualisys_data'/ 'qualisys_joint_centers_3d_xyz.npy',
    qualisys_marker_list= qualisys_markers,
    markers_to_compare_list= markers_to_extract,
    frame_for_comparison= 220,
    frame_range= None
)

#yolo'd mediapipe with dlc
leg_length_pos_25_mp_yolo_dlc_config = RecordingConfig(
    recording_name= 'Mediaipipe/YOLO + DLC, +.25in leg length',
    path_to_recording = path_to_recording,
    path_to_freemocap_output_data = path_to_recording/'mediapipe_yolo_dlc_output_data'/'mediapipe_body_3d_xyz.npy',
    path_to_qualisys_output_data = path_to_recording/'qualisys_data'/ 'qualisys_joint_centers_3d_xyz.npy',
    qualisys_marker_list= qualisys_markers,
    markers_to_compare_list= markers_to_extract,
    frame_for_comparison= 220,
    frame_range= None

)

leg_length_pos_25_rigid_mp_dlc_config = RecordingConfig(
    recording_name= 'Mediaipipe/YOLO + DLC, +.25in leg length',
    path_to_recording = path_to_recording,
    path_to_freemocap_output_data = path_to_recording/'rigid_mediapipe_dlc_output_data'/'mediapipe_body_3d_xyz.npy',
    path_to_qualisys_output_data = path_to_recording/'qualisys_data'/ 'qualisys_joint_centers_3d_xyz.npy',
    qualisys_marker_list= qualisys_markers,
    markers_to_compare_list= markers_to_extract,
    frame_for_comparison= 220,
    frame_range= None

)


if __name__ == '__main__':
    from main import main
    import numpy as np
    
    saved_transformation_matrix = np.load(path_to_recording/'transformation_matrix.npy')
    # saved_transformation_matrix = None
    main(leg_length_pos_25_rigid_mp_dlc_config,
        create_scatter_plot=False,
        save_transformation_matrix=False,
        transformation_matrix_to_use=saved_transformation_matrix)