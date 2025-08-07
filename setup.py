#!/usr/bin/env python3
"""
Setup script for Chord DHT Network Graph Visualization
"""

from setuptools import setup, find_packages
import os

# Read README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements file
def read_requirements():
    requirements = []
    if os.path.exists("requirements.txt"):
        with open("requirements.txt", "r", encoding="utf-8") as fh:
            requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]
    return requirements

setup(
    name="chord-dht-viz",
    version="1.0.0",
    author="Team Glitch",
    author_email="team.glitch@example.com",
    description="A comprehensive Chord DHT implementation with graph visualization",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Akashbht/Chord-DHT-graphi-viz",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: System :: Distributed Computing",
        "Topic :: System :: Networking",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.0.0",
            "black>=21.0.0",
            "flake8>=3.9.0",
            "mypy>=0.910",
        ],
        "optional": [
            "networkx>=2.6",
            "matplotlib>=3.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "chord-dht=Main:main",
        ],
    },
    keywords=[
        "chord",
        "dht",
        "distributed-hash-table",
        "p2p",
        "peer-to-peer",
        "visualization",
        "graph",
        "network",
        "distributed-systems",
    ],
    project_urls={
        "Bug Reports": "https://github.com/Akashbht/Chord-DHT-graphi-viz/issues",
        "Source": "https://github.com/Akashbht/Chord-DHT-graphi-viz",
        "Documentation": "https://github.com/Akashbht/Chord-DHT-graphi-viz/blob/main/README.md",
    },
    include_package_data=True,
    zip_safe=False,
)