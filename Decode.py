from PIL import Image

image = Image.open("Sample/Encode.png")

width, height = image.size

header_bytes = bytearray()
for i in range(4):
    x = i % width
    y = i // width
    r, g, b = image.getpixel((x, y))
    header_bytes.extend([r, g, b])

file_length = 182

decoded_bytes = []

for i in range(4, (file_length // 3) + 4):
    x = i % width
    y = i // width
    if y < height:
        r, g, b = image.getpixel((x, y))
        decoded_bytes.extend([r, g, b])
    else:
        break

print(file_length)

decoded_bytes = bytes(decoded_bytes[:file_length])

with open("Decode.txt", "wb") as f:
    f.write(decoded_bytes)