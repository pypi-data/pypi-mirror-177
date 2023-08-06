from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.0'
DESCRIPTION = 'Simple Package for Beauty Coding'

# Setting up
setup(
    name="vardxg",
    version=VERSION,
    author="Vardxg",
    author_email="<vardxgend@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['pystyle'],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
