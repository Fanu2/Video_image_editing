from PIL import Image
import numpy as np

# Create a 256x256 image with RGB color
width, height = 1024, 1024
image = Image.new('RGB', (width, height))

# Get pixel access object
pixels = image.load()

# Iterate over its pixels
for x in range(width):
    for y in range(height):
        # Set the pixels' red value to its x position value
        # Set the pixels' green value to its y position value
        pixels[x, y] = (x, y, 0)

# Save the resulting image to a file
image.save('/home/jasvir/Music/Jacinta2/image.png')

print("Image created and saved as image.png")
