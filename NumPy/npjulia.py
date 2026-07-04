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

def julia(x, y, size, scale, iterations):
    jx = (x - size/2.0) / (scale * 0.5 * size)
    jy = (y - size/2.0) / (scale * 0.5 * size)
    c = complex(-0.8, 0.156)
    a = complex(jx, jy)
    for i in range(iterations):
        a = a * a + c
        m = abs(a)
        if m >= 4:
            return 0
    return 0x0000FF

def fractal(size):
    img = Image.new("RGB", (size, size), "white")
    pixels = img.load()
    for y in range(size):
        for x in range(size):
            pixels[(x, y)] = julia(x, y, size, 10, 200)
    return img

def main(argv):
    # Setup
    size = 1024 # 4096
    if len(argv) > 1:
        N = int(argv[1])
    else:
        N = 10
    grid = makeGrid(8, 10)
    print(grid)
    return
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
