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

import numba
from numba import cuda as kernel

@kernel.jit(numba.void(numba.int64, numba.float64, numba.complex128, numba.int64))
def julia(size, scale, c, iterations):
    """Julia calculation for single point, return color"""
    x = 0
    y = 0
    jx = (x - size/2.0) / (scale * 0.5 * size)
    jy = (y - size/2.0) / (scale * 0.5 * size)
    #c = complex(-0.8, 0.156)
    a = complex(jx, jy)
    color = 0x0000FF
    for i in range(iterations):
        a = a * a + c
        m = abs(a)
        if m >= 4:
            color = 0
            break

def fractal(size, scale=10.0, iterations=200):
    """Create fractal image size x size"""
    # GPU side array
    gpuPixels = cupy.empty((size, size), dtype=cupy.uint32)
    c = complex(-0.8, 0.156)
    # Copy back from GPU
    points = cupy.asnumpy(gpuPixels)
    # PIL wants individual byte elements
    pixels = points.view(dtype=np.uint8).reshape((size, size, 4))
    img = Image.fromarray(pixels, mode="RGBA")
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
