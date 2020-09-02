from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop
import sys
import subprocess


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        """Run strip-hints to support python 3.5.

        Python version is constrained to [3.5, 4.0), so if the minor version is < 6,
        run the script to strip type hints
        """
        if sys.version_info.minor < 6:
            subprocess.call('chmod 755 scripts/strip_hints.sh', shell=True)
            subprocess.call('./scripts/strip_hints.sh', shell=True)
        install.run(self)


class PostDevelopCommand(develop):
    """Post-installation for develop mode."""

    def run(self):
        """Run strip-hints to support python 3.5.

        Python version is constrained to [3.5, 4.0), so if the minor version is < 6,
        run the script to strip type hints
        """
        if sys.version_info.minor < 6:
            subprocess.call('chmod 755 scripts/strip_hints.sh', shell=True)
            subprocess.call('./scripts/strip_hints.sh', shell=True)
        develop.run(self)


setup(name='gemd',
      version='0.13.2',
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
              'units/constants_en.txt'
          ]
      },
      install_requires=[
          "toolz",
          "pytest>=4.3",
          "pint>=0.9",
          "strip-hints>=0.1.5",
          "deprecation>=2.0.7,<3"
      ],
      classifiers=[
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
      ],
      # TODO: add this back when we apply them on deployments
      # cmdclass={
      #     'install': PostInstallCommand,
      #     'develop': PostDevelopCommand
      # }
      )
