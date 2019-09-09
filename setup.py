from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop
import sys
import subprocess


class PostInstallCommand(install):
    """Post-installation for installation mode"""
    def run(self):
        """Python version is constrained to [3.5, 4.0), so if the minor version is < 6,
        run the script to strip type hints"""
        if sys.version_info.minor < 6:
            subprocess.call('chmod 755 scripts/strip_hints.sh', shell=True)
            subprocess.call('./scripts/strip_hints.sh', shell=True)
        install.run(self)


class PostDevelopCommand(develop):
    """Post-installation for develop mode"""
    def run(self):
        """Python version is constrained to [3.5, 4.0), so if the minor version is < 6,
        run the script to strip type hints"""
        if sys.version_info.minor < 6:
            subprocess.call('chmod 755 scripts/strip_hints.sh', shell=True)
            subprocess.call('./scripts/strip_hints.sh', shell=True)
        develop.run(self)


setup(name='taurus',
      version='0.0.0',
      url='http://github.com/CitrineInformatics/taurus-py',
      description='Python library for the Citrine Platform',
      author='Max Hutchinson',
      author_email='maxhutch@citrine.io',
      packages=find_packages(),
      package_data={'taurus': ['demo/strehlow_and_cook.json']},
      install_requires=[
          "toolz",
          "pytest>=4.3",
          "enum34",
          "pint>=0.9",
          "pymatgen",
          "strip-hints>=0.1.5"
      ],
      cmdclass={
          'install': PostInstallCommand,
          'develop': PostDevelopCommand
      }
)