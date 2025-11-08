"""
Setup script for HMP Framework

Author: RokoOfficial
License: Apache 2.0
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hmp-framework",
    version="1.0.0",
    author="RokoOfficial",
    description="Hybrid Messaging Protocol - A modular framework for computational agents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RokoOfficial/HMP-Protocol-LLMs-Language-",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "agno>=1.6",
        "requests",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "black>=22.0",
            "flake8>=4.0",
        ],
    },
)
