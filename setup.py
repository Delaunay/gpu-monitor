#!/usr/bin/env python
import os
from pathlib import Path

from setuptools import setup

with open("gpusmi/core/__init__.py") as file:
    for line in file.readlines():
        if "version" in line:
            version = line.split("=")[1].strip().replace('"', "")
            break

assert (
    os.path.exists(os.path.join("gpusmi", "__init__.py")) is False
), "gpusmi is a namespace not a module"

extra_requires = {"plugins": ["importlib_resources"]}
extra_requires["all"] = sorted(set(sum(extra_requires.values(), [])))

if __name__ == "__main__":
    setup(
        name="gpusmi",
        version=version,
        extras_require=extra_requires,
        description="GPU monitoring utilities",
        long_description=(Path(__file__).parent / "README.rst").read_text(),
        author="Pierre Delaunay",
        author_email="pierre@delaunay.io",
        license="BSD 3-Clause License",
        url="https://gpusmi.readthedocs.io",
        classifiers=[
            "License :: OSI Approved :: BSD License",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Operating System :: OS Independent",
        ],
        packages=[
            "gpusmi.core",
            "gpusmi.testing",
            "gpusmi.plugins.amd",
            "gpusmi.plugins.nvidia",
        ],
        setup_requires=["setuptools"],
        install_requires=["importlib_resources"],
        namespace_packages=[
            "gpusmi",
            "gpusmi.plugins",
        ],
        package_data={
            "gpusmi.data": [
                "gpusmi/data",
            ],
        },
    )
