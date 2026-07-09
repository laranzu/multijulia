#!/usr/bin/env python

""" Create Julia set fractal image, CUDA Python

    Written by hugo.fisher@gmail.com Canberra Australia.
    
    Released under Creative Commons CC0 Public Domain Dedication.
    This code may be freely copied and modified for any purpose
"""

import math, sys, time

import PIL
from PIL import Image

import numpy as np

import cupy
from cupy import cuda
from cuda import core

import numba
from numba import cuda as kernel

@kernel.jit(numba.void(numba.uint32[:], numba.int64, numba.float64, numba.complex128, numba.int64))
def julia(points, size, scale, c, iterations):
    """Julia calculation for single point in array"""
    # Point coords
    x = kernel.blockIdx.x * kernel.blockDim.x + kernel.threadIdx.x
    y = kernel.blockIdx.y
    # Convert to origin at centre, divided by scale
    half = float(size / 2)
    jx = (float(x) - half) / (scale * half)
    jy = (float(y) - half) / (scale * half)
    # a = complex(jx, jy)
    rgba = 0xFF0000FF
    # for i in range(iterations):
    #     a = a * a + c
    #     m = abs(a)
    #     if m >= 4:
    #         color = 0
    #         break
    idx = y * size + x
    points[idx] = rgba

def fractal(gpu, size, scale=10.0, iterations=200):
    """Create fractal image size x size"""
    # GPU side array
    gpuPoints = cupy.empty(size * size, dtype=cupy.uint32)
    # One or more blocks per row
    maxThread = gpu.properties.max_threads_per_block
    perRow = int(math.ceil(size / maxThread))
    # Invoke and wait for result
    c = complex(-0.8, 0.156)
    julia[(perRow, size), maxThread](gpuPoints, size, scale, c, iterations)
    kernel.synchronize()
    # Copy back from GPU
    points = cupy.asnumpy(gpuPoints)
    # PIL wants individual byte elements
    pixels = points.view(dtype=np.uint8).reshape((size, size, 4))
    img = Image.fromarray(pixels, mode="RGBA")
    return img

def main(argv):
    # Need a GPU
    if core.system.get_num_devices() > 0:
        gpu = core.Device(0)
        print("GPU {}".format(gpu.name))
        gpu.set_current()
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
        img = fractal(gpu, size)
    now = time.time()
    print("Average generate time {:4.3f} secs".format((now - timeBase)/N))
    # Save last fractal for checking
    fName = "./fractal.png"
    img.save(fName)
    print("Saved to {}".format(fName))

if __name__ == "__main__":
    main(sys.argv)
