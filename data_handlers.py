import numpy as np
import pandas as pd
from pathlib import Path
from typing import Union, Optional, List


class DataProcessor:
    def __init__(self, data: np.ndarray, marker_list: List[str], markers_for_alignment:List[str]):
        self._data = data
        self.marker_list = marker_list
        self.markers_for_alignment = markers_for_alignment
        self._extracted_data = self._extract_markers(markers_for_alignment)

    def _extract_markers(self, markers_for_alignment: List[str]):
        indices = [self.marker_list.index(marker) for marker in markers_for_alignment]
        extracted_data = self._data[:, indices, :]
        return extracted_data
    
    def _convert_3d_data_to_dataframe(self, data_to_convert: np.ndarray, markers_for_data: List[str]):
        num_frames = data_to_convert.shape[0]
        num_markers = data_to_convert.shape[1]

        frame_list = []
        marker_list = []
        x_list = []
        y_list = []
        z_list = []

        for frame in range(num_frames):
            for marker in range(num_markers):
                frame_list.append(frame)
                marker_list.append(markers_for_data[marker])
                x_list.append(data_to_convert[frame, marker, 0])
                y_list.append(data_to_convert[frame, marker, 1])
                z_list.append(data_to_convert[frame, marker, 2])

        dataframe = pd.DataFrame({
            'frame': frame_list,
            'marker': marker_list,
            'x': x_list,
            'y': y_list,
            'z': z_list
        })

        return dataframe

    
    @property
    def data_3d(self):
        return self._data
    
    @property
    def extracted_data_3d(self):
        return self._extracted_data
    
    @property
    def dataframe_of_extracted_3d_data(self):
        return self._convert_3d_data_to_dataframe(data_to_convert=self._extracted_data, markers_for_data=self.markers_for_alignment)
    
    @property
    def dataframe_of_3d_data(self):
        return self._convert_3d_data_to_dataframe(data_to_convert=self._data, markers_for_data=self.marker_list)
    

