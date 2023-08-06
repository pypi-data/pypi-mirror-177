"""Plotting utilities for the WAVES dataset
"""

import logging

from typing import List, Tuple

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import numpy as np

from waves_utilities.types import WaveformCSVRow


LOG = logging.getLogger()


class WaveformPlotter:
    """Plotting utility for WAVES waveform data"""

    def plot_waveform(
        self,
        waveform_row: WaveformCSVRow,
        ax: Axes = None,
        save_filepath: str = None,
        xlabel: str = None,
        title: str = None,
        duration_seconds: int = None,
    ):
        """Plot a single waveform to the specified axis

        Args:
            waveform_row (WaveformCSVRow): A single row of waveform data
            ax (Axes, optional): Matplotlib Axes to plot to. Defaults to None (make a
                new single subplot from scratch).
            save_filepath (str, optional): Save the figure to the specified filepath.
                Defaults to None.
            xlabel (bool, optional): Add an X-axis (time) label to the plot axes.
                Defaults to False.
            title (str, optional): Add an title to the plot axes. Defaults to False.
            duration_seconds (int, optional): Only plot this many seconds of data
        """

        if ax is None:
            # Make a single axis figure
            f, axarr = self.make_figure()
            ax = axarr[0, 0]

        if duration_seconds is not None:
            waveform_row["stop_index"] = min(
                waveform_row["stop_index"],
                waveform_row["start_index"]
                + duration_seconds * waveform_row["frequency"],
            )
            waveform_row["waveform"] = waveform_row["waveform"][
                : waveform_row["stop_index"]
            ]

        # Set up and plot the waveform vs time
        time_axis = (
            np.arange(
                waveform_row["start_index"], waveform_row["stop_index"], dtype=np.float
            )
            / waveform_row["frequency"]
        )
        ax.plot(time_axis, waveform_row["waveform"] * waveform_row["gain"])

        # Add labels
        ax.set_ylabel("{0}  ({1})".format(waveform_row["type"], waveform_row["units"]))
        ax.set_xlim([min(time_axis) - 0.1, max(time_axis) + 0.1])
        # duration_seconds = (waveform_row["stop_index"] - waveform_row["start_index"]) / waveform_row["frequency"]
        # title = f"{waveform_row['wave_id']}/{waveform_row['group']} for {duration_seconds}s"
        if title is not None:
            ax.set_title(title)
        if xlabel is not None:
            ax.set_xlabel(xlabel)

        if save_filepath is not None:
            LOG.info(f"Saving plot of '{title}' to {save_filepath}")
            plt.savefig(save_filepath, bbox_inches="tight")

    def plot_waveforms(
        self,
        waveform_rows: List[WaveformCSVRow],
        save_filepath: str = None,
        title: str = None,
        duration_seconds: int = None,
    ):
        """Plot all of the provided waveforms to a single figure

        Args:
            waveform_rows (List[WaveformCSVRow]): All waveform data/channels to plot in
                parallel
            save_filepath (str, optional): Save the figure to the specified filepath.
                Defaults to None.
            duration_seconds (int, optional): Only plot this many seconds of data
        """
        f, axarr = self.make_figure(len(waveform_rows))

        for row_index, waveform_row in enumerate(waveform_rows):
            # Plot each waveform to a separate subplot
            # Add a title to the top and an xlabel to the bottom
            self.plot_waveform(
                waveform_row=waveform_row,
                ax=axarr[row_index, 0],
                xlabel="Time (s)" if (row_index == len(waveform_rows) - 1) else None,
                title=title if (row_index == 0) else None,
                duration_seconds=duration_seconds,
            )

        if save_filepath is not None:
            LOG.info(f"Saving plot of '{title}' to {save_filepath}")
            plt.savefig(save_filepath, bbox_inches="tight")

    def make_figure(self, num_channels: int = 1) -> Tuple[Figure, List[Axes]]:
        """Create a figure and axes to add plots on

        Args:
            num_channels (int, optional): Number of channels to plot. Defaults to 1.

        Returns:
            Tuple[Figure, List[Axes]]: Matplotlib Figure and subplot axes
        """
        plt.rcParams.update({"font.size": 22})
        f, axarr = plt.subplots(
            num_channels, sharex=True, figsize=(20, 5 * num_channels), squeeze=False
        )
        return f, axarr
