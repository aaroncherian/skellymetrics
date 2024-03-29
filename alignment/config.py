
from dataclasses import dataclass
from typing import Union, Tuple, Optional
from pathlib import Path


@dataclass
class RecordingConfig:
    recording_name: str
    path_to_recording: Union[str, Path]
    path_to_freemocap_output_data: Union[str, Path]
    path_to_qualisys_output_data: Union[str, Path]
    qualisys_marker_list: list
    markers_to_compare_list: list
    frame_for_comparison: int
    frame_range: Optional[Tuple[int, Optional[int]]] = None
