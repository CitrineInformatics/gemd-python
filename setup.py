from setuptools import setup, find_packages


setup(name='gemd',
      version='1.10.2',
      url='http://github.com/CitrineInformatics/gemd-python',
      description="Python binding for Citrine's GEMD data model",
      author='Citrine Informatics',
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
          "toolz>=0.10.0,<1",
          "pint>=0.13,<1",
          "deprecation>=2.0.7,<3"
      ],
      extras_require={
          "tests": [
              "pytest>=6.2.5,<7"
          ],
          "gemd.demo.tests": [
              "pandas>=1.1.5,<2"
          ],
          "gemd.entity.bounds.tests": [
              "numpy"
          ]
      },
      classifiers=[
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
      ],
      )
