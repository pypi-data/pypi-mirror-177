"""Utilities to work with waveform .csv files downloaded from Redivis.

Note: since the actual waveform arrays are base-64 encoded and compressed in very large
single rows/cells, it is not sufficient to simply use a standard csv reader like pandas
"""
import base64
import binascii
import csv
from datetime import datetime
import logging
import sys
from typing import Iterator, Sequence, TypedDict
import zlib
from hashlib import sha256

import numpy as np

from waves_utilities.constants import BAD_VALUES
from waves_utilities.types import WaveformCSVRow

LOG = logging.getLogger()


class WavesCSVManager:
    def read_csv(
        self,
        filepath: str,
        header: Sequence[str] = None,
        from_index: int = None,
        to_index: str = None,
        limit: int = None,
        start_row: int = None,
    ) -> Iterator[WaveformCSVRow]:
        """Read the specified Waveform .csv file, yielding rows as they are loaded for
        memory efficiency

        Args:
            filepath (str): Path to the source .csv file
            header (Sequence[str], optional): Optionally filter the .csv columns by
                name. Defaults to None.
            from_index (int, optional): Start reading the waveform array(s) from this
                index.  Defaults to None.
            to_index (str, optional): Stop reading the waveform array(s) at this index.
                Defaults to None.
            limit (int, optional): Only read this many rows
            start_row (int, optional):  Start reading the csv from this row

        Yields:
            Iterator[WaveformCSVRow]: _description_
        """

        LOG.info(f"Reading {filepath} from {from_index} to {to_index}")
        csv.field_size_limit(sys.maxsize)
        with open(filepath, "r") as csvfile:
            csvreader = csv.DictReader(csvfile, delimiter=",", fieldnames=header)
            read_count = 0
            for row_index, row in enumerate(csvreader):
                if start_row is not None and row_index < start_row:
                    # Skip the first N rows of the csv file
                    continue

                LOG.debug(
                    f"Starting to read the .csv file at row {row_index}. "
                    f"{row['type']} channel valid from index {row['start_index']} to "
                    f"{row['stop_index']}"
                )
                clean_waveform = self.load_waveform(row["waveform"])

                # Data subsetting
                if to_index is not None:
                    clean_waveform = clean_waveform[:to_index]
                    row["stop_index"] = min(to_index, int(row["stop_index"]))
                if from_index is not None:
                    clean_waveform = clean_waveform[from_index:]
                    row["start_index"] = max(from_index, int(row["start_index"]))

                # row["waveform"] = clean_waveform

                clean_row = WaveformCSVRow(
                    wave_id=row["wave_id"],
                    group=int(row["group"]),
                    frequency=int(row["frequency"]),
                    gain=float(row["gain"]),
                    type=row["type"],
                    units=row["units"],
                    start_index=int(row["start_index"]),
                    stop_index=int(row["stop_index"]),
                    waveform=clean_waveform,
                )
                yield clean_row

                # Clean up for next iteration
                row = None
                clean_waveform = None

                read_count += 1
                if limit is not None and read_count >= limit:
                    LOG.info(f"Read limit of {read_count} rows from file, stopping!")
                    break

    def load_waveform(
        self, waveform_base64: str, filter_values: bool = True
    ) -> np.ndarray:
        """Load a single waveform array from compressed base-64 encoded string form

        Args:
            waveform_base64 (str): Encoded and compressed waveform data
            filter_values (bool, optional): Whether to drop all "bad" values.  Note:
                extreme 16-bit integer range values are used to encode various error and
                NaN types by the source Philips bedside monitor system. Defaults to
                True.

        Returns:
            np.ndarray: 16-bit signed integer array of the waveform data
        """
        raw_waveform = zlib.decompress(binascii.a2b_base64(waveform_base64))
        waveform = np.frombuffer(
            raw_waveform,
            # lz4.frame.decompress(binascii.a2b_base64(row["waveform"])),
            dtype=np.int16,
        )
        waveform_hash = sha256(raw_waveform).hexdigest()

        bad_mask = np.in1d(waveform, BAD_VALUES)
        LOG.debug(
            f"\twaveform hash:  {waveform_hash}, valid start:  {waveform[~bad_mask][:10]}..."
        )

        # Data filtering
        if filter_values:
            bad_mask = np.in1d(waveform, BAD_VALUES)
            clean_waveform = np.empty_like(waveform)
            clean_waveform[~bad_mask] = waveform[~bad_mask]
            LOG.debug(f"\tclean_waveform: {clean_waveform[:10]}...")
        else:
            clean_waveform = waveform

        return clean_waveform

    def write_csv(self, filepath: str, rows: Iterator[WaveformCSVRow]):
        """Write a list/iterable of waveform rows to the specified .csv file.

        Args:
            filepath (str): File path to save the new file (overwrites)
            rows (Iterator[WaveformCSVRow]): List or other iterable of CSV rows that
                should be written to file.
        """

        with open(filepath, "w") as f:
            csv_writer = csv.writer(f, delimiter=",")
            self.write_csv_header(csv_writer)
            for row_index, row in enumerate(rows):
                self.write_csv_row(
                    csv_writer=csv_writer,
                    row=row,
                )

    def write_csv_header(self, csv_writer):
        """Write a .csv file header to the top of the file.  Should call this as soon as
        the file is opened

        Args:
            csv_writer (_type_): output of csv.writer()
        """
        csv_writer.writerow(
            [
                "wave_id",
                "group",
                "type",
                "units",
                "gain",
                "frequency",
                "start_index",
                "stop_index",
                "waveform",
            ]
        )

    def write_csv_row(
        self,
        csv_writer,
        row: WaveformCSVRow,
    ):
        """Write a single row of CSV data to open file

        Args:
            csv_writer (_type_): output of csv.writer()
            row (WaveformCSVRow):  A single row of waveform data
        """
        csv_writer.writerow(
            [
                row["wave_id"],
                row["group"],
                row["type"],
                row["units"],
                row["gain"],
                row["frequency"],
                row["start_index"],
                row["stop_index"],
                # row["start_datetime"].isoformat(),
                # row["stop_datetime"].isoformat(),
                self.encode_waveform_data(row["waveform"]),
            ]
        )

    def encode_waveform_data(self, data: np.ndarray) -> str:
        """Base-64 encode a raw waveform array to string for storage in .csv file

        Args:
            data (np.ndarray): Raw waveform data (array of 16-bit signed integers)

        Returns:
            str: Base-64 encoded representation of the waveform data
        """
        return base64.b64encode(self.compress_data(data.astype(np.int16))).decode(
            "ascii"
        )

    def compress_data(
        self, data: np.ndarray, compression: str = "zlib", compression_level: int = None
    ) -> bytes:
        """Compress raw waveform data

        Args:
            data (np.ndarray): Raw uncompressed waveform data (16-bit signed integers)
            compression (str, optional): Compression library to use. Defaults to "zlib".
            compression_level (int, optional): Compression level (depends on selected
                library). Defaults to None.

        Raises:
            NotImplementedError: Invalid compression options

        Returns:
            bytes: Compressed waveform data, ready for base-64 encoding
        """
        if compression == "zlib":
            return zlib.compress(data)
        elif compression == "lz4":
            return lz4.frame.compress(
                data,
                compression_level=compression_level,
            )
        else:
            raise NotImplementedError(f"Unknown compression style {compression}")
