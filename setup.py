from setuptools import find_packages
import setuptools
import fakear


with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name = "fakear",
    version = "0.1",
    author = "Franck LOURME",
    author_email = "flourme@scaleway.com",
    description = "A Shell-command faker for Python Unit Testing",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "",
    packages = find_packages(),
    install_requires = [
        "pyyaml",
        "voluptuous"
    ],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT Licence",
        "Operating System :: Linux"
    ]
)
