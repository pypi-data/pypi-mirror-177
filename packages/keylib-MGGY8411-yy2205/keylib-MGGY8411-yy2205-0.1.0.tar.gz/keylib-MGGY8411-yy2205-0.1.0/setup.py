from setuptools import setup

from codecs import open
from os import path

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="keylib-MGGY8411-yy2205",
    version="0.1.0",
    description="Just a key",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Yue",
    author_email="yy2205@nyu.edu",
    packages=["keylib"],
    include_package_data=True,
    install_requires=[
    ],
)
