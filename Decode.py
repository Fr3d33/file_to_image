from PIL import Image

image = Image.open("Sample/Encode.png")

width, height = image.size

header_bytes = bytearray()
for i in range(4):
    x = i % width
    y = i // width
    r, g, b = image.getpixel((x, y))
    header_bytes.extend([r, g, b])

# Berechne file_length basierend auf Bildgröße und Pixelanzahl
total_pixels = width * height
file_length = min(total_pixels * 3 - 12, 182)  # 12 Bytes für das Header-Segment

# Prüfen, ob file_length durch 3 teilbar ist
if file_length % 3 != 0:
    file_length -= file_length % 3  # auf die nächste kleinere durch 3 teilbare Zahl runden

decoded_bytes = []

for i in range(4, (file_length // 3) + 4):
    x = i % width
    y = i // width
    if y < height:
        r, g, b = image.getpixel((x, y))
        decoded_bytes.extend([r, g, b])
    else:
        break

# Nur die ersten file_length Bytes verwenden
decoded_bytes = bytes(decoded_bytes[:file_length])

with open("Sample/Decode.txt", "wb") as f:
    f.write(decoded_bytes)

print("Decodierung abgeschlossen, Datei gespeichert.")
