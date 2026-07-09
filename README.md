
## Julia Set generation in C++, Python, Mojo, Mojo GPU

Version 1.1 July 2026 - now with `numpy`

Written by Hugh/Hugo Fisher <br/>
AKA laranzu <br/>
Canberra, Australia <br/>
hugo.fisher@gmail.com

Released under Creative Commons CC0 Public Domain Dedication.
This code may be freely copied and modified for any purpose

Here are several programs to generate the Julia set, a fractal image.
Each of them is a command line program which generates an image N
(default 10) times, and saves the last one to a PNG file for checking.
They also report the average time to generate each image.

- Python (`py`), without any acceleration.

- Python (`NumPy`) using numpy arrays.

- Python (`CuPy`) using CUDA on GPU.

- C++ (`CPP`) again without any special libraries.

- Mojo (`Mojo`) running on the CPU.

- Mojo (`MojoGPU`) running on a GPU.

None of these programs are particularly optimised, which is the point.
This is a comparison between the same algorithm written by a competent
programmer implemented in different programs.

#### Dependencies

I have only tested these on Linux.

You will need something that displays image files, as the output is
always a file `fractal.png`

The C++ version needs `libpng-devel`. There's a Makefile, but it is only
two source files so shouldn't be hard to load into an IDE.

The Python and Mojo versions all need Pillow, the Python Image Library.
Pip install into your virtual environment, or equivalent.

The Python numpy and CUDA versions needs `numpy` as well.

#### CUDA

You need the CUDA driver, which is independent of Python. Once
installed run `nvcc --version`. Mine is 12.6.

You can then create a venv and install the corresponding version of
CuPy, in my case

    pip install cupy-cuda12x

#### Mojo

For Mojo, you can at time of development just

    pip install mojo mojo-compiler

You don't need the full MAX/Magic environment.

**However** the Mojo code was written end of 2025. Since then Modular,
the company that owns Mojo, have changed direction and declared that
now the goal is to make Mojo a system programming language and Python
source compatibility is less important.
For me, Mojo has changed from "Python but really fast" to "Rust without
curly braces" and I've given up on it. The code here might not compile
any more, and I'm not going to bother fixing it.


#### Results

My system has an Intel i7-9700 @ 3Ghz CPU and an NVIDIA RTX A2000 GPU.

1. The Python version is very slow, the C++ version is a lot faster by
more than an order of magnitude. No surprise there.

1. Python with numpy is a lot faster than Python. C++ is only three
times as fast.

1. The Mojo version, on the CPU, is faster than C++! While I didn't try to
optimise the code, I don't think it's particularly bad either. And rewriting
the C++ code to use GLM and SIMD intrinsics didn't change the performance.

1. The Mojo version on the GPU is really fast. Again not surprising,
the real lesson I learned is how easy it is to write GPU code in Mojo.
(However, converting Mojo arrays into Python for saving the PNG is very slow.)
