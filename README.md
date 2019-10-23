# taurus
Python binding for Citrine's nextgen data model (codename: taurus). 

This package provides a framework for storing information about the processes that create materials, the materials themselves, and measurements performed on those materials. 

## Usage

To install `taurus`, you can simply:
```
$ pip install taurus-citrine
```

Documentation of this package can be found at https://citrineinformatics.github.io/taurus/
Detailed documentation of the `taurus` data model can be found in the [language-agnostic documentation](https://citrineinformatics.github.io/taurus-documentation/).

## Developer instructions
To download the repo and install requirements, run 

```pip install git+https://github.com/CitrineInformatics/taurus.git```

Tests are run with `pytest`, and the `pytest-cov` package is used to assess test coverage. 
In order to assess coverage locally, run `pytest` with the following arguments:
* `--cov=taurus/` Assess coverage of all modules in the directory `taurus/` (required)
* `--cov-report term-missing` Prints line numbers for lines that are not executed (optional)
* `--cov-report term:skip-covered` Skips output for modules with full coverage (optional)
* `--cov-report xml` Saves coverage report to `coverage.xml` (optional)
* `--cov-fail-under=100` Throws an error if coverage is less than 100% (optional)

The following command will run all tests, print line numbers for lines that are not executed, skip modules with full coverage, and fail if coverage is less than 100%:
`python -m pytest --cov=taurus/ --cov-report term:skip-covered --cov-report term-missing --cov-fail-under=100`


