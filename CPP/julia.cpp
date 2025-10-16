
/** Create Julia set fractal image.

    Written by hugo.fisher@gmail.com Canberra Australia.
    
    Released under Creative Commons CC0 Public Domain Dedication.
    This code may be freely copied and modified for any purpose
**/

#include <stdarg.h>
#include <stdint.h>
#include <stdio.h>
#include <time.h>

#include <png.h>

#include <complex>
#include <stdexcept>

#include "fail.h"

uint32_t julia(int x, int y, int size, float scale, int iterations)
{
    float jx = (x - (size * 0.5)) / (scale * 0.5 * size);
    float jy = (y - (size * 0.5)) / (scale * 0.5 * size);
    std::complex<float> c(-0.8, 0.156);
    std::complex<float> a(jx, jy);
    float m;

    for (int i = 0; i < iterations; i += 1) {
        a = a * a + c;
        m = std::abs(a);
        if (m >= 4)
            return 0xFF000000;
    }
    return 0xFF0000FF;
}

void fractal(uint32_t pixels[], int size)
{
    uint32_t    rgb;
    uint32_t *  dst;

    dst = pixels;
    for (int y = 0; y < size; y += 1) {
        for (int x = 0; x < size; x += 1) {
            rgb = julia(x, y, size, 10, 200);
            *dst++ = rgb;
        }
    }
}

void savePNG(uint32_t pixels[], int size, const char * fileName)
{
    FILE * f;
    png_structp     writer;
    png_infop       info;
    uint32_t **     rows;

    f = fopen(fileName, "wb");
    FailNull(f, "Cannot open file %s", fileName);

    writer = png_create_write_struct(PNG_LIBPNG_VER_STRING, NULL, NULL, NULL);
    FailNull(writer, "Cannot create PNG write struct");
    info = png_create_info_struct(writer);
    FailNull(info, "Cannot create PNG info struct");
    png_set_IHDR(writer, info, size, size, 8, PNG_COLOR_TYPE_RGBA,
                PNG_INTERLACE_NONE, PNG_COMPRESSION_TYPE_BASE, PNG_FILTER_TYPE_BASE);
    rows = new uint32_t *[size];
    FailNull(rows, "savePNG cannot allocate rows array");
    png_init_io(writer, f);
    for (int i = 0; i < size; i += 1) {
        rows[i] = pixels + (i * size);
    }
    png_set_rows(writer, info, (png_bytepp)rows);
    png_write_png(writer, info, PNG_TRANSFORM_IDENTITY, NULL);

    png_destroy_write_struct(&writer, &info);

    fclose(f);
}

//****      When things go horribly wrong

void Fail(const char * format, ...)
{
    char msg[1024];
    va_list ap;

    va_start(ap, format);
    vsnprintf(msg, sizeof(msg), format, ap);
    va_end(ap);
    throw std::runtime_error(msg);
}

double elapsed(struct timespec & start, struct timespec & end)
{
    const int64_t NANO = 1000000000;
    int64_t diff;

    diff = (end.tv_sec - start.tv_sec) * NANO + (end.tv_nsec - start.tv_nsec);
    return (double)diff / (double)NANO;
}

int main(int argc, char * argv[])
{
    int size = 4096; // 1024;
    int N    = 10;
    uint32_t *  buf;
    struct timespec timeBase, now;
    const char * fName = "./fractal.png";

    if (argc > 1) {
        N = atoi(argv[1]);
        if (N <= 0)
            Fail("Bad repeat count %s", argv[1]);
    }
    buf = new uint32_t[size * size];
    FailNull(buf, "Cannot allocate pixel buffer");

    clock_gettime(CLOCK_MONOTONIC, &timeBase);
    for (int repeats = 0; repeats < N; repeats += 1) {
        printf("%d\n", repeats + 1);
        fractal(buf, size);
    }
    clock_gettime(CLOCK_MONOTONIC, &now);
    printf("Average generate time %4.3f secs\n", elapsed(timeBase, now) / N);

    savePNG(buf, size, fName);

    printf("Done.\n");

    delete[] buf;

    return 0;
}
