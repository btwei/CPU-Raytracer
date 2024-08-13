import argparse
import numpy as np
from PIL import Image

## Default Settings
image_width = 250
image_height = 250
output_file = 'output.png'

e = np.array([0.0, 0.0, 0.0])
d = 1.0
viewport_width = 1
viewport_height = 1

BACKGROUND_COLOR = (0,0,0,255)

## Object Types

class Sphere:
    def __init__(self, center, radius, color):
        self.center = center
        self.radius = radius
        self.color = color

spheres = []

## Function Definitions
def ScreenToViewport(x, y):
    return ((x-(image_width-1)/2)*viewport_width/(image_width-1), -1*(y-(image_height-1)/2)*viewport_height/(image_height-1), d)

def TraceRay(origin, direction, t_min, t_max):
    closest_t = np.inf
    closest_object = None

    for sphere in spheres:
        t1, t2 = IntersectRaySphere(origin, direction, sphere)
        if t_min < t1 < t_max and t1 < closest_t:
            closest_t = t1
            closest_object = sphere
        if t_min < t2 < t_max and t2 < closest_t:
            closest_t = t2
            closest_object = sphere
    
    if closest_object == None:
        return BACKGROUND_COLOR
    
    return closest_object.color

def IntersectRaySphere(origin, direction, sphere):
    OC = origin - sphere.center

    a = np.dot(direction, direction)
    b = 2*np.dot(OC, direction)
    c = np.dot(OC, OC) - sphere.radius*sphere.radius

    discriminant = b*b - 4*a*c
    if discriminant < 0:
        return np.inf, np.inf
    
    t1 = (-b + np.sqrt(discriminant)) / (2*a)
    t2 = (-b - np.sqrt(discriminant)) / (2*a)

    return t1, t2

## Main Code

image = Image.new("RGBA", (image_width, image_height), (0,0,0,0))

spheres.append(Sphere((0, 1, 3), 0.3, (60, 40, 10, 255)))
spheres.append(Sphere((-2, 0.5, 2), 1, (10, 0, 30, 255)))
spheres.append(Sphere((1, 2, 4.5), 2, (100, 0, 255, 255)))

for x in range(image_width):
    for y in range(image_height):
        direction = ScreenToViewport(x, y)
        color = TraceRay(e, direction, 1, np.inf)
        image.putpixel((x,y), color)

image.save(output_file)