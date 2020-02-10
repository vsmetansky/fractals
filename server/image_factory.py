from math import atan2, cos

from numba import njit, uint16, complex64, float32, boolean
from PIL import Image

MAX_ITER = 100


def get_color(c):
    return (c, c, c)


@njit(boolean(float32, float32))
def inside_cardioid(x0, y0):
    return (x0 - 0.25) ** 2 + y0 ** 2 < (0.5 - 0.5 * cos(atan2(y0, x0 - 0.25))) ** 2


@njit(uint16(complex64, uint16))
def iteration(c, max_iter):
    z = 0
    for i in range(1, max_iter):
        if z.real ** 2 + z.imag ** 2 > 4:
            return i
        z = z ** 2 + c
    return 0


@njit(uint16(complex64, uint16))
def mandelbrot(c, max_iter):
    if inside_cardioid(c.real, c.imag):
        return 0
    return iteration(c, max_iter)


@njit
def transform(x, y, width, height):
    return ((x - (width - 1) // 2) / width * 4,
            ((height - 1) // 2 - y) / height * 2)


def set_pixel_data(pixels, width, height):
    for x in range(width):
        for y in range(height):
            x_t, y_t = transform(x, y, width, height)
            pixels[x, y] = get_color(mandelbrot(complex(x_t, y_t), MAX_ITER))


def create_image(width, height):
    img = Image.new('RGB', (width, height), (0, 0, 0))
    set_pixel_data(img.load(), width, height)
    return img


if __name__ == '__main__':
    import argparse as ap

    DEFAULT_DIMENSION = 1000

    parser = ap.ArgumentParser(description='Window dimension setter.')
    parser.add_argument('--width', type=int, dest='width', default=DEFAULT_DIMENSION,
                        help='Width of the program\'s window.')
    parser.add_argument('--height', type=int, dest='height', default=DEFAULT_DIMENSION,
                        help='Height of the program\'s window.')

    args = parser.parse_args()

    create_image(args.width, args.height).show()
