#!/usr/bin/env python3

from PIL import Image

# Path to the image that needs to be decoded
image_path = 'Sample/Encode.png'
image = Image.open(image_path)

def count_non_white_pixels(image):
    # Get the dimensions of the image (width and height)
    width, height = image.size
    non_white_pixel_count = 0
    image = image.convert("RGB")  # Ensure the image is in RGB format

    # Loop through each pixel in the image
    for x in range(width):
        for y in range(height):
            r, g, b = image.getpixel((x, y))  # Get the RGB values of the pixel
            # Check if the pixel is not white
            if (r, g, b) != (255, 255, 255):
                non_white_pixel_count += 1

    return non_white_pixel_count

# Get the count of non-white pixels in the image
non_white_pixels = count_non_white_pixels(image)

# Get the image dimensions again for decoding purposes
width, height = image.size

# Calculate the file length based on the number of non-white pixels (3 bytes per pixel)
file_length = non_white_pixels * 3

decoded_bytes = []

# Loop through the image data to decode the bytes
for i in range(file_length // 3):
    x = i % width  # Column position
    y = i // width  # Row position
    if y < height:
        r, g, b = image.getpixel((x, y))  # Get the RGB values
        decoded_bytes.extend([r, g, b])  # Add them to the decoded bytes list
    else:
        break  # Stop if we've reached the end of the image

# Convert the decoded list of values into a bytes object
decoded_bytes = bytes(decoded_bytes)

# Remove any padding (null bytes) at the end of the decoded data
decoded_bytes = decoded_bytes.rstrip(b'\x00')

# Save the decoded bytes to a file
with open("Sample/Decode.txt", "wb") as f:
    f.write(decoded_bytes)

# Output the number of non-white pixels and confirm the decoding
print(non_white_pixels)
print("Decoding completed, file saved.")
