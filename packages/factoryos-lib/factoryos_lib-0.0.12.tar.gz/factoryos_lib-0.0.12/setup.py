# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="FactoryOS_lib",
    version="0.1.0",
    description="Data science library for FactoryOS Team",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/valiot/factoryos_lib/",
    author="FactoryOS Team",
    author_email="factoryos@valiot.io",
    license="Copyright Valiot.io",
    classifiers=[
        "Intended Audience :: FactoryOS Team",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["factoryos_lib.base",
              "factoryos_lib.base.inputs",
              "factoryos_lib.base.outputs",
              "factoryos_lib.execution",
              "factoryos_lib.filters"],
    include_package_data=True,
    install_requires=[
        "valiotworker",
        "pygqlc",
        "numpy",
        "pandas",
        "tensorflow",
        "retrying",
        "boto3",
        "protobuf",
        "fuzzylab",
        "matplotlib"
    ]
)