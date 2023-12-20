from PIL import Image
import matplotlib.pyplot as plt
from math import sin, cos, pi


def bresenham(image, x0: int, y0: int, x1: int, y1: int, color: tuple = (255, 255, 255)):
    delta_x = abs(x1 - x0)
    delta_y = abs(y1 - y0)
    error = 0
    diff = 1

    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    if y0 > y1:
        diff = -1

    if delta_x >= delta_y:
        y_i = y0
        for x in range(x0, x1 + 1):
            image.putpixel((x, y_i), color)
            error += 2 * delta_y
            if error >= delta_x:
                y_i += diff
                error -= 2 * delta_x
    else:
        if diff == -1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        x_i = x0
        for y in range(y0, y1 + 1):
            image.putpixel((x_i, y), color)
            error += 2 * delta_x
            if error >= delta_y:
                x_i += diff
                error -= 2 * delta_y


def change_vector(change_matrix: list, vector: list):
    new_vector = [0] * len(vector)

    for i in range(len(change_matrix)):
        for j in range(len(vector)):
            new_vector[i] += change_matrix[i][j] * vector[j]

    return new_vector[:-1]


def get_vector(dots: list):
    return [dots[0], dots[1], dots[2], 1]


def to_radian(angle: float):
    return (angle * pi) / 180


def get_move_matrix(dx: float = 0, dy: float = 0, dz: float = 0):
    return [
        [1, 0, 0, dx],
        [0, 1, 0, dy],
        [0, 0, 1, dz],
        [0, 0, 0, 1]
    ]


def get_scale_matrix(kx: float = 0, ky: float = 0, kz: float = 0):
    return [
        [kx, 0, 0, 0],
        [0, ky, 0, 0],
        [0, 0, kz, 0],
        [0, 0, 0, 1]
    ]


def get_rotate_matrix_X(angle: float, is_radian: bool = False):
    if not is_radian:
        angle = to_radian(angle)

    return [
        [1, 0, 0, 0],
        [0, cos(angle), -sin(angle), 0],
        [0, sin(angle), cos(angle), 0],
        [0, 0, 0, 1]
    ]


def get_rotate_matrix_Y(angle: float, is_radian: bool = False):
    if not is_radian:
        angle = to_radian(angle)

    return [
        [cos(angle), 0, sin(angle), 0],
        [0, 1, 0, 0],
        [-sin(angle), 0, cos(angle), 0],
        [0, 0, 0, 1]
    ]


def get_rotate_matrix_Z(angle: float, is_radian: bool = False):
    if not is_radian:
        angle = to_radian(angle)

    return [
        [cos(angle), -sin(angle), 0, 0],
        [sin(angle), cos(angle), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ]


def is_visible(fig: list):
    global dots

    xa, ya, za = dots[fig[0]-1][0], dots[fig[0]-1][1], dots[fig[0]-1][2]
    xb, yb, zb = dots[fig[1]-1][0], dots[fig[1]-1][1], dots[fig[1]-1][2]
    xc, yc, zc = dots[fig[2]-1][0], dots[fig[2]-1][1], dots[fig[2]-1][2]

    C = (xb - xa) * (yc - ya) - (yb - ya) * (xc - xa)

    return C >= 0


dots = []
figures = []

with open(input("path_to_your_file: ")) as file:
    info = file.read().split('\n')

    for line in info:
        if line.startswith("v"):
            _, *line = line.split()
            dots.append(list(map(float, line)))
        elif line.startswith("f"):
            _, *line = line.split()
            figures.append(list(map(int, line)))

with Image.new("RGB", (26, 26)) as image:
    for x in range(0, image.width):
        for y in range(0, image.height):
            if x % 2 == y % 2:
                image.putpixel((x, y), (54, 54, 54))

    for i in range(len(dots)):
        dots[i] = change_vector(get_scale_matrix(
            15, 15, 15), get_vector(dots[i]))
        dots[i] = change_vector(get_rotate_matrix_Z(35), get_vector(dots[i]))
        dots[i] = change_vector(get_rotate_matrix_X(55), get_vector(dots[i]))
        dots[i] = change_vector(get_move_matrix(13, 13), get_vector(dots[i]))

    for i in range(len(figures)):
        fig = figures[i]
        if is_visible(fig):
            for j in range(-1, len(fig) - 1):
                bresenham(image, int(dots[fig[j] - 1][0]), int(dots[fig[j] - 1][1]),
                          int(dots[fig[j + 1] - 1][0]), int(dots[fig[j + 1] - 1][1]))

    plt.imshow(image)
    plt.show()
