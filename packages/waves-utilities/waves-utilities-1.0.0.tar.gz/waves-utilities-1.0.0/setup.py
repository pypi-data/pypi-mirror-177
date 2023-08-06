#!/usr/bin/env python

from distutils.core import setup

# read the contents of your README file
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="waves-utilities",
    version="1.0.0",
    description="SURF WAVES physiological waveform dataset utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    author="Daniel Miller",
    author_email="danielroymiller@gmail.com",
    url="https://bitbucket.org/surfstanfordmedicine/waves-utilities",
    packages=["waves_utilities"],
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "pytest",
    ],
)
