# To use a consistent encoding
from codecs import open
from os import path

from setuptools import find_packages, setup

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="file-repository-api-client",
    version="0.2.0",
    description="",
    long_description="Text File Repository API client",
    long_description_content_type="text/markdown",
    url="https://file-repository-api-client.readthedocs.io/",
    author="Mfana Ronald Conco",
    author_email="ronald.conco@mlankatech.co.za",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=find_packages(include=['file_repository_api_client'],exclude="tests"),
    include_package_data=True,
    install_requires=["requests"],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests'
)
