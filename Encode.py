from PIL import Image

red = 200
green = 0
blue = 255

file = r"Sample/Decode.txt"
with open(file, "rb") as f:
    file_bytes = f.read()

print(f"Das file ist {len(file_bytes)} Bytes lang.")

file_length = len(file_bytes)

# Prüfen, ob die Länge durch 3 teilbar ist und ggf. auffüllen
if file_length % 3 != 0:
    padding = 3 - (file_length % 3)
    file_bytes += b'\x00' * padding
    file_length = len(file_bytes)

# Setting the size of the Image
size = (500, 400)

# Creating a new Image with RGB mode
new_image = Image.new("RGB", size, color=(red, green, blue))

# Pixel-Daten vorbereiten
pixel_data = [(file_bytes[i], file_bytes[i+1], file_bytes[i+2])
    for i in range(0, len(file_bytes), 3)]

width, height = new_image.size
for i, color in enumerate(pixel_data):
    x = i % width
    y = i // width
    if y < height:
        new_image.putpixel((x, y), color)
    else:
        break

# Saving the new Image
new_image.save("Sample/Encode.png")

print(f"Es wurden {len(pixel_data) * 3} Bytes geschrieben.")
