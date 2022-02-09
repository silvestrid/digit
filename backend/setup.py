#!/usr/bin/env python
import os

from setuptools import find_packages, setup


PROJECT_DIR = os.path.dirname(__file__)
REQUIREMENTS_DIR = os.path.join(PROJECT_DIR, "requirements")
VERSION = "0.1.0"


def get_requirements(env):
    with open(os.path.join(REQUIREMENTS_DIR, f"{env}.txt")) as fp:
        return [x.strip() for x in fp.read().split("\n") if not x.startswith("#")]


install_requires = get_requirements("base")


setup(
    name="digit",
    version=VERSION,
    url="",
    scripts=[""],
    author="Davide Silvestri",
    author_email="silvestri.eng@gmail.com",
    license="MIT",
    description="Piccoli Sergio reporting app",
    long_description="This app creates reports for the ABB smart sensors assets",
    platforms=["linux"],
    package_dir={"": "src"},
    packages=find_packages("src"),
    include_package_data=True,
    install_requires=install_requires,
)
