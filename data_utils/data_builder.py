import numpy as np
import pandas as pd 

# Define constants
DATA_3D_ARRAY = 'original_data_3d_array'
EXTRACTED_3D_ARRAY = 'extracted_data_3d_array'
DATAFRAME_OF_ORIGINAL_3D_DATA = 'dataframe_of_original_3d_data'
DATAFRAME_OF_EXTRACTED_3D_DATA = 'dataframe_of_extracted_3d_data'

class DataBuilder:
    def __init__(self, marker_list, path_to_data=None, data_array=None, extracted_3d_array = None, dataframe_of_original_3d_data = None, dataframe_of_extracted_3d_data = None):
        """
        Initialize the DataFrameBuilder.

        Parameters:
        - path_to_data (Path or str, optional): Path to the data file.
        - data_array (np.ndarray, optional): Pre-loaded data array.
        - marker_list (list): List of marker names.
        """
        self.path_to_data = path_to_data

        if data_array is not None:
            self.original_data_3d_array = data_array
        else:
            self.original_data_3d_array = None
            
        self.data_array = data_array
        self.marker_list = marker_list
        self.extracted_3d_array = extracted_3d_array
        self.dataframe_of_original_3d_data = dataframe_of_original_3d_data
        self.dataframe_of_extracted_3d_data = dataframe_of_extracted_3d_data

   
        # self.extracted_3d_array = None
        # self.dataframe_of_original_3d_data = None
        # self.dataframe_of_extracted_3d_data = None

    def load_data(self):
        """
        Load 3D data from file into numpy array if path_to_data is provided

        Returns:
        self
        """
        if self.path_to_data:
            self.original_data_3d_array = np.load(self.path_to_data)
        else:
            raise ValueError("Either path_to_data or data_array must be provided.")
        return self
    

    def extract_common_markers(self, markers_to_extract:list):
        """
        Extract markers from a specified list 
        Returns:
        self
        """

        self.markers_to_extract = markers_to_extract

        if self.original_data_3d_array is None:
            raise ValueError(f"{DATA_3D_ARRAY} is None. You must run load_data() first.")
            
        self.extracted_3d_array = self._extract_specific_markers(
            data_marker_dimension=self.original_data_3d_array,
            list_of_markers=self.marker_list,
            markers_to_extract=markers_to_extract)
        return self

    def convert_original_data_to_dataframe(self):
        """
        Convert the 3D data to a DataFrame.

        Returns:
        self
        """
        # Check if the target array exists
        if self.original_data_3d_array is None:
            raise ValueError(f"The target 3D array is None. You must run load_data() first.")

        self.dataframe_of_original_3d_data = self._convert_3d_array_to_dataframe(
            data_3d_array=self.original_data_3d_array,
            data_marker_list=self.original_data_3d_array)
        
        return self
    
    def convert_extracted_data_to_dataframe(self):
        """
        Convert the 3D data to a DataFrame.

        Returns:
        self
        """
        # Check if the target array exists
        if self.extracted_3d_array is None:
            raise ValueError(f"The target 3D array is None. You must run extract_common_markers() first.")
        
        self.dataframe_of_extracted_3d_data = self._convert_3d_array_to_dataframe(
            data_3d_array=self.extracted_3d_array,
            data_marker_list=self.markers_to_extract)
        
        return self
        

    def build(self):
        """
        Build the final DataFrame with 3D data.

        Returns:
        dict: Dictionary containing the loaded data, extracted 3D array, and final DataFrame.
        """
        return {
            DATA_3D_ARRAY: self.original_data_3d_array,
            EXTRACTED_3D_ARRAY: self.extracted_3d_array,
            DATAFRAME_OF_ORIGINAL_3D_DATA: self.dataframe_of_original_3d_data,
            DATAFRAME_OF_EXTRACTED_3D_DATA: self.dataframe_of_extracted_3d_data
        }

    def _extract_specific_markers(self,data_marker_dimension:np.ndarray, list_of_markers:list, markers_to_extract:list):
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
        extracted_data = data_marker_dimension[:,col_indices, :]

        return extracted_data
    
    def _convert_3d_array_to_dataframe(self, data_3d_array:np.ndarray, data_marker_list:list):
        """
        Convert the FreeMoCap data from a numpy array to a pandas DataFrame.

        Parameters:
        - data_3d_array (numpy.ndarray): The 3d data array. Shape should be (num_frames, num_markers, 3).
        - data_marker_list (list): List of marker names 

        Returns:
        - data_frame_marker_dim_dataframe (pandas.DataFrame): DataFrame containing FreeMoCap data with columns ['Frame', 'Marker', 'X', 'Y', 'Z'].

        """
        num_frames = data_3d_array.shape[0]
        num_markers = data_3d_array.shape[1]

        frame_list = []
        marker_list = []
        x_list = []
        y_list = []
        z_list = []

        for frame in range(num_frames):
            for marker in range(num_markers):
                frame_list.append(frame)
                marker_list.append(data_marker_list[marker])
                x_list.append(data_3d_array[frame, marker, 0])
                y_list.append(data_3d_array[frame, marker, 1])
                z_list.append(data_3d_array[frame, marker, 2])

        data_frame_marker_dim_dataframe = pd.DataFrame({
            'frame': frame_list,
            'marker': marker_list,
            'x': x_list,
            'y': y_list,
            'z': z_list
        })

        return data_frame_marker_dim_dataframe
