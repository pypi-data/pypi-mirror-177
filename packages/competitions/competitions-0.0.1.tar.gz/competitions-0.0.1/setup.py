# coding=utf-8
# Copyright 2022 Hugging Face Inc
#
# Lint as: python3
# pylint: enable=line-too-long
"""Hugging Face Competitions
"""
from setuptools import find_packages, setup


DOCLINES = __doc__.split("\n")

QUALITY_REQUIRE = [
    "black~=22.0",
    "isort==5.8.0",
    "flake8==3.9.2",
    "mypy==0.901",
]

TEST_REQUIRE = ["pytest", "pytest-cov"]

EXTRAS_REQUIRE = {
    "dev": QUALITY_REQUIRE,
    "quality": QUALITY_REQUIRE,
    "test": TEST_REQUIRE,
    "docs": [
        "recommonmark",
        "sphinx==3.1.2",
        "sphinx-markdown-tables",
        "sphinx-rtd-theme==0.4.3",
        "sphinx-copybutton",
    ],
}

setup(
    name="competitions",
    version="0.0.1",
    description=DOCLINES[0],
    long_description="\n".join(DOCLINES),
    author="HuggingFace Inc.",
    url="https://github.com/huggingface/competitions",
    download_url="https://github.com/huggingface/competitions/tags",
    packages=find_packages("."),
    extras_require=EXTRAS_REQUIRE,
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="huggingface competitions machine learning ai nlp",
)
