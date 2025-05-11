# -*- coding: utf-8 -*-
import numpy as np
from PIL import Image
import sys

def text_to_binary(text):
    binary = ''
    for char in text:
        binary += format(ord(char), '08b')
    return binary

# Function to embed watermark into the image
def embed_watermark(image_path, watermark, output_path):
    # Load the image and convert to RGB
    img = Image.open(image_path).convert('RGB')
    img_array = np.array(img, dtype=np.uint8)
    height, width, channels = img_array.shape

    # Convert watermark to binary
    watermark_bits = text_to_binary(watermark)
    bit_index = 0

    # Embed bits into the LSB of color channels
    for i in range(height):
        for j in range(width):
            if bit_index >= len(watermark_bits):
                break
            r, g, b = img_array[i, j]
            if bit_index < len(watermark_bits):
                r = (r & 0xFE) | int(watermark_bits[bit_index])
                bit_index += 1
            if bit_index < len(watermark_bits):
                g = (g & 0xFE) | int(watermark_bits[bit_index])
                bit_index += 1
            if bit_index < len(watermark_bits):
                b = (b & 0xFE) | int(watermark_bits[bit_index])
                bit_index += 1
            img_array[i, j] = (r, g, b)
        if bit_index >= len(watermark_bits):
            break

    # Save the image with embedded watermark in JPEG format
    img = Image.fromarray(img_array)
    img.save(output_path, format='JPEG', quality=95)  # Set quality to 95 to reduce loss
    print("Watermark embedded successfully!")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python embed.py <image_path> <watermark> <output_path>")
        sys.exit(1)
    image_path = sys.argv[1]  # Get image path from command line argument
    watermark = sys.argv[2]   # Get watermark text from command line argument
    output_path = sys.argv[3] # Get output path from command line argument
    embed_watermark(image_path, watermark, output_path)