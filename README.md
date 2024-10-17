# Image Encoding and Decoding Project

## Overview

This project allows you to encode binary data into an image and decode it back into its original form. It leverages the Python Imaging Library (PIL) to manipulate images and the NumPy library for efficient data handling. The encoding process transforms text files into RGB pixel data, while the decoding process extracts the original bytes from the image.

## Features

- Encode text files into an image format by converting bytes to pixel colors.
- Decode images back into the original text files, retrieving the embedded data.
- Handles non-white pixels efficiently, ensuring that the encoding and decoding processes are robust.

## Prerequisites

To run this project, you'll need:

- Python 3.x
- Pillow (Python Imaging Library)
- NumPy (optional, based on project needs)

You can install the required libraries using pip:

```bash
pip install Pillow numpy
