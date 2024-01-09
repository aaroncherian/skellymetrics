from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

from markers.mediapipe_markers import mediapipe_markers

def load_data_from_path(path_to_data_folder):
    # file_name = 'mediapipe_deeplabcut_3dData_spliced.npy'
    file_name = 'mediapipe_body_3d_xyz.npy'
    path_to_file = path_to_data_folder / file_name

    return np.load(path_to_file)


path_to_session = Path(r'D:\2023-06-07_TF01\1.0_recordings\treadmill_calib\sesh_2023-06-07_12_06_15_TF01_flexion_neutral_trial_1')
path_to_session = path_to_session

# #to check raw data
# path_to_mediapipe_dlc = path_to_session / 'dlc_non_rotated'/'raw_data'
# path_to_mediapipe_yolo_dlc = path_to_session / 'dlc_yolo_non_rotated'/'raw_data'


path_to_mediapipe_dlc = path_to_session / 'mediapipe_dlc_output_data'
path_to_mediapipe_yolo_dlc = path_to_session / 'mediapipe_output_data'
path_to_mediapipe_yolo_ref_dlc = path_to_session / 'mediapipe_yolo_ref_dlc_output_data'


# path_to_mediapipe_dlc = path_to_session / 'mediapipe_dlc_output_data'
# path_to_mediapipe_yolo_dlc = path_to_session / 'mediapipe_yolo_dlc_output_data'
# path_to_mediapipe_yolo_ref_dlc = path_to_session / 'mediapipe_yolo_ref_dlc_output_data'

mediapipe_data = load_data_from_path(path_to_mediapipe_dlc)
mediapipe_yolo_data = load_data_from_path(path_to_mediapipe_yolo_dlc)
mediapipe_yolo_ref_data = load_data_from_path(path_to_mediapipe_yolo_ref_dlc)


hip_index = mediapipe_markers.index('right_hip')
knee_index = mediapipe_markers.index('right_knee')
ankle_index = mediapipe_markers.index('right_ankle')

index_list = [23]


plt.figure()

for index in index_list:
    plt.plot(mediapipe_data[:, index, 0], label='dlc', color='blue', alpha=0.5)
    plt.plot(mediapipe_yolo_data[:, index, 0], label='dlc_yolo', color='red', alpha=0.5)
    plt.plot(mediapipe_yolo_ref_data[:, index, 0], label='dlc_yolo_ref', color='grey', alpha=0.5)

plt.suptitle('Non-Rotated DLC Data')
plt.xlabel('Frame')
plt.ylabel('X (mm)')
plt.legend()
plt.show()


