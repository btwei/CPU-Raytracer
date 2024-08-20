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

recursion_depth = 1

BACKGROUND_COLOR = np.array([0,0,0,255])

## Object Types

class Sphere:
    def __init__(self, center, radius, color, specularity, reflectivity):
        self.center = center
        self.radius = radius
        self.color = color
        self.specularity = specularity
        self.reflectivity = reflectivity

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
        self.type = "directional"
        self.intensity = intensity
        self.direction = np.array(direction)

lights = []

## Function Definitions
def ScreenToViewport(x, y):
    return ((x-(image_width-1)/2)*viewport_width/(image_width-1), -1*(y-(image_height-1)/2)*viewport_height/(image_height-1), d)

def TraceRay(origin, direction, t_min, t_max, recursion_depth):
    closest_object, closest_t = ClosestIntersection(origin, direction, t_min, t_max)
    
    if closest_object == None:
        return BACKGROUND_COLOR
    
    point = origin + closest_t * np.array(direction)
    # Only works with spheres
    normal = point - closest_object.center
    normal = normal / (np.sqrt(normal.dot(normal)))

    color = np.array(closest_object.color) * ComputeLighting(point, normal,-1*np.array(direction), closest_object.specularity)
    color[3] = 255

    # Is lighting done or is there a reflective component to this point?
    reflectivity = closest_object.reflectivity
    if recursion_depth <= 0 or reflectivity <= 0:
        return color

    #Compute reflective component of lighting on this point
    reflection_ray = ReflectRay(normal, -1*np.array(direction))
    reflected_color = TraceRay(point, reflection_ray, 0.001, np.inf, recursion_depth - 1)

    color = color * (1 - reflectivity) + reflected_color * reflectivity
    color[3] = 255

    return color

def ClosestIntersection(origin, direction, t_min, t_max):
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
    
    return closest_object, closest_t

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
                t_max = 1
            else:
                direction = light.direction
                t_max = np.inf

            # Check for shadows (blocking light ray), if so, skip this light source
            shadow_object, shadow_t = ClosestIntersection(point, direction, 0.001, t_max)
            if shadow_object != None:
                continue
            
            # Diffuse Reflection
            diffuse_dot = np.dot(normal, direction)
            if diffuse_dot > 0:
                intensity += light.intensity * diffuse_dot/(np.sqrt(normal.dot(normal)) * np.sqrt(direction.dot(direction)))

            # Specular Reflection
            if specularity != -1:
                reflection = ReflectRay(normal, direction)
                specular_dot = np.dot(reflection, view_angle)
                if specular_dot > 0:
                    intensity += light.intensity * np.pow(specular_dot/(np.sqrt(reflection.dot(reflection)) * np.sqrt(view_angle.dot(view_angle))), specularity)
    
    return intensity

def ReflectRay(normal, ray):
    return 2 * normal * np.dot(normal, ray) - ray

## Main Code

# Args and file i/o
parser = argparse.ArgumentParser()
parser.add_argument("inputfile", help="path to input file")
args = parser.parse_args()

f = open(args.inputfile, "r")
lines = f.readlines()

# Parse Input line by line
for line in lines:
    words = line.split()

    if(len(words) == 0): continue

    if(words[0] == "png"):
        #Usage: png width height filename
        if(len(words) < 4): continue
        image_width = int(words[1])
        image_height = int(words[2])
        output_file = words[3]
    if(words[0] == "viewport"):
        #Usage: viewport vp_width vp_height
        if(len(words) < 3): continue
        viewport_width = float(words[1])
        viewport_height = float(words[2])
    elif(words[0] == "sphere"):
        #Usage: sphere x y z radius r g b a specularity reflectivity
        spheres.append(Sphere((float(words[1]), float(words[2]), float(words[3])), float(words[4]), (float(words[5]), float(words[6]), float(words[7]), float(words[8])), float(words[9]), float(words[10])))
    elif(words[0] == "directional_light"):
        #Usage: directional_light i x y z
        if(len(words) < 5): continue
        lights.append(DirectionalLight(0.2, (1, 4, 4)))
    elif(words[0] == "point_light"):
        #Usage: point_light i x y z
        lights.append(PointLight(float(words[1]), (float(words[2]), float(words[3]), float(words[4]))))
    elif(words[0] == "ambient_light"):
        #Usage: ambient_light i
        if(len(words) < 2): continue
        lights.append(AmbientLight(float(words[1])))
    elif(words[0] == "recursion_depth"):
        if(len(words) < 2): continue
        recursion_depth = int(words[1])

print("Rendering Image.. (this can take a while, especially for larger images)")

image = Image.new("RGBA", (image_width, image_height), (0,0,0,0))

#Add Test Geometry
spheres.append(Sphere((0, -2, 10), 1, (0, 255, 0, 255), 500, 0.2))
spheres.append(Sphere((1, 0, 7), 1, (255, 0, 0, 255), 500, 0.3))
spheres.append(Sphere((-2, 0, 5), 1, (0, 0, 255, 255), 10, 0.4))
spheres.append(Sphere((0, -5001, 0), 5000, (255, 255, 255, 255), 1000, 0.5))

#Add Test Light Sources
lights.append(AmbientLight(0.2))



for x in range(image_width):
    for y in range(image_height):
        direction = ScreenToViewport(x, y)
        # Color is a np array of floats from 0 to 255
        color = TraceRay(e, direction, 1, np.inf, recursion_depth)
        # Restore color to an integer and format as a tuple for pillow
        color = tuple(np.round(color).astype(np.int64).tolist())
        image.putpixel((x,y), color)

image.save(output_file)