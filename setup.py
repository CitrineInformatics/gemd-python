from setuptools import setup, find_packages


setup(name='gemd',
      version='1.5.0',
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
          "toolz",
          "pytest>=4.3",
          "pint>=0.10",
          "deprecation>=2.0.7,<3"
      ],
      extras_require={
          "tests": [
              "pytest"
          ]
      },
      classifiers=[
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
      ],
      )
