from setuptools import setup, find_packages

packages = find_packages()
packages.append("")

setup(name='gemd',
      version='1.14.0',
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
          "toolz>=0.10.0,<1",
          "pint>=0.18,<0.22",
          "deprecation>=2.0.7,<3"
      ],
      extras_require={
          "tests": [
              "pytest>=7.3.1,<8"
          ],
          "gemd.demo.tests": [
              "pandas>=1.3.5,<2"
          ],
          "gemd.entity.bounds.tests": [
              "numpy"
          ]
      },
      classifiers=[
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
      ],
      )
