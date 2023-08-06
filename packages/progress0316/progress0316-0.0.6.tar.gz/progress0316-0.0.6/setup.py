from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.6'
DESCRIPTION = 'Progress Bar'
LONG_DESCRIPTION = 'A kinda simple progress bar'

# Setting up
setup(
    name="progress0316",
    version=VERSION,
    author="Friscobuffo",
    author_email="<friscobuffo@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'progress', 'bar'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
