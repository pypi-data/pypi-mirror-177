"""Top-level Python API to all WAVES utilities
"""

from waves_utilities.csv_manager import WavesCSVManager
from waves_utilities.plot import WaveformPlotter


class WavesUtilityAPI:
    """Top-level Python API class to easily access all WAVES utilities"""

    @property
    def csv_manager(self) -> WavesCSVManager:
        """Manager for reading and writing waveform .csv files

        Returns:
            WavesCSVManager: Instance of the CSV manager
        """
        return WavesCSVManager()

    @property
    def waveform_plotter(self) -> WaveformPlotter:
        """Manager for easily plotting waveform data with matplotlib

        Returns:
            WaveformPlotter: Instance of the plotting manager
        """
        return WaveformPlotter()
