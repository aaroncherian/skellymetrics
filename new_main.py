from dash_app.run_dash_app import run_dash_app
from models.mocap_data_model import MoCapData

from pydantic import BaseModel, Field, model_validator
from typing import Callable, List
from pathlib import Path
import numpy as np
from skellymodels.skeleton_models.skeleton import Skeleton
from skellymodels.create_model_skeleton import create_mediapipe_skeleton_model, create_qualisys_skeleton_model
from p01_marker_set import markers_for_alignment
from data_handlers import DataProcessor
import pandas as pd

from error_calculations.get_error_metrics import get_error_metrics


def merge_dataframes(freemocap_dataframe, qualisys_dataframe):
    freemocap_dataframe['system'] = 'freemocap'
    qualisys_dataframe['system'] = 'qualisys'
    combined_dataframe = pd.concat([freemocap_dataframe, qualisys_dataframe], ignore_index=True)

    return combined_dataframe

def calculate_velocity(data_array):
    """
    Calculates the velocity from the data dictionary that is returned from the DataBuilder object 
    """
    return np.diff(data_array, axis = 0)

class SpatialAlignmentConfig(BaseModel):
    recording_name:str
    path_to_freemocap_recording_folder:Path
    path_to_freemocap_output_data: Path
    freemocap_skeleton_function: Callable[[], Skeleton]
    path_to_qualisys_output_data: Path
    qualisys_skeleton_function: Callable[[], Skeleton]
    markers_for_alignment: List[str]
    frames_to_sample: int = Field(20, gt=0, description="Number of frames to sample in each RANSAC iteration")
    max_iterations: int = Field(20, gt=0, description="Maximum number of RANSAC iterations")
    inlier_threshold: float = Field(50, gt=0, description="Inlier threshold for RANSAC")

    @model_validator(mode='after')
    def check_paths_and_load_data(cls, values):
        path_to_freemocap_output_data = values.path_to_freemocap_output_data
        path_to_qualisys_output_data = values.path_to_qualisys_output_data

        # Check if paths exist
        if not path_to_freemocap_output_data.exists():
            raise ValueError(f"Path does not exist: {path_to_freemocap_output_data}")
        if not path_to_qualisys_output_data.exists():
            raise ValueError(f"Path does not exist: {path_to_qualisys_output_data}")

        # Try loading the numpy data
        try:
            np.load(path_to_freemocap_output_data)
        except Exception as e:
            raise ValueError(f"Failed to load numpy data from {path_to_freemocap_output_data}: {e}")

        try:
            np.load(path_to_qualisys_output_data)
        except Exception as e:
            raise ValueError(f"Failed to load numpy data from {path_to_qualisys_output_data}: {e}")

        return values


path_to_freemocap_recording_folder= Path(r'D:\2024-04-25_P01\1.0_recordings\sesh_2024-04-25_15_44_19_P01_WalkRun_Trial1')

path_to_aligned_data_folder = path_to_freemocap_recording_folder/'aligned_data'
path_to_aligned_data_folder.mkdir(parents=True, exist_ok=True)

path_to_aligned_center_of_mass_folder = path_to_aligned_data_folder/'center_of_mass'
path_to_aligned_center_of_mass_folder.mkdir(parents=True, exist_ok=True)


p01_walkrun_trial_1_alignment_config = SpatialAlignmentConfig(
    recording_name = 'P01 WalkRun Trial 1',
    path_to_freemocap_recording_folder=path_to_freemocap_recording_folder,
    path_to_freemocap_output_data = path_to_freemocap_recording_folder/'aligned_data'/'mediapipe_body_3d_xyz.npy',
    freemocap_skeleton_function = create_mediapipe_skeleton_model,
    path_to_qualisys_output_data = path_to_freemocap_recording_folder/'qualisys_data'/ 'qualisys_joint_centers_3d_xyz.npy',
    qualisys_skeleton_function= create_qualisys_skeleton_model,
    markers_for_alignment=markers_for_alignment,
    frames_to_sample=20,
    max_iterations=50,
    inlier_threshold=40
)

def get_metrics(config:SpatialAlignmentConfig):

    freemocap_skeleton_model = config.freemocap_skeleton_function()
    qualisys_skeleton_model = config.qualisys_skeleton_function()


    freemocap_data = np.load(config.path_to_freemocap_output_data)
    freemocap_skeleton_model.integrate_freemocap_3d_data(freemocap_data)

    qualisys_data = np.load(config.path_to_qualisys_output_data)
    qualisys_skeleton_model.integrate_freemocap_3d_data(qualisys_data)

    freemocap_data_handler = DataProcessor(
        data=freemocap_skeleton_model.marker_data_as_numpy,
        marker_list=freemocap_skeleton_model.marker_names,
        markers_for_alignment=config.markers_for_alignment
    )
    qualisys_data_handler = DataProcessor(
        data=qualisys_skeleton_model.marker_data_as_numpy,
        marker_list=qualisys_skeleton_model.marker_names,
        markers_for_alignment=config.markers_for_alignment
    )

    position_data_frame = merge_dataframes(freemocap_data_handler.dataframe_of_extracted_3d_data, qualisys_data_handler.dataframe_of_extracted_3d_data)
    position_error_metrics = get_error_metrics(position_data_frame)

    position_data = MoCapData(
        joint_dataframe=position_data_frame,
        rmse_dataframe=position_error_metrics['rmse_dataframe'],
        absolute_error_dataframe=position_error_metrics['absolute_error_dataframe']
    )

    freemocap_velocity_data = calculate_velocity(freemocap_data_handler.data_3d)
    freemocap_velocity_data_handler = DataProcessor(
        data=freemocap_velocity_data,
        marker_list=freemocap_skeleton_model.marker_names,
        markers_for_alignment=config.markers_for_alignment
    )

    qualisys_velocity_data = calculate_velocity(qualisys_data_handler.data_3d)
    qualisys_velocity_data_handler = DataProcessor(
        data=qualisys_velocity_data,
        marker_list=qualisys_skeleton_model.marker_names,
        markers_for_alignment=config.markers_for_alignment
    )

    velocity_data_frame = merge_dataframes(freemocap_velocity_data_handler.dataframe_of_extracted_3d_data, qualisys_velocity_data_handler.dataframe_of_extracted_3d_data)
    velocity_error_metrics = get_error_metrics(velocity_data_frame)

    velocity_data = MoCapData(
        joint_dataframe=velocity_data_frame,
        rmse_dataframe=velocity_error_metrics['rmse_dataframe'],
        absolute_error_dataframe=velocity_error_metrics['absolute_error_dataframe']
    )

    run_dash_app(position_data_and_error=position_data, velocity_data_and_error=velocity_data, recording_config=config)


    f = 2


get_metrics(p01_walkrun_trial_1_alignment_config)

# run_dash_app(position_data_and_error=position_data, velocity_data_and_error=velocity_data, recording_config=recording_config)