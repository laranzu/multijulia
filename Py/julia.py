#!/usr/bin/env python

""" Create Julia set fractal image.

    Written by hugo.fisher@gmail.com Canberra Australia.
    
    Released under Creative Commons CC0 Public Domain Dedication.
    This code may be freely copied and modified for any purpose
"""

import sys, time

import PIL
from PIL import Image

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

def fractal(pixels, size):
    for y in range(size):
        for x in range(size):
            pixels[(x, y)] = julia(x, y, size, 10, 200)

def main(argv):
    # Setup
    size = 4096 # 1024
    if len(argv) > 1:
        N = int(argv[1])
    else:
        N = 10
    # Create image from (last) fractal
    fName = "./fractal.png"
    img = Image.new("RGB", (size, size), "white")
    pix = img.load()
    # Just measure fractal creation
    timeBase = time.time()
    for i in range(N):
        print(i + 1)
        fractal(pix, size)
    now = time.time()
    print("Average generate time {:4.3f} secs".format((now - timeBase)/N))
    # Done
    img.save(fName)
    print("Saved to {}".format(fName))

if __name__ == "__main__":
    main(sys.argv)
