from setuptools import setup, find_packages
from codecs import open
from os import path

# Read version from VERSION file
here = path.abspath(path.dirname(__file__))

VERSION = "0.1.0"
DESCRIPTION = "A simple-to-use Instagram Python interface using Selenium."

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="PyGramCore",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Joel Taylor",
    author_email="contact@joeltaylor.business",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    keywords=["instagram", "instagram bot", "selenium", "automation", "bot"],
    packages=find_packages(exclude=["docs", "tests"]),
    install_requires=["selenium", "selenium-stealth"],
    setup_requires=["setuptools>=38.6.0"],
)
