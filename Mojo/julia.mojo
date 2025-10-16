
""" Create Julia set fractal image.

    Written by hugo.fisher@gmail.com Canberra Australia.
    
    Released under Creative Commons CC0 Public Domain Dedication.
    This code may be freely copied and modified for any purpose
"""

import sys, time
from complex import ComplexSIMD
from python import Python

alias Complex32 = ComplexSIMD[DType.float32, 1]

fn julia(x: Float32, y: Float32, size: Float32, scale: Float32, iterations: Int) -> UInt32:
    var jx: Float32 = (x - size/2.0) / (scale * 0.5 * size)
    var jy: Float32 = (y - size/2.0) / (scale * 0.5 * size)
    var c: Complex32 = Complex32(-0.8, 0.156)
    var a: Complex32 = Complex32(jx, jy)
    for _ in range(iterations):
        a = a * a + c
        var m: Float32 = a.norm()
        if m >= 4:
            return 0
    return 0x0000FF

fn fractal(mut pixels: List[UInt32], size: Int):
    for y in range(size):
        for x in range(size):
            pixels[y * size + x] = julia(x, y, size, 10, 200)

def main():
    # Need Pillow
    Image = Python.import_module("PIL.Image")
    # Setup
    size = 4096 # 1024
    args = sys.argv()
    if len(args) > 1:
        N = Int(args[1])
    else:
        N = 10
    var pix: List[UInt32] = [0 for _ in range(size * size)]
    # Just measure fractal creation
    timeBase = time.perf_counter()
    for i in range(N):
        print(i + 1)
        fractal(pix, size)
    now = time.perf_counter()
    niceStr = Python.str("Average generate time {:4.3f} secs")
    print(niceStr.format((now - timeBase)/N))
    # Create image from last fractal
    fName = "./fractal.png"
    img = Image.new("RGB", Python.tuple(size, size), "white")
    img.putdata(Python.list(pix))
    img.save(fName)
    print("Saved to", fName)
