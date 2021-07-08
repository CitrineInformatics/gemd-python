from os.path import join
from setuptools import setup, find_packages


setup(name='gemd',
      version='1.0.2',
      url='http://github.com/CitrineInformatics/gemd-python',
      description="Python binding for Citrine's GEMD data model",
      author='Max Hutchinson',
      author_email='maxhutch@citrine.io',
      packages=find_packages(),
      package_data={
          'gemd': [
              join('demo', 'strehlow_and_cook.pif'),
              join('demo', 'strehlow_and_cook_small.pif'),
              join('demo', 'toothpick.jpg'),
              join('units', 'citrine_en.txt'),
              join('units', 'constants_en.txt'),
              join('units', 'tests/test_units.txt')
          ]
      },
      install_requires=[
          "toolz",
          "pytest>=4.3",
          "pint>=0.10",
          "deprecation>=2.0.7,<3"
      ],
      classifiers=[
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
      ],
      )
