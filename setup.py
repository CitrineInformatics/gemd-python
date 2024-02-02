from setuptools import setup, find_packages
from os import path
from packaging.version import Version
import re

packages = find_packages()

this_directory = path.abspath(path.dirname(__file__))
version_file = path.join(this_directory, 'gemd', '__version__.py')
version_re = r'''^__version__\s*=\s*(['"])([\w\.]+)\1$'''
with open(version_file, 'r') as f:
    mo = re.search(version_re, f.read(), re.M)
    if mo:
        version = Version(mo.group(2))
    else:
        raise RuntimeError(f"Unable to find version string in {version_file}")

setup(name='gemd',
      # Update this in gemd/__version__.py
      version=str(version),
      python_requires='>=3.8',
      url='http://github.com/CitrineInformatics/gemd-python',
      description="Python binding for Citrine's GEMD data model",
      author='Citrine Informatics',
      packages=packages,
      package_data={
          'gemd.demo': [
              'strehlow_and_cook.pif',
              'strehlow_and_cook_small.pif',
              'toothpick.jpg'
          ],
          'gemd.units': [
              'citrine_en.txt',
              'constants_en.txt',
          ],
          'tests.units': ['test_units.txt']
      },
      install_requires=[
          "pint>=0.20,<0.24",
          "deprecation>=2.1.0,<3"
      ],
      extras_require={
          "tests": [
              "pytest>=8.0.0,<9"
          ],
          "tests.demo": [
              "pandas>=2.0.3,<3"
          ],
          "tests.entity.bounds": [
              "numpy>=1.24.4,<2",
              "pandas>=2.0.3,<3"
          ]
      },
      classifiers=[
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
          'Programming Language :: Python :: 3.12',
      ],
      )
