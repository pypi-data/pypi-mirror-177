from setuptools import setup, find_packages
from ms_imputedhours_core import __version__

setup(
      name='ms_imputedhours_core',
      version=__version__,
      packages=find_packages(),
      author='Jonathan Rodriguez Alejos',
      author_email='jrodriguez.5716@gmail.com',
      install_requires=open('requirements.txt').read().splitlines()
)