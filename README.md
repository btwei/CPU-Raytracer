# CPU-Raytracer
This project displays a CPU implementation of a raytracer in Python. It implements basic raytracing and a few extra features. To try this yourself, clone the repository and run a test scene or construct your own.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Contact](#contact)

## Features
- Basic Raytracing: A camera points down the +Z axis and maps rays from the on screen canvas to the viewport. These rays are traced for intersections and their points are lit accordingly.
- Primatives: Rays can collide with basic primitives. Currently, only spheres are implemented. With each primitive, ray-primitive intersections need to be handled correctly.
- Light & Shadows: Light comes from point, directional, and ambient sources. These sources are used to calculate specular and diffuse light components depending on the primative's material. When lighting is calculated, rays are traced back to their light sources to check for shadows.
- Reflections: Some materials, like mirrors in real life, get most of their color from their surroundings. This is implemented by recursively reflecting rays on mirror-like surfaces. To prevent infinite recursion, a depth is set, which limits the reflections to an integer amount.
- Custom Inputs and File Handling: This python script takes a file input to define the scene. See more under usage.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/btwei/CPU-Rasterizer.git
    ```
2. Navigate to the project directory:
    ```bash
    cd CPU-Rasterizer
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
```
python3 Raytracer.py input.txt
```

Input files are defined line by line with keywords followed by parameters:

png
Usage: png width height filename

viewport
Usage: viewport vp_width vp_height

sphere
Usage: sphere x y z radius r g b a specularity reflectivity
Notes: rgba range 0-255, reflectivity ranges 0(non-reflective) to 1(perfect mirror), and specularity scales exponentially over (0, infinity), use -1 to disable specularity

directional_light
Usage: directional_light i x y z

point_light
Usage: point_light i x y z

ambient_light
Usage: ambient_light i

recursion_depth
Usage: recusion_depth depth

## Examples
![example1.png](/examples/example1.png)

## Contact
Ben Wei - [ben.stwei@gmail.com](mailto:ben.stwei@gmail.com)

Project Link: [https://github.com/btwei/CPU-Raytracer](https://github.com/btwei/CPU-Raytracer)