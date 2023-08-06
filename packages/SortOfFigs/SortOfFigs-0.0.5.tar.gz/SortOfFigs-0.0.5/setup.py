from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.5'
DESCRIPTION = 'PythonProgram'
LONG_DESCRIPTION = 'A package for sorting, searching and ordering of different figures'

# Setting up
setup(
    name="SortOfFigs",
    version=VERSION,
    author="Gopal Tiwari,Ranu Singh,Karishma Patel,Aman Pandey",
    author_email="gopaltiwarigopal786@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'tutorial', 'sorting and ordering of figs', 'areas'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)