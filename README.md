# GEMD-python 
Python binding for Citrine's nextgen data model, GEMD. 

This package provides a framework for storing information about the processes that create materials, the materials themselves, and measurements performed on those materials. 

## Usage

To install `gemd`, you can simply:
```bash
$ pip install gemd
```

Detailed documentation of the `GEMD` data model can be found in the [language-agnostic documentation](https://citrineinformatics.github.io/gemd-docs/).
Documentation of this package can be found [here](https://citrineinformatics.github.io/gemd-python/).

## Developer instructions
To download the repo and install requirements, run 

```bash
pip install git+https://github.com/CitrineInformatics/gemd-python.git
```

Tests are run with `pytest`, and the `pytest-cov` package is used to assess test coverage. 
In order to assess coverage locally, run `pytest` with the following arguments:
* `--cov=gemd/` Assess coverage of all modules in the directory `gemd/` (required)
* `--cov-report term-missing` Prints line numbers for lines that are not executed (optional)
* `--cov-report term:skip-covered` Skips output for modules with full coverage (optional)
* `--cov-report xml` Saves coverage report to `coverage.xml` (optional)
* `--cov-fail-under=100` Throws an error if coverage is less than 100% (optional)

The following command will run all tests, print line numbers for lines that are not executed, skip modules with full coverage, and fail if coverage is less than 100%:
```bash
pytest --cov=gemd --cov-report term-missing --cov-report term:skip-covered --cov-config=tox.ini --cov-fail-under=100 -s ./gemd
```


