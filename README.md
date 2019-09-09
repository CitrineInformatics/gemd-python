# taurus
Data concepts for Next Gen platform. 
Provides a framework for storing information about the processes that create materials, the materials themselves, and measurements performance on those materials. 

Detailed documentation of the next gen format can be found in the language-agnostic documentation.

## Installation
To download the repo and install requirements, run 

```pip install git+https://github.com/CitrineInformatics/taurus.git```

Tests are run with `pytest`, and the `pytest-cov` package is used to assess test coverage. 
In order to assess coverage locally, run `pytest` with the following arguments:
* `--cov=taurus/` Assess coverage of all modules in the directory `taurus/` (required)
* `--cov-report term-missing` Prints line numbers for lines that are not executed (optional)
* `--cov-report term:skip-covered` Skips output for modules with full coverage (optional)
* `--cov-report xml` Saves coverage report to `coverage.xml` (optional)
* `--cov-fail-under=85` Throws an error if coverage is less than 85% (optional)

The following command will run all tests, print line numbers for lines that are not executed, skip modules with full coverage, and fail if coverage is less than 85%:
`python -m pytest --cov=taurus/ --cov-report term:skip-covered --cov-report term-missing --cov-fail-under=85`

## Usage
Ingester scripts are used to import real-world materials data. 
The results can then be serialized to JSON, and deserialized back into Taurus. 

An example ingester can be found in `/taurus/ingest/material_run_example.py`, and code that feeds example data into the ingester is at `taurus/ingest/tests/test_material_run_example.py`. 
For details, see `taurus/ingest/readme.md`.
