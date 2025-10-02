# File to Image Encoder/Decoder

A Python application that encodes binary data from any file into an image and decodes it back to its original form. The encoding process converts file bytes into RGB pixel values, while the decoding process extracts the original data from the image pixels.

## 🚀 Features

- **Universal File Support**: Encode any type of file (text, binary, images, documents, etc.) into an image
- **Lossless Encoding**: Perfect reconstruction of original files with no data loss
- **Smart Decoding**: Automatic detection of encoded data boundaries
- **Flexible Image Dimensions**: Auto-calculation of optimal image size or manual specification
- **Command-Line Interface**: Easy-to-use CLI with comprehensive options
- **Error Handling**: Robust error checking and informative error messages
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 📋 Prerequisites

- Python 3.8 or higher
- Pillow (Python Imaging Library)

## 🔧 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/file-to-image.git
   cd file-to-image
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   Or install Pillow directly:
   ```bash
   pip install Pillow
   ```

## 💻 Usage

### Basic Usage

**Encode a file to image:**
```bash
python Encode.py input.txt output.png
```

**Decode image back to file:**
```bash
python Decode.py encoded.png decoded.txt
```

### Advanced Usage

**Encode with specific dimensions:**
```bash
python Encode.py data.bin image.png --width 800 --height 600
```

**Decode with smart detection:**
```bash
python Decode.py image.png output.bin --method smart
```

**Use default sample files:**
```bash
python Encode.py    # Uses Sample/Encode.txt → Sample/Encode.png
python Decode.py    # Uses Sample/Encode.png → Sample/Decode.txt
```

### Command-Line Options

#### Encode.py Options
- `input_file`: Path to the file to encode (default: Sample/Encode.txt)
- `output_image`: Path for the output image (default: Sample/Encode.png)  
- `--width WIDTH`: Specify image width (auto-calculated if not provided)
- `--height HEIGHT`: Specify image height (auto-calculated if not provided)
- `--version`: Show version information

#### Decode.py Options
- `input_image`: Path to the image to decode (default: Sample/Encode.png)
- `output_file`: Path for the output file (default: Sample/Decode.txt)
- `--method METHOD`: Decoding method ('count' or 'smart', default: 'smart')
- `--version`: Show version information

### Decoding Methods

- **smart**: Finds the last non-white pixel for accurate data boundary detection (recommended)
- **count**: Counts all non-white pixels (legacy method, may include extra padding)

## 📁 Project Structure

```
file-to-image/
├── Encode.py           # Main encoding script
├── Decode.py           # Main decoding script
├── requirements.txt    # Python dependencies
├── README.md          # Project documentation
├── LICENSE            # License file
├── .gitignore         # Git ignore rules
├── tests/             # Unit tests
│   ├── test_encode.py
│   ├── test_decode.py
│   └── test_data/
└── Sample/            # Sample files for testing
    ├── Encode.txt     # Sample input file
    ├── Encode.png     # Encoded image output
    └── Decode.txt     # Decoded output file
```

## 🔬 How It Works

### Encoding Process
1. **File Reading**: Read the input file as binary data
2. **Padding**: Add null bytes if needed to make the data length divisible by 3
3. **RGB Conversion**: Group bytes into sets of 3, treating each set as RGB values (0-255)
4. **Image Creation**: Create an image with white background and set pixels to the RGB values
5. **Dimension Calculation**: Auto-calculate optimal dimensions or use provided values
6. **Image Saving**: Save the resulting image in PNG format

### Decoding Process
1. **Image Loading**: Open and validate the encoded image
2. **Data Detection**: Find pixels containing encoded data (non-white pixels)
3. **RGB Extraction**: Extract RGB values from each data pixel
4. **Byte Reconstruction**: Convert RGB values back to individual bytes
5. **Padding Removal**: Remove null byte padding added during encoding
6. **File Writing**: Write the reconstructed bytes to the output file

## 🧪 Testing

The project includes comprehensive tests to ensure reliability:

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test files
python -m pytest tests/test_encode.py -v
python -m pytest tests/test_decode.py -v

# Test with the included sample
python Encode.py Sample/Encode.txt Sample/Test.png
python Decode.py Sample/Test.png Sample/Test.txt
# Compare Sample/Encode.txt and Sample/Test.txt - they should be identical
```

## 📊 Capacity and Limitations

- **Image Capacity**: Each pixel can store 3 bytes of data
- **Maximum File Size**: Limited by maximum image dimensions (e.g., 10,000 x 10,000 = 300MB capacity)
- **Supported Formats**: Output images are saved as PNG to preserve exact pixel values
- **File Types**: Any file type can be encoded (binary data is treated universally)

## 🔍 Example Use Cases

- **Data Hiding**: Embed data in images for steganography-like applications
- **File Backup**: Convert files to image format for unique storage solutions
- **Data Transmission**: Send files through image-sharing platforms
- **Educational**: Demonstrate concepts of data encoding and binary representation
- **Art Projects**: Create visual representations of data/files

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational and legitimate purposes only. Users are responsible for complying with applicable laws and regulations when using this software.

## 🐛 Known Issues

- Very large files may require substantial memory during processing
- Image viewers might compress or modify pixel values - always use the original PNG files for decoding

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/file-to-image/issues) page for existing solutions
2. Create a new issue if your problem hasn't been addressed
3. Provide detailed information including error messages and steps to reproduce

## 🎯 Future Enhancements

- [ ] Support for different image formats (TIFF, BMP)
- [ ] Compression options to reduce image file size
- [ ] GUI interface for non-technical users
- [ ] Batch processing capabilities
- [ ] Progress bars for large files
- [ ] Encryption options for secure data hiding
- [ ] Metadata preservation

---

**Made with ❤️ for the open source community**
