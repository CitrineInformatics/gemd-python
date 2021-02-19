from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop
import sys
import subprocess


setup(name='gemd',
      version='0.17.1',
      url='http://github.com/CitrineInformatics/gemd-python',
      description="Python binding for Citrine's GEMD data model",
      author='Max Hutchinson',
      author_email='maxhutch@citrine.io',
      packages=find_packages(),
      package_data={
          'gemd': [
              'demo/strehlow_and_cook.pif',
              'demo/strehlow_and_cook_small.pif',
              'demo/toothpick.jpg',
              'units/citrine_en.txt',
              'units/constants_en.txt',
              'units/tests/test_units.txt'
          ]
      },
      install_requires=[
          "toolz",
          "pytest>=4.3",
          "pint>=0.9",
          "deprecation>=2.0.7,<3"
      ],
      classifiers=[
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
      ],
)
