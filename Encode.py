from PIL import Image

# Define the RGB values for white color
red = 255
green = 255
blue = 255

# Path to the file that contains the bytes to encode
file = r"Sample/Encode.txt"
with open(file, "rb") as f:
    file_bytes = f.read()  # Read the bytes from the file

print(f"The file is {len(file_bytes)} bytes long.")

# Get the length of the file's bytes
file_length = len(file_bytes)

# Ensure the byte length is a multiple of 3 (for RGB)
if file_length % 3 != 0:
    padding = 3 - (file_length % 3)  # Calculate the padding needed
    file_bytes += b'\x00' * padding  # Add padding (null bytes)
    file_length = len(file_bytes)  # Update the length after padding

# Set the size of the new image
size = (500, 400)

# Create a new RGB image with a white background
new_image = Image.new("RGB", size, color=(red, green, blue))

# Create pixel data from the file bytes, grouping them into RGB tuples
pixel_data = [(file_bytes[i], file_bytes[i+1], file_bytes[i+2])
              for i in range(0, len(file_bytes), 3)]

# Get the width and height of the new image
width, height = new_image.size
# Loop through the pixel data to populate the image
for i, color in enumerate(pixel_data):
    x = i % width  # Calculate the x coordinate
    y = i // width  # Calculate the y coordinate
    if y < height:
        new_image.putpixel((x, y), color)  # Set the pixel color
    else:
        break  # Stop if we've reached the end of the image

# Save the newly created image to a file
new_image.save("Sample/Encode.png")

# Print the total number of bytes written to the image
print(f"{len(pixel_data) * 3} bytes have been written to the image.")
