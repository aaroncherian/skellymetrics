
from dataclasses import dataclass
from typing import Union, Tuple, Optional, List
from pathlib import Path


@dataclass
class RecordingConfig:
    recording_name: str
    path_to_recording: Union[str, Path]
    path_to_freemocap_output_data: Union[str, Path]
    path_to_qualisys_output_data: Union[str, Path]
    qualisys_marker_list: List[str]
    markers_to_compare_list: List[str]
    frames_to_sample: int = 20
    max_iterations: int = 10
    inlier_threshold: float = 70
    frame_range: Optional[Tuple[int, Optional[int]]] = None

