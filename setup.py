from setuptools import setup, find_packages
from pathlib import Path
import re

packages = find_packages()

this_directory = Path(__file__).parent.absolute()
version_file = this_directory / 'gemd' / '__version__.py'
version_re = r'''^\s*__version__\s*=\s*(['"])([\w\.]+)\1$'''
if mo := re.search(version_re, version_file.read_text(), re.M):
    version = mo.group(2)
else:
    raise RuntimeError(f"Unable to find version string in {version_file}")

setup(name='gemd',
      # Update this in gemd/__version__.py
      version=version,
      python_requires='>=3.9',
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
          "pint>=0.24.4,<0.25",
          "deprecation>=2.1.0,<3",
          "typing_extensions>=4.8,<5",
          "importlib-resources>=5.3,<7"
      ],
      extras_require={
          "scripts": [
              "packaging",
              "sphinx==5.0.0",
              "sphinx-rtd-theme==1.0.0",
              "sphinxcontrib-apidoc==0.3.0",
          ],
          "tests": [
              "pytest>=8.0.0,<9"
          ],
          "tests.demo": [
              "pandas>=2.0.3,<3"
          ],
          "tests.entity.bounds": [
              "numpy>=1.24.4,<2; python_version<='3.10'",
              "pandas>=2.0.3,<3"
          ]
      },
      classifiers=[
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
          'Programming Language :: Python :: 3.12',
          'Programming Language :: Python :: 3.13',
      ],
      )
