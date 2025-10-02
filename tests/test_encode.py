#!/usr/bin/env python3
"""
Unit tests for the Encode.py module.
"""

import os
import tempfile
import unittest
from unittest.mock import patch
from PIL import Image
import sys
import shutil

# Add the project root to the path to import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Encode import encode_file_to_image, calculate_optimal_dimensions


class TestEncode(unittest.TestCase):
    """Test cases for the encoding functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "test_input.txt")
        self.test_image = os.path.join(self.test_dir, "test_output.png")
        
        # Create a test file
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("Hello, World! This is a test file for encoding.")

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_calculate_optimal_dimensions(self):
        """Test the optimal dimension calculation."""
        # Test small file
        width, height = calculate_optimal_dimensions(30)  # 30 bytes = 10 pixels needed
        self.assertGreaterEqual(width * height, 10)
        
        # Test larger file
        width, height = calculate_optimal_dimensions(3000)  # 3000 bytes = 1000 pixels needed
        self.assertGreaterEqual(width * height, 1000)
        
        # Test with constraints
        width, height = calculate_optimal_dimensions(1000000, max_width=500, max_height=500)
        self.assertLessEqual(width, 500)
        self.assertLessEqual(height, 500)

    def test_encode_basic_functionality(self):
        """Test basic encoding functionality."""
        encode_file_to_image(self.test_file, self.test_image)
        
        # Check that the output image was created
        self.assertTrue(os.path.exists(self.test_image))
        
        # Check that it's a valid image
        with Image.open(self.test_image) as img:
            self.assertEqual(img.mode, "RGB")
            self.assertGreater(img.width, 0)
            self.assertGreater(img.height, 0)

    def test_encode_with_dimensions(self):
        """Test encoding with specific dimensions."""
        width, height = 100, 50
        encode_file_to_image(self.test_file, self.test_image, width, height)
        
        with Image.open(self.test_image) as img:
            self.assertEqual(img.width, width)
            self.assertEqual(img.height, height)

    def test_encode_empty_file(self):
        """Test encoding an empty file."""
        empty_file = os.path.join(self.test_dir, "empty.txt")
        with open(empty_file, "w") as f:
            pass  # Create empty file
        
        with self.assertRaises(ValueError):
            encode_file_to_image(empty_file, self.test_image)

    def test_encode_nonexistent_file(self):
        """Test encoding a non-existent file."""
        nonexistent = os.path.join(self.test_dir, "nonexistent.txt")
        
        with self.assertRaises(FileNotFoundError):
            encode_file_to_image(nonexistent, self.test_image)

    def test_encode_binary_data(self):
        """Test encoding binary data."""
        binary_file = os.path.join(self.test_dir, "binary.dat")
        binary_data = bytes(range(256))  # All possible byte values
        
        with open(binary_file, "wb") as f:
            f.write(binary_data)
        
        encode_file_to_image(binary_file, self.test_image)
        
        # Verify the image was created and has the right size
        self.assertTrue(os.path.exists(self.test_image))
        with Image.open(self.test_image) as img:
            self.assertGreater(img.width * img.height, len(binary_data) // 3)

    def test_encode_padding(self):
        """Test that padding is handled correctly."""
        # Create a file with length not divisible by 3
        test_data = b"AB"  # 2 bytes, should be padded to 3
        padded_file = os.path.join(self.test_dir, "padded.dat")
        
        with open(padded_file, "wb") as f:
            f.write(test_data)
        
        encode_file_to_image(padded_file, self.test_image, 10, 10)
        
        # Check that encoding succeeded
        self.assertTrue(os.path.exists(self.test_image))
        
        # Verify the first pixel contains our data plus padding
        with Image.open(self.test_image) as img:
            first_pixel = img.getpixel((0, 0))
            self.assertEqual(first_pixel[0], ord('A'))  # 65
            self.assertEqual(first_pixel[1], ord('B'))  # 66
            self.assertEqual(first_pixel[2], 0)        # Padding

    def test_file_too_large_for_dimensions(self):
        """Test error when file is too large for given dimensions."""
        large_file = os.path.join(self.test_dir, "large.txt")
        
        # Create a file with 100 characters (100 bytes)
        with open(large_file, "w") as f:
            f.write("A" * 100)
        
        # Try to encode into a 1x1 image (capacity: 3 bytes)
        with self.assertRaises(ValueError):
            encode_file_to_image(large_file, self.test_image, 1, 1)


if __name__ == "__main__":
    unittest.main()