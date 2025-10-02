#!/usr/bin/env python3
"""
Integration test script for the File to Image project.
This script tests the complete workflow and various scenarios.
"""

import os
import tempfile
import shutil
import subprocess
import sys
from pathlib import Path


def run_command(cmd, description=""):
    """Run a command and return success status."""
    print(f"Running: {description or cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        print(f"✅ Success: {description}")
        return True, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {description}")
        print(f"Error: {e.stderr}")
        return False, e.stdout, e.stderr


def compare_files(file1, file2):
    """Compare two files for binary equality."""
    try:
        with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
            return f1.read() == f2.read()
    except Exception as e:
        print(f"Error comparing files: {e}")
        return False


def test_basic_functionality():
    """Test basic encoding and decoding functionality."""
    print("\n=== Testing Basic Functionality ===")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test input
        input_file = os.path.join(temp_dir, "input.txt")
        encoded_image = os.path.join(temp_dir, "encoded.png")
        decoded_file = os.path.join(temp_dir, "decoded.txt")
        
        test_content = "Hello, World! This is a test file with some content.\nLine 2\nLine 3"
        
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        # Test encoding
        success, stdout, stderr = run_command(
            f'python Encode.py "{input_file}" "{encoded_image}"',
            "Basic encoding test"
        )
        if not success:
            return False
        
        # Check if image was created
        if not os.path.exists(encoded_image):
            print("❌ Encoded image was not created")
            return False
        
        # Test decoding
        success, stdout, stderr = run_command(
            f'python Decode.py "{encoded_image}" "{decoded_file}"',
            "Basic decoding test"
        )
        if not success:
            return False
        
        # Check if decoded file was created
        if not os.path.exists(decoded_file):
            print("❌ Decoded file was not created")
            return False
        
        # Compare files
        if compare_files(input_file, decoded_file):
            print("✅ Round-trip test passed - files are identical")
            return True
        else:
            print("❌ Round-trip test failed - files differ")
            return False


def test_binary_files():
    """Test with binary files."""
    print("\n=== Testing Binary Files ===")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create binary test file
        input_file = os.path.join(temp_dir, "binary.dat")
        encoded_image = os.path.join(temp_dir, "binary_encoded.png")
        decoded_file = os.path.join(temp_dir, "binary_decoded.dat")
        
        # Create binary data (all possible byte values)
        binary_data = bytes(range(256)) * 2  # 512 bytes
        
        with open(input_file, 'wb') as f:
            f.write(binary_data)
        
        # Test encoding
        success, stdout, stderr = run_command(
            f'python Encode.py "{input_file}" "{encoded_image}"',
            "Binary file encoding"
        )
        if not success:
            return False
        
        # Test decoding
        success, stdout, stderr = run_command(
            f'python Decode.py "{encoded_image}" "{decoded_file}"',
            "Binary file decoding"
        )
        if not success:
            return False
        
        # Compare files
        if compare_files(input_file, decoded_file):
            print("✅ Binary file test passed")
            return True
        else:
            print("❌ Binary file test failed")
            return False


def test_different_sizes():
    """Test with files of different sizes."""
    print("\n=== Testing Different File Sizes ===")
    
    sizes_to_test = [1, 2, 3, 10, 100, 1000]  # Different file sizes in bytes
    
    for size in sizes_to_test:
        print(f"\nTesting {size} byte file...")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = os.path.join(temp_dir, f"size_{size}.dat")
            encoded_image = os.path.join(temp_dir, f"size_{size}_encoded.png")
            decoded_file = os.path.join(temp_dir, f"size_{size}_decoded.dat")
            
            # Create file with specific size
            test_data = b'A' * size
            
            with open(input_file, 'wb') as f:
                f.write(test_data)
            
            # Encode
            success, stdout, stderr = run_command(
                f'python Encode.py "{input_file}" "{encoded_image}"',
                f"Encoding {size} bytes"
            )
            if not success:
                return False
            
            # Decode
            success, stdout, stderr = run_command(
                f'python Decode.py "{encoded_image}" "{decoded_file}"',
                f"Decoding {size} bytes"
            )
            if not success:
                return False
            
            # Compare
            if not compare_files(input_file, decoded_file):
                print(f"❌ Size test failed for {size} bytes")
                return False
    
    print("✅ All size tests passed")
    return True


def test_custom_dimensions():
    """Test encoding with custom dimensions."""
    print("\n=== Testing Custom Dimensions ===")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        input_file = os.path.join(temp_dir, "custom_dim.txt")
        encoded_image = os.path.join(temp_dir, "custom_dim_encoded.png")
        decoded_file = os.path.join(temp_dir, "custom_dim_decoded.txt")
        
        test_content = "Testing custom dimensions!"
        
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        # Test with custom dimensions
        success, stdout, stderr = run_command(
            f'python Encode.py "{input_file}" "{encoded_image}" --width 100 --height 50',
            "Encoding with custom dimensions"
        )
        if not success:
            return False
        
        # Decode
        success, stdout, stderr = run_command(
            f'python Decode.py "{encoded_image}" "{decoded_file}"',
            "Decoding custom dimensions"
        )
        if not success:
            return False
        
        # Compare
        if compare_files(input_file, decoded_file):
            print("✅ Custom dimensions test passed")
            return True
        else:
            print("❌ Custom dimensions test failed")
            return False


def test_sample_files():
    """Test with the included sample files."""
    print("\n=== Testing Sample Files ===")
    
    if not os.path.exists("Sample/Encode.txt"):
        print("❌ Sample/Encode.txt not found")
        return False
    
    # Test with sample files
    success, stdout, stderr = run_command(
        'python Encode.py Sample/Encode.txt Sample/IntegrationTest.png',
        "Sample file encoding"
    )
    if not success:
        return False
    
    success, stdout, stderr = run_command(
        'python Decode.py Sample/IntegrationTest.png Sample/IntegrationTestDecoded.txt',
        "Sample file decoding"
    )
    if not success:
        return False
    
    # Compare
    if compare_files("Sample/Encode.txt", "Sample/IntegrationTestDecoded.txt"):
        print("✅ Sample files test passed")
        return True
    else:
        print("❌ Sample files test failed")
        return False


def test_help_and_version():
    """Test help and version commands."""
    print("\n=== Testing Help and Version Commands ===")
    
    # Test encode help
    success, stdout, stderr = run_command(
        'python Encode.py --help',
        "Encode help command"
    )
    if not success or "--help" not in stdout and "usage:" not in stdout:
        print("❌ Encode help test failed")
        return False
    
    # Test decode help  
    success, stdout, stderr = run_command(
        'python Decode.py --help',
        "Decode help command"
    )
    if not success or "--help" not in stdout and "usage:" not in stdout:
        print("❌ Decode help test failed")
        return False
    
    # Test version
    success, stdout, stderr = run_command(
        'python Encode.py --version',
        "Encode version command"
    )
    if not success or "1.0.0" not in stdout:
        print("❌ Encode version test failed")
        return False
    
    success, stdout, stderr = run_command(
        'python Decode.py --version',
        "Decode version command"
    )
    if not success or "1.0.0" not in stdout:
        print("❌ Decode version test failed")
        return False
    
    print("✅ Help and version tests passed")
    return True


def main():
    """Run all integration tests."""
    print("🚀 Starting File to Image Integration Tests")
    print("=" * 50)
    
    tests = [
        ("Basic Functionality", test_basic_functionality),
        ("Binary Files", test_binary_files),
        ("Different Sizes", test_different_sizes),
        ("Custom Dimensions", test_custom_dimensions),
        ("Sample Files", test_sample_files),
        ("Help and Version", test_help_and_version),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"Integration Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All integration tests passed!")
        return True
    else:
        print(f"💥 {total - passed} integration tests failed!")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)