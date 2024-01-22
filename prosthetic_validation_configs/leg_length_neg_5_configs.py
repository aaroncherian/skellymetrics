
from alignment.config import RecordingConfig
from pathlib import Path


from marker_sets.prosthetic_study_marker_set import qualisys_markers, markers_to_extract
path_to_leg_length_neg_5_mp_dlc = Path(r'D:\2023-06-07_TF01\1.0_recordings\treadmill_calib\sesh_2023-06-07_12_38_16_TF01_leg_length_neg_5_trial_1')

leg_length_neg_5_mp_dlc_config = RecordingConfig(
    recording_name= 'Mediaipipe + DLC, -.5in leg length',
    path_to_recording = path_to_leg_length_neg_5_mp_dlc,
    path_to_freemocap_output_data = path_to_leg_length_neg_5_mp_dlc/'mediapipe_dlc_output_data'/'mediapipe_body_3d_xyz.npy',
    path_to_qualisys_output_data = path_to_leg_length_neg_5_mp_dlc/'qualisys_data'/ 'qualisys_joint_centers_3d_xyz.npy',
    qualisys_marker_list= qualisys_markers,
    markers_to_compare_list= markers_to_extract,
    frame_for_comparison= 180,
    frame_range= None
)
