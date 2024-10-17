from PIL import Image

image_path = 'Sample/Encode.png'  # Pfad zu deinem Bild
image = Image.open("Sample/Encode.png")

def count_non_white_pixels(image):
    width, height = image.size
    non_white_pixel_count = 0
    image = image.convert("RGB")

    for x in range(width):
        for y in range(height):
            r, g, b = image.getpixel((x, y))
            if (r, g, b) != (255, 255, 255):
                non_white_pixel_count += 1

    return non_white_pixel_count

non_white_pixels = count_non_white_pixels(image)

width, height = image.size

file_length = non_white_pixels * 3

decoded_bytes = []

for i in range(file_length // 3):
    x = i % width
    y = i // width
    if y < height:
        r, g, b = image.getpixel((x, y))
        decoded_bytes.extend([r, g, b])
    else:
        break

decoded_bytes = bytes(decoded_bytes)

decoded_bytes = decoded_bytes.rstrip(b'\x00')

with open("Sample/Decode.txt", "wb") as f:
    f.write(decoded_bytes)

print(non_white_pixels)
print("Decodierung abgeschlossen, Datei gespeichert.")
