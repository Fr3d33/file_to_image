#!/usr/bin/env python3
"""
Image to File Decoder

This script decodes binary data from an image back to its original file format.
It extracts RGB pixel values and converts them back to bytes.

Usage:
    python Decode.py [input_image] [output_file] [--method METHOD]

Example:
    python Decode.py Sample/Encode.png Sample/Decode.txt
    python Decode.py image.png output.bin --method smart
"""

import argparse
import os
import sys
from pathlib import Path
from PIL import Image


def count_non_white_pixels(image):
    """
    Count the number of non-white pixels in an image.
    
    Args:
        image (PIL.Image.Image): The image to analyze
        
    Returns:
        int: Number of non-white pixels
    """
    # Ensure the image is in RGB format
    image = image.convert("RGB")
    width, height = image.size
    non_white_count = 0
    
    # Loop through each pixel
    for y in range(height):
        for x in range(width):
            r, g, b = image.getpixel((x, y))
            if (r, g, b) != (255, 255, 255):  # Not white
                non_white_count += 1
    
    return non_white_count


def find_data_end_smart(image):
    """
    Smart detection of where encoded data ends by finding the last non-white pixel.
    
    Args:
        image (PIL.Image.Image): The image to analyze
        
    Returns:
        int: Index of the last pixel containing data
    """
    image = image.convert("RGB")
    width, height = image.size
    last_data_pixel = 0
    
    # Scan pixels in reading order to find last non-white pixel
    for y in range(height):
        for x in range(width):
            pixel_index = y * width + x
            r, g, b = image.getpixel((x, y))
            if (r, g, b) != (255, 255, 255):  # Not white
                last_data_pixel = pixel_index
    
    return last_data_pixel + 1  # +1 because we want count, not index


def decode_image_to_file(input_image: str, output_file: str, method: str = "count"):
    """
    Decode an image back to its original file format.
    
    Args:
        input_image (str): Path to the input image
        output_file (str): Path for the output file
        method (str): Decoding method ('count' or 'smart')
    
    Raises:
        FileNotFoundError: If input image doesn't exist
        ValueError: If image cannot be processed
        IOError: If there's an error reading/writing files
    """
    try:
        # Check if input image exists
        if not os.path.exists(input_image):
            raise FileNotFoundError(f"Input image '{input_image}' not found.")
        
        # Open and validate the image
        try:
            image = Image.open(input_image)
        except Exception as e:
            raise ValueError(f"Cannot open image '{input_image}': {e}")
        
        # Ensure RGB format
        image = image.convert("RGB")
        width, height = image.size
        
        print(f"Input image: {input_image}")
        print(f"Image dimensions: {width}x{height}")
        print(f"Decoding method: {method}")
        
        # Determine how many pixels contain data
        if method == "smart":
            data_pixels = find_data_end_smart(image)
            print(f"Smart detection: {data_pixels} pixels contain data")
        else:  # count method
            data_pixels = count_non_white_pixels(image)
            print(f"Non-white pixels: {data_pixels}")
        
        if data_pixels == 0:
            raise ValueError("No encoded data found in image (all pixels are white)")
        
        # Extract bytes from pixels
        decoded_bytes = []
        
        for i in range(data_pixels):
            x = i % width
            y = i // width
            
            if y >= height:
                break
            
            r, g, b = image.getpixel((x, y))
            decoded_bytes.extend([r, g, b])
        
        # Convert to bytes object
        decoded_data = bytes(decoded_bytes)
        
        # Remove trailing null bytes (padding)
        decoded_data = decoded_data.rstrip(b'\x00')
        
        if not decoded_data:
            raise ValueError("No valid data found after removing padding")
        
        # Create output directory if it doesn't exist
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save the decoded data
        with open(output_file, "wb") as f:
            f.write(decoded_data)
        
        print(f"Successfully decoded {len(decoded_data)} bytes to '{output_file}'")
        print(f"Decoded {data_pixels} pixels ({len(decoded_bytes)} total bytes before padding removal)")
        
    except Exception as e:
        print(f"Error decoding image: {e}", file=sys.stderr)
        raise


def main():
    """
    Main function to handle command-line arguments and execute decoding.
    """
    parser = argparse.ArgumentParser(
        description="Decode an image back to its original file format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Methods:
  count: Count all non-white pixels (legacy method)
  smart: Find the last non-white pixel (more accurate)

Examples:
  python Decode.py encoded.png output.txt
  python Decode.py Sample/Encode.png Sample/Decode.txt --method smart
        """
    )
    
    parser.add_argument(
        "input_image",
        nargs="?",
        default="Sample/Encode.png",
        help="Path to the input image to decode (default: Sample/Encode.png)"
    )
    
    parser.add_argument(
        "output_file",
        nargs="?",
        default="Sample/Decode.txt",
        help="Path for the output file (default: Sample/Decode.txt)"
    )
    
    parser.add_argument(
        "--method",
        choices=["count", "smart"],
        default="smart",
        help="Decoding method to use (default: smart)"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="Image to File Decoder 1.0.0"
    )
    
    args = parser.parse_args()
    
    try:
        decode_image_to_file(
            args.input_image,
            args.output_file,
            args.method
        )
    except Exception as e:
        sys.exit(1)


if __name__ == "__main__":
    main()
