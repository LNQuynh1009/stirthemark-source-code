# -*- coding: utf-8 -*-
import numpy as np
from PIL import Image
import sys

def binary_to_text(binary):
    text = ''
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        if len(byte) == 8:
            char_code = int(byte, 2)
            text += chr(char_code)
    return text

def extract_watermark(image_path, watermark_length_bits, expected_watermark="PTIT"):
    # Load the image and convert to RGB
    img = Image.open(image_path).convert('RGB')
    img_array = np.array(img, dtype=np.uint8)
    height, width, channels = img_array.shape

    # Extract bits from the LSB of color channels
    extracted_bits = ''
    bit_index = 0
    for i in range(height):
        for j in range(width):
            if bit_index >= watermark_length_bits:
                break
            r, g, b = img_array[i, j]
            if bit_index < watermark_length_bits:
                extracted_bits += str(r & 1)
                bit_index += 1
            if bit_index < watermark_length_bits:
                extracted_bits += str(g & 1)
                bit_index += 1
            if bit_index < watermark_length_bits:
                extracted_bits += str(b & 1)
                bit_index += 1
        if bit_index >= watermark_length_bits:
            break

    # Convert bits to text
    extracted_text = binary_to_text(extracted_bits)

    # Check if the watermark is damaged
    if extracted_text == expected_watermark:
        return extracted_text, extracted_bits
    else:
        return "damaged_watermark", extracted_bits

if __name__ == "__main__":
    watermark_length_bits = 32  # "PTIT" = 4 characters x 8 bits
    image_path = sys.argv[1] if len(sys.argv) > 1 else "marked_flag.jpg"
    extracted_text, extracted_bits = extract_watermark(image_path, watermark_length_bits)
    print(extracted_text)