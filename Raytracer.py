import argparse
import numpy as np
from PIL import Image

# Default Settings
image_width = 20
image_height = 30
output_file = 'output.png'

e = np.array([0.0, 0.0, 0.0])
d = 1.0
viewport_width = 1
viewport_height = 1

# Function Definitions
def ScreenToViewport(x, y):
    pass

# Main Code

image = Image.new("RGBA", (image_width, image_height), (0,0,0,0))

for x in range(image_width):
    for y in range(image_height):
        image.putpixel((x,y), (0, 255, 255, 255))

image.save(output_file)