
## Julia Set generation in C++, Python, Mojo, Mojo GPU

Version 1.0 October 2025

Written by Hugh/Hugo Fisher <br/>
AKA laranzu <br/>
Canberra, Australia <br/>
hugo.fisher@gmail.com

Released under Creative Commons CC0 Public Domain Dedication.
This code may be freely copied and modified for any purpose

Here are four programs to generate the Julia set, a fractal image.
Each of them is a command line program which generates an image N
(default 10) times, and saves the last one to a PNG file for checking.
They also report the average time to generate each image.

- Python (`py`), without any acceleration.

- C++ (`CPP`) again without any special libraries.

- Mojo (`Mojo`) running on the CPU.

- Mojo (`GPU`) running on a GPU.

None of these programs are particularly optimised, which is the point.
This is a comparison between the same algorithm written by an average
programmer implemented in four different programs.

#### Dependencies

I have only tested these on Linux.

You will need something that displays image files, as the output is
always a file `fractal.png`

The C++ version needs `libpng-devel`. There's a Makefile, but it is only
two source files so shouldn't be hard to load into an IDE.

The Python and both Mojo versions need Pillow, the Python Image Library.
Pip install into your virtual environment, or equivalent.

#### Results

My system has an Intel i7-9700 @ 3Ghz CPU and an NVIDIA RTX A2000 GPU.

1. The Python version is very slow, the C++ version is a lot faster.
No surprise there.

2. The Mojo version, on the CPU, is faster than C++! While I didn't try to
optimise the code, I don't think it's particularly bad either. And rewriting
the C++ code to use GLM and SIMD intrinsics didn't change the performance.

3. The Mojo version on the GPU is really fast. Again not surprising,
the real lesson I learned is how easy it is to write GPU code in Mojo.
Mojo really is "CUDA for Python programmers" <br>
(However, converting Mojo arrays into Python for saving the PNG is very slow.)
