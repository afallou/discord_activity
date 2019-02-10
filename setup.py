#!/usr/bin/env python
from setuptools import find_packages, setup

project = "bplc"
version = "0.1.0"

setup(
    name=project,
    python_requires=">=3.6.0",
    version=version,
    description="ETL engine for Discord",
    author="Adrien Fallou",
    author_email="",
    url="",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "click>=7.0",
        "microcosm>=2.4.1",
        "microcosm-logging>=1.3.0",
        "requests>=2.21.0",
    ],
    setup_requires=[],
    entry_points={
        "console_scripts": [
            "extract = discord_activity.extract.main:main",
        ],
    },
    tests_require=[
        "pyhamcrest>=1.9.0",
        "nose>=1.3.7",
    ],
)
