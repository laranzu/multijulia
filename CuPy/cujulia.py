#!/usr/bin/env python

""" Create Julia set fractal image, CUDA Python

    Written by hugo.fisher@gmail.com Canberra Australia.
    
    Released under Creative Commons CC0 Public Domain Dedication.
    This code may be freely copied and modified for any purpose
"""

import sys, time

import PIL
from PIL import Image

import numpy as np

import cupy
from cupy import cuda
from cuda import core

def fractal(size):
    """Create fractal image size x size"""
    img = Image.new("RGB", (size, size), "white")
    # pixels = img.load()
    # for y in range(size):
    #     for x in range(size):
    #         pixels[(x, y)] = julia(x, y, size, 10, 200)
    return img

def main(argv):
    # Need a GPU
    if core.system.get_num_devices() > 0:
        dev = core.Device(0)
        print("GPU {}".format(dev.name))
        dev.set_current()
    else:
        raise RuntimeError("Requires CUDA GPU")
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
