#!/usr/bin/env python

from glob import glob
from os.path import basename, splitext
from pathlib import Path
from typing import List, Union

from setuptools import find_packages, setup


def parse_requirements(filename: Union[str, Path]) -> List:
    """Read requirements file in the style as produced by pip freeze.

    Parameters
    ----------
    filename : str or Path

    Returns
    -------
    list of required pkgs w/ evtl. version specs
    """
    with open(filename, "r", encoding="utf8") as f:
        lineiter = (line.strip() for line in f.readlines())
    return [line for line in lineiter if line and not line.startswith("#")]


DIR = Path(__file__).parent.absolute()
README = (DIR / "README.md").read_text()
install_reqs = parse_requirements(DIR / "requirements.txt")
try:
    dev_reqs = parse_requirements(DIR / "requirements-dev.txt")
except FileNotFoundError:
    dev_reqs = {}
    print("INFO: Could not find dev and/or prepro requirements txt file.")

version = "unknown"
with open(DIR / "src/smad/__init__.py") as file:
    for line in file:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip("'").strip('"').strip("\n")
            break

if __name__ == "__main__":

    setup(
        name="smad",
        version=version,
        author="abox1337",
        author_email="abox-dev@fiduciagad.de",
        description="SMAD library",
        long_description=README,
        long_description_content_type="text/markdown",
        packages=find_packages("src"),
        package_dir={"": "src"},
        include_package_data=True,
        py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
        zip_safe=False,
        classifiers=[
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3 :: Only",
            "Programming Language :: Python :: 3.9",
        ],
        keywords=[
            "smad",
        ],
        python_requires="==3.9.*",
        install_requires=install_reqs,
        extras_require={"dev": dev_reqs},
    )
