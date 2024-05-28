from alignment.config import RecordingConfig
from pathlib import Path


from marker_sets.P01_validation_marker_set import qualisys_markers, markers_to_extract
path_to_recording = Path(r"D:\2024-04-25_P01\1.0_recordings\sesh_2024-04-25_14_45_59_P01_NIH_Trial1")

p01_nih_trial_1_config = RecordingConfig(
    recording_name= 'P01 NIH Trial 1',
    path_to_recording = path_to_recording,
    path_to_freemocap_output_data = path_to_recording/'output_data'/'mediapipe_body_3d_xyz.npy',
    path_to_qualisys_output_data = path_to_recording/'qualisys_data'/ 'qualisys_joint_centers_3d_xyz.npy',
    qualisys_marker_list= qualisys_markers,
    markers_to_compare_list= markers_to_extract,
    frame_for_comparison= 450,
    frame_range= None
)


# mdn_nih_trial_2_mediapipe_yolo_config = RecordingConfig(
#     recording_name= 'MDN NIH Trial 2 Mediapipe/Yolo',
#     path_to_recording = path_to_recording,
#     path_to_freemocap_output_data = path_to_recording/'mediapipe_yolo_output_data'/'mediapipe_body_3d_xyz.npy',
#     path_to_qualisys_output_data = path_to_recording/'qualisys_data'/ 'qualisys_joint_centers_3d_xyz.npy',
#     qualisys_marker_list= qualisys_markers,
#     markers_to_compare_list= markers_to_extract,
#     frame_for_comparison= 20,
#     frame_range= None
# )


if __name__ == '__main__':
    from main import main
    import numpy as np
    
    # saved_transformation_matrix = np.load(path_to_recording/'transformation_matrix.npy')
    saved_transformation_matrix = None
    main(p01_nih_trial_1_config,
        create_scatter_plot=False,
        save_transformation_matrix=False,
        transformation_matrix_to_use=saved_transformation_matrix)