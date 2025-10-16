
""" Create Julia set fractal image.

    Written by hugo.fisher@gmail.com Canberra Australia.
    
    Released under Creative Commons CC0 Public Domain Dedication.
    This code may be freely copied and modified for any purpose
"""

import sys, time
from complex import ComplexSIMD
from memory import UnsafePointer
from python import Python

import gpu
from gpu.host import DeviceContext, DeviceAttribute, HostBuffer, DeviceBuffer
from gpu.id import block_dim, block_idx, thread_idx

alias Complex32 = ComplexSIMD[DType.float32, 1]

fn julia(pixels: UnsafePointer[UInt32], size: Float32, scale: Float32, iterations: Int):
    x: Float32 = block_idx.x * block_dim.x + thread_idx.x;
    y: Float32 = block_idx.y;
    jx: Float32 = (x - size/2.0) / (scale * 0.5 * size)
    jy: Float32 = (y - size/2.0) / (scale * 0.5 * size)
    c: Complex32 = Complex32(-0.8, 0.156)
    a: Complex32 = Complex32(jx, jy)
    rgb: UInt32 = 0xFF0000FF;
    for _ in range(iterations):
        a = a * a + c
        var m: Float32 = a.norm()
        if m >= 4:
            rgb = 0x000000;
            break;
    idx: Int = Int(y) * Int(size) + Int(x);
    pixels[idx] = rgb;

fn fractal(ctx: DeviceContext, size: Int, iterations: Int) raises -> HostBuffer[DType.uint32]:
    # CPU side array for result
    hostPix = ctx.enqueue_create_host_buffer[DType.uint32](size * size)
    # GPU side config
    pix = ctx.enqueue_create_buffer[DType.uint32](size * size)
    kernel = ctx.compile_function_checked[julia, julia]()
    # How many threads? Should be at least 1024
    nBlocks: Int = 1
    maxThread = ctx.get_attribute(DeviceAttribute.MAX_THREADS_PER_BLOCK) # 1024
    while size // nBlocks > maxThread:
        nBlocks += 1
    for i in range(iterations):
        print(i + 1)
        ctx.enqueue_function_checked(kernel, pix, Float32(size), Float32(10.0), 200,
                grid_dim=(nBlocks, size),
                block_dim=size // nBlocks)
        ctx.enqueue_copy(dst_buf=hostPix, src_buf=pix)
        ctx.synchronize()
    return hostPix


def main():
    # Need a GPU
    # Don't make this @parameter: that tests at compile time, not runtime
    if sys.has_accelerator():
        ctx = DeviceContext()
        print("GPU:", ctx.name())
    else:
        raise Error("No accelerator")
    # Need Pillow
    Image = Python.import_module("PIL.Image")
    # Setup
    size = 4096 # 1024
    args = sys.argv()
    if len(args) > 1:
        N = Int(args[1])
    else:
        N = 10
    # Just measure fractal creation
    timeBase = time.perf_counter()
    pix = fractal(ctx, size, N)
    now = time.perf_counter()
    niceStr = Python.str("Average generate time {:4.3f} secs")
    print(niceStr.format((now - timeBase)/N))
    # Create image from last fractal
    fName = "./fractal.png"
    img = Image.new("RGB", Python.tuple(size, size), "white")
    # Convert HostBuffer values to Python. Really slow :-(
    pixelData = Python.list()
    for i in range(len(pix)):
        pixelData.append(pix[i])
    img.putdata(pixelData)
    img.save(fName)
    print("Saved to", fName)
