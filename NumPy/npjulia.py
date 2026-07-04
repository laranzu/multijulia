#!/usr/bin/env python

""" Create Julia set fractal image, using Numpy.

    Written by hugo.fisher@gmail.com Canberra Australia.
    
    Released under Creative Commons CC0 Public Domain Dedication.
    This code may be freely copied and modified for any purpose
"""

import sys, time

import numpy as np

import PIL
from PIL import Image

def makeGrid(size, scale):
    """Create 2D array for fractal calculation"""
    # Initial array of complex numbers. Real part is
    # X coord divided by scale, imaginary from Y
    def base(v):
        return (v - size/2.0) / (scale * 0.5 * size)
    # Can create 2D array by multiplying row, column vectors
    varying = np.linspace(base(0), base(size - 1), size, dtype=np.double)
    fixed = np.ndarray(size, dtype=np.double)
    fixed.fill(1.0)
    # Generate separate real and imaginary
    rGrid = varying.reshape((size, 1)) * fixed.reshape((1, size))
    iGrid = fixed.reshape((size, 1)) * varying.reshape((1, size))
    # Combine
    grid = rGrid + iGrid * complex(0, 1)
    return grid

JULIA_LIMIT = 4.0

def julia(grid, c, iterations):
    """Julia calculation over grid"""
    for i in range(iterations):
        # Stop calculating point when value reaches 4
        mask = np.abs(grid) < JULIA_LIMIT
        grid[mask]= np.square(grid[mask]) + c
    return grid

def fractal(size, scale=10.0, iterations=200):
    """Generate fractal image size x size pixels"""
    # Fractal math
    grid = makeGrid(size, scale)
    c = complex(-0.8, 0.156)
    grid = julia(grid, c, iterations)
    # Image
    # Start with 2D array of ABGR values
    points = np.ndarray((size, size), dtype=np.uint32)
    points.fill(0xFF000000) # Solid black
    # Color points from last generation
    mask = np.abs(grid) < JULIA_LIMIT
    points[mask] = 0xFF0000FF
    # PIL wants individual byte elements
    pixels = points.view(dtype=np.uint8).reshape((size, size, 4))
    img = Image.fromarray(pixels, mode="RGBA")
    return img

def main(argv):
    # Setup
    size = 1024 # 4096
    if len(argv) > 1:
        N = int(argv[1])
    else:
        N = 10
    # Just measure fractal creation
    timeBase = time.time()
    for i in range(N):
        print(i + 1)
        img = fractal(size)
    now = time.time()
    print("Average generate time {:4.3f} secs".format((now - timeBase)/N))
    # Save last fractal for checking
    fName = "./fractal.png"
    img.save(fName)
    print("Saved to {}".format(fName))

if __name__ == "__main__":
    main(sys.argv)
