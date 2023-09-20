
import numpy as np

def extract_specific_markers(data_marker_dimension:np.ndarray, list_of_markers:list, markers_to_extract:list):
    """
    Extracts specific markers for a frame of a 3D data array based on the given indices and markers to extract.

    Parameters:
    - data (numpy.ndarray): The 3D data array containing all markers. Shape should be (num_markers, 3).
    - indices (list): The list of marker names corresponding to the columns in the data array.
    - markers_to_extract (list): The list of marker names to extract.

    Returns:
    - extracted_data (numpy.ndarray): A new 3D data array containing only the extracted markers. 
      Shape will be (num_frames, num_extracted_markers, 3).
    """
    # Identify the column indices that correspond to the markers to extract
    col_indices = [list_of_markers.index(marker) for marker in markers_to_extract if marker in list_of_markers]
    
    # Extract the relevant columns from the data array
    extracted_data = data_marker_dimension[col_indices, :]
    
    return extracted_data

