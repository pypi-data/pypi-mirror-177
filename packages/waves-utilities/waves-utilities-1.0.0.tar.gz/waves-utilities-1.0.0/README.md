# WAVES Utilities #

This python package/repository contains useful scripts, dataloaders, and examples for
working with the WAVES dataset of pediatric physiological waveforms.

## What is WAVES? ###

WAVES is an open-access pediatric physiological waveform dataset containing ECG, 
respiratory, plethysmogram, arterial blood pressure, and a variety of other 
high-frequency waveforms extracted from bedside monitors for patients at the Lucile 
Packard Childrens Hospital. The WAVES dataset itself is hosted by Redivis at 
[https://redivis.com/WAVES/datasets](https://redivis.com/WAVES/datasets)

WAVES is administrated by the 
[SURF Stanford Medicine](https://surf.stanford.edu/)
research group.

## What is this repository for? ###

* Python utilities to load and plot physiological waveform data from the WAVES dataset

## How do I get set up? ###
* Download/clone the repository
* Set up a python environment with the required dependencies: `conda env create -f environment.yml`
* Install the python package from pypi with `pip install waves_utilities`
    * (or run `python setup.py develop` for local development)


## Usage Examples

Refer to the tests and API documentation for more information on API options/arguments.

### Load data from .csv file
    from waves_utilities import WavesUtilityAPI
    util_api = WavesUtilityAPI()

    # Load a single row
    csv_row = next(util_api.csv_manager.read_csv("waveform_test_extract.csv", limit=1))

    # Load all rows (keep memory usage in mind for large data extracts)
    csv_rows = list(util_api.csv_manager.read_csv("waveform_test_extract.csv"))

### Plot waveforms
    # Plot 5 seconds from a single waveform
    util_api.waveform_plotter.plot_waveform(
        csv_row, save_filepath="single_waveform.png", duration_seconds=5
    )

    # Plot the full duration of multiple waveforms in file
    util_api.waveform_plotter.plot_waveforms(
        csv_rows, save_filepath="multi_waveforms.png", title="Test Waveform Data"
    )

## Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

## Who do I talk to? ###

* Daniel Miller: Primary researcher/developer for the WAVES dataset and codebase
* David Scheinker: Head of the SURF Stanford Medicine research group
