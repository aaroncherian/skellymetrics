from alignment.config import RecordingConfig
from pathlib import Path


from marker_sets.MDN_validation_marker_set import qualisys_markers, markers_to_extract
path_to_recording = Path(r"D:\2023-05-17_MDN_NIH_data\1.0_recordings\calib_3\mediapipe_MDN_Trial_2_yolo")

mdn_nih_trial_2_mediapipe_config = RecordingConfig(
    recording_name= 'MDN NIH Trial 2 Mediapipe',
    path_to_recording = path_to_recording,
    path_to_freemocap_output_data = path_to_recording/'mediapipe_output_data'/'mediapipe_body_3d_xyz.npy',
    path_to_qualisys_output_data = path_to_recording/'qualisys_data'/ 'qualisys_joint_centers_3d_xyz.npy',
    qualisys_marker_list= qualisys_markers,
    markers_to_compare_list= markers_to_extract,
    frame_for_comparison= 20,
    frame_range= None
)


mdn_nih_trial_2_mediapipe_yolo_config = RecordingConfig(
    recording_name= 'MDN NIH Trial 2 Mediapipe/Yolo',
    path_to_recording = path_to_recording,
    path_to_freemocap_output_data = path_to_recording/'mediapipe_yolo_output_data'/'mediapipe_body_3d_xyz.npy',
    path_to_qualisys_output_data = path_to_recording/'qualisys_data'/ 'qualisys_joint_centers_3d_xyz.npy',
    qualisys_marker_list= qualisys_markers,
    markers_to_compare_list= markers_to_extract,
    frame_for_comparison= 20,
    frame_range= None
)


if __name__ == '__main__':
    from main import main
    import numpy as np
    
    # saved_transformation_matrix = np.load(path_to_recording/'transformation_matrix.npy')
    saved_transformation_matrix = None
    main(mdn_nih_trial_2_mediapipe_yolo_config,
        create_scatter_plot=False,
        save_transformation_matrix=True,
        transformation_matrix_to_use=saved_transformation_matrix)