
import setuptools
import re
import os
import sys


setuptools.setup(
    name="neural-diffeqs",
    version="0.2.0rc",
    python_requires=">3.6.0",
    author="Michael E. Vinyard - Harvard University - Broad Institute of MIT and Harvard - Massachussetts General Hospital",
    author_email="mvinyard@broadinstitute.org",
    url=None,
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    description="neural differential equations",
    packages=setuptools.find_packages(),
    install_requires=[
        "torch>=1.12",
        "torch-nets>=0.0.1",
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3.6",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    license="MIT",
)
