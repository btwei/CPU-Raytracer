import argparse
import numpy as np
from PIL import Image

## Default Settings
image_width = 1920
image_height = 1080
output_file = 'output.png'

e = np.array([0.0, 0.0, 0.0])
d = 1.0
viewport_width = 1.3333333
viewport_height = 0.75

BACKGROUND_COLOR = np.array([0,0,0,255])

## Object Types

class Sphere:
    def __init__(self, center, radius, color, specularity):
        self.center = center
        self.radius = radius
        self.color = color
        self.specularity = specularity

spheres = []

class AmbientLight():
    def __init__(self, intensity):
        self.type = "ambient"
        self.intensity = intensity

class PointLight():
    def __init__(self, intensity, position):
        self.type = "point"
        self.intensity = intensity
        self.position = position

class DirectionalLight():
    def __init__(self, intensity, direction):
        self.type = "ambient"
        self.intensity = intensity
        self.direction = direction

lights = []

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
    
    point = e + closest_t * np.array(direction)
    # Only works with spheres
    normal = point - closest_object.center
    normal = normal / (np.sqrt(normal.dot(normal)))

    color = np.array(closest_object.color) * ComputeLighting(point, normal,-1*np.array(direction), closest_object.specularity)
    color[3] = 255

    return color

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

def ComputeLighting(point, normal, view_angle, specularity):
    intensity = 0.0
    for light in lights:
        if light.type == "ambient":
            intensity += light.intensity
        else:
            if light.type == "point":
                direction = light.position - point
            else:
                direction = light.direction
            
            # Diffuse Reflection
            diffuse_dot = np.dot(normal, direction)
            if diffuse_dot > 0:
                intensity += light.intensity * diffuse_dot/(np.sqrt(normal.dot(normal)) * np.sqrt(direction.dot(direction)))

            # Specular Reflection
            if specularity != -1:
                reflection = 2 * normal * np.dot(normal, direction) - direction
                specular_dot = np.dot(reflection, view_angle)
                if specular_dot > 0:
                    intensity += light.intensity * np.pow(specular_dot/(np.sqrt(reflection.dot(reflection)) * np.sqrt(view_angle.dot(view_angle))), specularity)
    
    return intensity

## Main Code

image = Image.new("RGBA", (image_width, image_height), (0,0,0,0))

#Add Test Geometry
spheres.append(Sphere((0, -1, 3), 1, (255, 0, 0, 255), 500))
spheres.append(Sphere((2, 0, 4), 1, (0, 0, 255, 255), 500))
spheres.append(Sphere((-2, 0, 4), 1, (0, 255, 0, 255), 10))
spheres.append(Sphere((0, -5001, 0), 5000, (255, 255, 0, 255), 1000))

#Add Test Light Sources
lights.append(AmbientLight(0.2))
lights.append(PointLight(0.6, (2, 1, 0)))
lights.append(DirectionalLight(0.2, (1, 4, 4)))

for x in range(image_width):
    for y in range(image_height):
        direction = ScreenToViewport(x, y)
        # Color is a np array of floats from 0 to 255
        color = TraceRay(e, direction, 1, np.inf)
        # Restore color to an integer and format as a tuple for pillow
        color = tuple(np.round(color).astype(np.int64).tolist())
        image.putpixel((x,y), color)

image.save(output_file)