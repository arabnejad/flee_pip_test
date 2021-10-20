#!/usr/bin/env python

"""The setup script."""

import pathlib
import os
import pkg_resources
from setuptools import setup, find_packages
import versioneer


with open("README.md") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()


pkg_local_dir = os.path.dirname(os.path.abspath(__file__))


with pathlib.Path("requirements.txt").open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

test_requirements = ["pytest>=3", ]

cmdclass = versioneer.get_cmdclass()

setup(
    author="Derek Groen",
    author_email="Derek.Groen@brunel.ac.uk",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD 3-clause license",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Flee is an agent-based modelling toolkit which is "
    "purpose-built for simulating the movement of individuals "
    "across geographical locations.",
    install_requires=install_requires,
    license="BSD 3-clause license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="flee",
    name="flee",
    packages=find_packages(include=["flee", "flee.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/arabnejad/flee",
    # version="0.1.0",
    version=versioneer.get_version(),
    cmdclass=cmdclass,
    zip_safe=False,
)
