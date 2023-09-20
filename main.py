from alignment.mocap_data_alignment import align_freemocap_and_qualisys_data
from visualizations.scatter_3d import plot_3d_scatter

def main(freemocap_data,qualisys_data,representative_frame, plot_3d_scatter = False):

    aligned_freemocap_data = align_freemocap_and_qualisys_data(freemocap_data=freemocap_data, qualisys_data=qualisys_data, representative_frame=representative_frame)

    if plot_3d_scatter:
        plot_3d_scatter(freemocap_data=aligned_freemocap_data, qualisys_data=qualisys_data)

    
    f = 2 



if __name__ == '__main__':

    from pathlib import Path
    import numpy as np

    qualisys_data_path = r"D:\2023-05-17_MDN_NIH_data\1.0_recordings\calib_3\qualisys_MDN_NIH_Trial3\output_data\clipped_qualisys_skel_3d.npy"
    freemocap_data_path = r"D:\2023-05-17_MDN_NIH_data\1.0_recordings\calib_3\sesh_2023-05-17_14_53_48_MDN_NIH_Trial3\output_data\mediapipe_body_3d_xyz.npy"
    freemocap_output_folder_path = Path(r"D:\2023-05-17_MDN_NIH_data\1.0_recordings\calib_3\sesh_2023-05-17_14_53_48_MDN_NIH_Trial3\output_data")

    freemocap_data = np.load(freemocap_data_path)
    qualisys_data = np.load(qualisys_data_path)

    main(freemocap_data,qualisys_data,800)
