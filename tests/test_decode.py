#!/usr/bin/env python3
"""
Unit tests for the Decode.py module.
"""

import os
import tempfile
import unittest
from PIL import Image
import sys
import shutil

# Add the project root to the path to import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Decode import decode_image_to_file, count_non_white_pixels, find_data_end_smart
from Encode import encode_file_to_image


class TestDecode(unittest.TestCase):
    """Test cases for the decoding functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "test_input.txt")
        self.test_image = os.path.join(self.test_dir, "test_encoded.png")
        self.decoded_file = os.path.join(self.test_dir, "decoded.txt")
        
        # Create test data
        self.test_data = "Hello, World! This is a test for round-trip encoding/decoding."
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write(self.test_data)

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_count_non_white_pixels(self):
        """Test counting non-white pixels in an image."""
        # Create a simple test image
        img = Image.new("RGB", (10, 10), color=(255, 255, 255))  # All white
        self.assertEqual(count_non_white_pixels(img), 0)
        
        # Add some non-white pixels
        img.putpixel((0, 0), (255, 0, 0))  # Red pixel
        img.putpixel((1, 0), (0, 255, 0))  # Green pixel
        img.putpixel((2, 0), (0, 0, 255))  # Blue pixel
        
        self.assertEqual(count_non_white_pixels(img), 3)

    def test_find_data_end_smart(self):
        """Test smart detection of data end."""
        # Create a test image with some data pixels
        img = Image.new("RGB", (10, 10), color=(255, 255, 255))  # All white
        
        # Add data pixels
        img.putpixel((0, 0), (100, 100, 100))
        img.putpixel((1, 0), (200, 200, 200))
        img.putpixel((5, 3), (50, 150, 250))  # Last data pixel
        
        # The smart method should find 3 pixels, with the last one being at position (5,3)
        # Position (5,3) in a 10-wide image = 3*10 + 5 = 35, so count should be 36
        data_pixels = find_data_end_smart(img)
        self.assertEqual(data_pixels, 36)

    def test_round_trip_encoding_decoding(self):
        """Test complete round-trip: encode then decode."""
        # Encode the test file
        encode_file_to_image(self.test_file, self.test_image)
        
        # Decode it back
        decode_image_to_file(self.test_image, self.decoded_file, method="smart")
        
        # Compare original and decoded content
        with open(self.test_file, "r", encoding="utf-8") as f:
            original = f.read()
        
        with open(self.decoded_file, "r", encoding="utf-8") as f:
            decoded = f.read()
        
        self.assertEqual(original, decoded)

    def test_decode_count_method(self):
        """Test decoding with count method."""
        # Encode then decode with count method
        encode_file_to_image(self.test_file, self.test_image)
        decode_image_to_file(self.test_image, self.decoded_file, method="count")
        
        # Verify the content matches
        with open(self.test_file, "rb") as f:
            original = f.read()
        
        with open(self.decoded_file, "rb") as f:
            decoded = f.read()
        
        self.assertEqual(original, decoded)

    def test_decode_smart_method(self):
        """Test decoding with smart method."""
        # Encode then decode with smart method
        encode_file_to_image(self.test_file, self.test_image)
        decode_image_to_file(self.test_image, self.decoded_file, method="smart")
        
        # Verify the content matches
        with open(self.test_file, "rb") as f:
            original = f.read()
        
        with open(self.decoded_file, "rb") as f:
            decoded = f.read()
        
        self.assertEqual(original, decoded)

    def test_decode_nonexistent_image(self):
        """Test decoding a non-existent image."""
        nonexistent = os.path.join(self.test_dir, "nonexistent.png")
        
        with self.assertRaises(FileNotFoundError):
            decode_image_to_file(nonexistent, self.decoded_file)

    def test_decode_invalid_image(self):
        """Test decoding an invalid image file."""
        invalid_image = os.path.join(self.test_dir, "invalid.png")
        
        # Create a file that's not a valid image
        with open(invalid_image, "w") as f:
            f.write("This is not an image file")
        
        with self.assertRaises(ValueError):
            decode_image_to_file(invalid_image, self.decoded_file)

    def test_decode_all_white_image(self):
        """Test decoding an image with no encoded data (all white)."""
        # Create an all-white image
        white_image = Image.new("RGB", (100, 100), color=(255, 255, 255))
        white_image.save(self.test_image)
        
        with self.assertRaises(ValueError):
            decode_image_to_file(self.test_image, self.decoded_file)

    def test_decode_binary_data(self):
        """Test round-trip with binary data."""
        # Create binary test data
        binary_file = os.path.join(self.test_dir, "binary.dat")
        binary_data = bytes(range(100))  # 100 bytes of binary data
        
        with open(binary_file, "wb") as f:
            f.write(binary_data)
        
        # Encode and decode
        encode_file_to_image(binary_file, self.test_image)
        decode_image_to_file(self.test_image, self.decoded_file)
        
        # Compare
        with open(binary_file, "rb") as f:
            original = f.read()
        
        with open(self.decoded_file, "rb") as f:
            decoded = f.read()
        
        self.assertEqual(original, decoded)

    def test_decode_with_padding(self):
        """Test decoding data that required padding during encoding."""
        # Create data with length not divisible by 3
        padded_file = os.path.join(self.test_dir, "padded.dat")
        padded_data = b"AB"  # 2 bytes
        
        with open(padded_file, "wb") as f:
            f.write(padded_data)
        
        # Encode and decode
        encode_file_to_image(padded_file, self.test_image)
        decode_image_to_file(self.test_image, self.decoded_file)
        
        # Original data should be recovered exactly (padding should be removed)
        with open(self.decoded_file, "rb") as f:
            decoded = f.read()
        
        self.assertEqual(decoded, padded_data)

    def test_decode_large_file(self):
        """Test round-trip with a larger file."""
        # Create a larger test file
        large_file = os.path.join(self.test_dir, "large.txt")
        large_data = "A" * 1000  # 1000 characters
        
        with open(large_file, "w", encoding="utf-8") as f:
            f.write(large_data)
        
        # Encode and decode
        encode_file_to_image(large_file, self.test_image)
        decode_image_to_file(self.test_image, self.decoded_file)
        
        # Verify
        with open(large_file, "r", encoding="utf-8") as f:
            original = f.read()
        
        with open(self.decoded_file, "r", encoding="utf-8") as f:
            decoded = f.read()
        
        self.assertEqual(original, decoded)


if __name__ == "__main__":
    unittest.main()