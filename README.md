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

Input files are processed line by line, where each line containes a keywords followed by parameters. The format for each line is as follows:

### Keywords and Usage

- **`png`**
  - **Usage:** `png width height filename`
  - **Description:** Defines the output image with the specified width, height, and filename.

- **`viewport`**
  - **Usage:** `viewport vp_width vp_height`
  - **Description:** Sets the viewport dimensions.

- **`sphere`**
  - **Usage:** `sphere x y z radius r g b a specularity reflectivity`
  - **Description:** Creates a sphere with the given center coordinates `(x, y, z)`, radius, color in RGBA, specularity, and reflectivity.
  - **Notes:**
    - `r, g, b, a`: Color values range from 0 to 255.
    - `reflectivity`: Ranges from 0 (non-reflective) to 1 (perfect mirror).
    - `specularity`: Scales exponentially over `(0, infinity)`. Use `-1` to disable specularity.

- **`directional_light`**
  - **Usage:** `directional_light i x y z`
  - **Description:** Defines a directional light with intensity `i` and direction `(x, y, z)`.

- **`point_light`**
  - **Usage:** `point_light i x y z`
  - **Description:** Specifies a point light source with intensity `i` located at `(x, y, z)`.

- **`ambient_light`**
  - **Usage:** `ambient_light i`
  - **Description:** Sets the ambient light intensity.

- **`recursion_depth`**
  - **Usage:** `recursion_depth depth`
  - **Description:** Specifies the recursion depth for rendering.

### Example Input File

```plaintext
png 800 600 output.png
viewport 1.1547 0.8660
sphere 0 0 7 0.5 0 255 0 255 10 0.8
sphere 0 1 7 0.5 255 0 0 255 10 0.5
sphere 0 -1 7 0.5 0 0 255 255 10 0
directional_light 0.4 1 0 0
point_light 0.4 5 5 0
ambient_light 0.2
recursion_depth 5
```

### Notes

- Ensure each line is formatted correctly to avoid processing errors.
- Lines starting with `#` are treated as comments and ignored by the program.

## Examples
![example1.png](/examples/example1.png)

![example2.png](/examples/example2.png)

## Contact
Ben Wei - [ben.stwei@gmail.com](mailto:ben.stwei@gmail.com)

Project Link: [https://github.com/btwei/CPU-Raytracer](https://github.com/btwei/CPU-Raytracer)