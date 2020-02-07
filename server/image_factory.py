from math import atan2, cos

from numba import jit
from PIL import Image

MAX_ITER = 1000


@jit
def get_color(c):
    return (c, c, c)


@jit
def mandelbrot(c, max_iter):
    if inside_cardioid(c.real, c.imag):
        return 0
    return iteration(c, max_iter)


@jit
def inside_cardioid(x0, y0):
    return (x0 - 0.25) ** 2 + y0 ** 2 < (0.5 - 0.5 * cos(atan2(y0, x0 - 0.25))) ** 2


@jit
def iteration(c, max_iter):
    z = 0
    for i in range(1, max_iter):
        if z.real ** 2 + z.imag ** 2 > 4:
            return i
        z = z ** 2 + c
    return 0


@jit
def transform(x, y, width, height):
    return ((x - (width - 1) // 2) / width * 10,
            ((height - 1) // 2 - y) / height * 5)


@jit(forceobj=True)
def set_pixel_data(pixels, width, height):
    for x in range(width):
        for y in range(height):
            x_t, y_t = transform(x, y, width, height)
            pixels[x, y] = get_color(mandelbrot(complex(x_t, y_t), MAX_ITER))


def create_image(width, height):
    img = Image.new('RGB', (width, height))
    set_pixel_data(img.load(), width, height)
    return img
