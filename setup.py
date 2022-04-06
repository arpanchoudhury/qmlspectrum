import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

PACKAGE_NAME = 'qmlspectrum'
VERSION = '22.04.02'
AUTHOR = 'Raghunathan Ramakrishnan'
AUTHOR_EMAIL = 'raghu.rama.chem@gmail.com'
URL = 'https://github.com/raghurama123/qmlspectrum'
LICENSE = 'MIT License'
DESCRIPTION = 'A test-suite that uses the package qml for modeling continuous spectra'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"
INSTALL_REQUIRES = [
      'numpy',
      'scipy',
      'matplotlib'
]

setup(name=PACKAGE_NAME,
      version=VERSION,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      url=URL,
      license=LICENSE,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages()
      )
