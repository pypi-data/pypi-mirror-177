from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'My package'

# Setting up
setup(
    name="testpypackage",
    version=VERSION,
    author="Vishal",
    author_email="vishal126sw@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python','python3'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
