"""Utility methods for the WAVES utility codebase
"""
import os


def get_waves_root() -> str:
    """Return local path to the root directory of the waves_utilities package install"""
    return os.path.abspath(os.path.join(__file__, ".."))
