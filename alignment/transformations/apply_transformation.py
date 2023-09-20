from scipy.spatial.transform import Rotation
import numpy as np


def apply_transformation(transformation_matrix, data_to_transform):
    """
    Apply 3D transformation to a given dataset.
    The transformation matrix contains [3 translation, 3 rotation, 1 scaling].

    Parameters:
    - transformation_matrix (list): Transformation parameters [tx, ty, tz, rx, ry, rz, s].
    - data_to_transform (numpy.ndarray): 3D array of shape (num_frames, num_markers, 3) to be transformed.

    Returns:
    - transformed_data (numpy.ndarray): 3D array of the transformed data.
    """
    tx, ty, tz, rx, ry, rz, s = transformation_matrix
    rotation = Rotation.from_euler('xyz', [rx, ry, rz], degrees=True)
    transformed_data = np.zeros_like(data_to_transform)
    
    for i in range(data_to_transform.shape[0]):
        transformed_data[i, :, :] = s * rotation.apply(data_to_transform[i, :, :]) + [tx, ty, tz]
        
    return transformed_data