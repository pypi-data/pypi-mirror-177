from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.11'
DESCRIPTION = 'Data wrangling on files read with pyreadstat'

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

# Setting up
setup(
    name="metatables",
    version=VERSION,
    author="Joël Grosjean",
    author_email="<joel.grosjean@gfs-zh.ch>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    url="https://github.com/tez4/metatables",
    packages=find_packages(),
    install_requires=[
        "pyreadstat >= 1.1",
        "pandas >= 1.3"
    ],
    extras_require={
        "dev": [
            "pytest >= 3.7",
            "check-manifest",
            "twine",
        ]
    },
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License"
    ]
)
