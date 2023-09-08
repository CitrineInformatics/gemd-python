from setuptools import setup, find_packages

packages = find_packages()
packages.append("")

setup(name='gemd',
      version='1.16.2',
      python_requires='>=3.7',
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
          "toolz>=0.11.0,<1",
          "pint>=0.18,<1",
          "deprecation>=2.1.0,<3"
      ],
      extras_require={
          "tests": [
              "pytest>=7.3.1,<8"
          ],
          "tests.demo": [
              "pandas>=1.3.5,<3"
          ],
          "tests.entity.bounds": [
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
