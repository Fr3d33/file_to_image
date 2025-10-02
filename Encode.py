#!/usr/bin/env python3
"""
File to Image Encoder

This script encodes binary data from a file into an image by converting bytes to RGB pixel values.
Each group of 3 bytes becomes one RGB pixel in the output image.

Usage:
    python Encode.py [input_file] [output_image] [--width WIDTH] [--height HEIGHT]

Example:
    python Encode.py Sample/Encode.txt Sample/Encode.png --width 500 --height 400
"""

import argparse
import math
import os
import sys
from pathlib import Path
from PIL import Image


def calculate_optimal_dimensions(file_size: int, max_width: int = 1000, max_height: int = 1000):
    """
    Calculate optimal image dimensions based on file size.
    
    Args:
        file_size (int): Size of the file in bytes
        max_width (int): Maximum width constraint
        max_height (int): Maximum height constraint
        
    Returns:
        tuple[int, int]: Optimal width and height for the image
    """
    # Calculate minimum pixels needed (3 bytes per pixel)
    pixels_needed = math.ceil(file_size / 3)
    
    # Calculate square root for roughly square image
    side_length = math.ceil(math.sqrt(pixels_needed))
    
    # Ensure dimensions don't exceed constraints
    width = min(side_length, max_width)
    height = math.ceil(pixels_needed / width)
    
    # Ensure height doesn't exceed constraint
    if height > max_height:
        height = max_height
        width = math.ceil(pixels_needed / height)
    
    return width, height


def encode_file_to_image(input_file: str, output_image: str, width: int = None, height: int = None):
    """
    Encode a file into an image by converting bytes to RGB pixel values.
    
    Args:
        input_file (str): Path to the input file
        output_image (str): Path for the output image
        width (int, optional): Image width. Auto-calculated if not provided
        height (int, optional): Image height. Auto-calculated if not provided
    
    Raises:
        FileNotFoundError: If input file doesn't exist
        ValueError: If image dimensions are too small for file size
        IOError: If there's an error reading/writing files
    """
    try:
        # Check if input file exists
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file '{input_file}' not found.")
        
        # Read the file bytes
        with open(input_file, "rb") as f:
            file_bytes = f.read()
        
        if not file_bytes:
            raise ValueError("Input file is empty.")
        
        print(f"Input file: {input_file}")
        print(f"File size: {len(file_bytes)} bytes")
        
        # Calculate or use provided dimensions
        if width is None or height is None:
            width, height = calculate_optimal_dimensions(len(file_bytes))
            print(f"Auto-calculated dimensions: {width}x{height}")
        else:
            print(f"Using provided dimensions: {width}x{height}")
        
        # Check if image is large enough
        max_capacity = width * height * 3
        if len(file_bytes) > max_capacity:
            raise ValueError(f"File too large for image dimensions. "
                           f"File: {len(file_bytes)} bytes, Image capacity: {max_capacity} bytes")
        
        # Add padding if necessary (ensure length is multiple of 3)
        padded_length = len(file_bytes)
        if padded_length % 3 != 0:
            padding = 3 - (padded_length % 3)
            file_bytes += b'\x00' * padding
            padded_length = len(file_bytes)
            print(f"Added {padding} bytes of padding")
        
        # Create a new RGB image with white background
        image = Image.new("RGB", (width, height), color=(255, 255, 255))
        
        # Convert bytes to RGB tuples
        pixel_data = [(file_bytes[i], file_bytes[i+1], file_bytes[i+2])
                      for i in range(0, len(file_bytes), 3)]
        
        # Set pixels in the image
        for i, color in enumerate(pixel_data):
            x = i % width
            y = i // width
            if y < height:
                image.putpixel((x, y), color)
            else:
                break
        
        # Create output directory if it doesn't exist
        output_path = Path(output_image)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save the image
        image.save(output_image)
        
        print(f"Successfully encoded {padded_length} bytes into '{output_image}'")
        print(f"Image dimensions: {width}x{height}")
        
    except Exception as e:
        print(f"Error encoding file: {e}", file=sys.stderr)
        raise


def main():
    """
    Main function to handle command-line arguments and execute encoding.
    """
    parser = argparse.ArgumentParser(
        description="Encode a file into an image by converting bytes to RGB pixels",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python Encode.py input.txt output.png
  python Encode.py data.bin image.png --width 800 --height 600
  python Encode.py Sample/Encode.txt Sample/Encode.png
        """
    )
    
    parser.add_argument(
        "input_file",
        nargs="?",
        default="Sample/Encode.txt",
        help="Path to the input file to encode (default: Sample/Encode.txt)"
    )
    
    parser.add_argument(
        "output_image",
        nargs="?", 
        default="Sample/Encode.png",
        help="Path for the output image (default: Sample/Encode.png)"
    )
    
    parser.add_argument(
        "--width",
        type=int,
        help="Image width (auto-calculated if not provided)"
    )
    
    parser.add_argument(
        "--height",
        type=int,
        help="Image height (auto-calculated if not provided)"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="File to Image Encoder 1.0.0"
    )
    
    args = parser.parse_args()
    
    try:
        encode_file_to_image(
            args.input_file,
            args.output_image,
            args.width,
            args.height
        )
    except Exception as e:
        sys.exit(1)


if __name__ == "__main__":
    main()
