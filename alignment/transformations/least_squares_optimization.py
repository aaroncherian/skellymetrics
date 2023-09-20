from scipy.spatial.transform import Rotation
from scipy import optimize
import numpy as np

def optimize_transformation_least_squares(transformation_matrix_guess, data_to_transform:np.ndarray, reference_data:np.ndarray):
    """
    Objective function for least squares optimization to find the best 3D transformation parameters, performed on a representative frame of data from both systems.
    The transformation matrix contains [3 translation, 3 rotation, 1 scaling].

    Parameters:
    - transformation_matrix_guess (list): Initial guess for [tx, ty, tz, rx, ry, rz, s].
    - data_to_transform (numpy.ndarray): A single frame of a 3D array of shape (num_markers, 3) to be transformed.
    - reference_data (numpy.ndarray): A single frame of a 3D array 3D array of shape (num_markers, 3) used as reference.

    Returns:
    - residuals (numpy.ndarray): Flattened array of residuals (differences) between transformed and reference data.
    """
    tx, ty, tz, rx, ry, rz, s = transformation_matrix_guess
    rotation = Rotation.from_euler('xyz', [rx, ry, rz], degrees=True)
    transformed_data = s * rotation.apply(data_to_transform) + [tx, ty, tz]
    residuals = reference_data - transformed_data
    return residuals.flatten()

def run_least_squares_optimization(data_to_transform:np.ndarray, reference_data:np.ndarray, initial_guess = [0,0,0,0,0,0,1]):
    transformation_matrix = optimize.least_squares(optimize_transformation_least_squares, initial_guess, args=(data_to_transform, reference_data),  gtol=1e-10, 
                                            verbose=2).x
    
    return transformation_matrix