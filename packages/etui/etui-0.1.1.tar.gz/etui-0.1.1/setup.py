#!/usr/bin/env python
import sys
import os

# from distutils.core import setup
from setuptools import setup

# 'setup.py publish'
if sys.argv[-1] == "publish":
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/*")
    sys.exit()

with open("README.md", "r") as f:
    readme = f.read()
with open("LICENSE", "r") as f:
    license_txt = f.read()

setup(
    name="etui",
    version="0.1.1",
    description="Exquisite capsule fitted with useful helpers for every day coding",
    long_description=readme,
    long_description_content_type="text/markdown",
    license=license_txt,
    author="Michael Lückl",
    author_email="mlueckl@pm.me",
    url="https://github.com/mlueckl/etui",
    packages=["etui"],
    package_dir={"etui": "etui"},
    install_requires=["requests"],
)
