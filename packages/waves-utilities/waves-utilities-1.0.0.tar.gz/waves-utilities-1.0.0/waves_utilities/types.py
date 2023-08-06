"""Custom data types, primarily for type hinting and autocompletion
"""
import datetime
import numpy as np
from typing import TypedDict


class WaveformCSVRow(TypedDict):
    """Typed representation of the data contained in each row of the waveform .csv files
    downloaded from the Redivis data store
    """

    wave_id: str
    group: str
    type: str
    frequency: int
    gain: float
    start_index: int
    stop_index: int
    start_datetime: datetime.datetime
    stop_datetime: datetime.datetime
    waveform: np.ndarray
