#!/bin/bash
# Guide students to set values for x, y, z
echo "Please edit this script to set values for x, y, z:"
echo "x: scale factor (e.g., 2.0)"
echo "y: shear factor (e.g., 0.5)"
echo "z: rotation angle in degrees (e.g., 90)"

# Default values (students can modify)
x=${x:-2.0}
y=${y:-0.5}
z=${z:-90}

python3 - <<EOF
import cv2
import numpy as np

# Load the image
img = cv2.imread('/home/$USER/attacks/marked_flag.jpg')

# Scale the image
height, width = img.shape[:2]
scaled_img = cv2.resize(img, (int(width * $x), int(height * $x)), interpolation=cv2.INTER_LINEAR)

# Shear the scaled image
new_height, new_width = scaled_img.shape[:2]
shear_matrix = np.float32([[1, $y, 0], [0, 1, 0]])
sheared_img = cv2.warpAffine(scaled_img, shear_matrix, (new_width + int(new_height * $y), new_height))

# Rotate the scaled and sheared image
final_height, final_width = sheared_img.shape[:2]
center = (final_width / 2, final_height / 2)
rotate_matrix = cv2.getRotationMatrix2D(center, $z, 1.0)
rotated_img = cv2.warpAffine(sheared_img, rotate_matrix, (final_width, final_height))

# Save the final image in JPEG format
cv2.imwrite('/home/$USER/attacks/attacked_image.jpg', rotated_img, [int(cv2.IMWRITE_JPEG_QUALITY), 95])

print("Applied linear transformations (scale, shear, rotate) to the same image.")
EOF