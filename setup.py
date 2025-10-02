#!/usr/bin/env python3
"""
Setup script for the File to Image Encoder/Decoder project.
"""

from setuptools import setup, find_packages
import os

# Read the README file for the long description
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
with open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="file-to-image",
    version="1.0.0",
    author="Fr3d33",
    author_email="frederikkoch@proton.me",
    description="Encode any file into an image and decode it back perfectly",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Fr3d33/file-to-image",
    project_urls={
        "Bug Reports": "https://github.com/Fr3d33/file-to-image/issues",
        "Source": "https://github.com/Fr3d33/file-to-image",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Topic :: Multimedia :: Graphics",
        "Topic :: System :: Archiving",
    ],
    keywords="encoding, decoding, image, steganography, data, conversion",
    py_modules=["Encode", "Decode"],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": ["pytest>=6.0", "pytest-cov"],
        "test": ["pytest>=6.0"],
    },
    entry_points={
        "console_scripts": [
            "file-to-image-encode=Encode:main",
            "file-to-image-decode=Decode:main",
        ],
    },
)