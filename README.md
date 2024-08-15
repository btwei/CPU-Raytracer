# IN PROGRESS CPU-Raytracer
This project showcases a CPU implementation of a raytracer in Python. It implements basic raytracing and a few extra bells and whistles. To try this yourself, clone the repository and run a test scene or construct your own.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Contact](#contact)

## Features
- Basic Raytracing: A camera points down the +Z axis and maps rays from a canvas of image_width by image_height to a viewport of viewport_width by viewport height, located d distance away from the camera on the Z axis.
- Primatives: Rays can collide with basic primitives. Currently, only spheres are implemented.
- Light & Shadows: Point lights, directional lights, and ambient light sources are implemented. When lighting is calculated, rays are traced back to their light sources to check for shadows.
- Reflections: 
- Custom Inputs and File Handling: 

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
    make install
    ```

## Usage
To run the application,

## Examples

## Contact
Ben Wei - [ben.stwei@gmail.com](mailto:ben.stwei@gmail.com)

Project Link: [https://github.com/btwei/CPU-Raytracer](https://github.com/btwei/CPU-Raytracer)