from PIL import Image
import matplotlib.pyplot as plt
from math import sin, cos, pi


class Dot:
    def __init__(self, cordX: float, cordY: float):
        self.x = cordX
        self.y = cordY


def change_dot(change_matrix: list, vector: list):
    new_vector = [0] * len(vector)

    for i in range(len(change_matrix)):
        for j in range(len(vector)):
            new_vector[i] += change_matrix[i][j] * vector[j]

    return Dot(new_vector[0], new_vector[1])


def get_vector(D: Dot):
    return [D.x, D.y, 1]


def to_radian(angle: float):
    return (angle * pi) / 180


def get_move_matrix(dx: float = 0, dy: float = 0, dz: float = 0):
    return [[1, 0, dx],
            [0, 1, dy],
            [0, 0, 1]]


def get_scale_matrix(kx: float = 0, ky: float = 0, kz: float = 0):
    return [[kx, 0, 0],
            [0, ky, 0],
            [0, 0, 1]]


def get_rotate_matrix(angle: float, is_radian: bool = False):
    if not is_radian:
        angle = to_radian(angle)

    return [[cos(angle), -sin(angle), 0],
            [sin(angle), cos(angle), 0],
            [0, 0, 1]]


def bresenham(image, x0: int, y0: int, x1: int, y1: int, color: tuple = (255, 255, 255)):
    delta_x = abs(x1 - x0)
    delta_y = abs(y1 - y0)
    error = 0
    diff = 1

    if x0 - x1 > 0:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    if y0 - y1 > 0:
        diff = -1

    if delta_x >= delta_y:
        y_i = y0
        for x in range(x0, x1 + 1):
            image.putpixel((x, y_i), color)
            error += 2 * delta_y
            if error >= delta_x:
                y_i += diff
                error -= 2 * delta_x
    elif delta_x < delta_y:
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


dots = []
figures = []

dots.append(Dot(0, 0))
dots.append(Dot(10, 0))
dots.append(Dot(10, 10))
dots.append(Dot(0, 10))
figures.append([1, 2, 3, 4])

with Image.new("RGB", (100, 100)) as image:
    for i in range(len(dots)):
        dots[i] = change_dot(get_scale_matrix(2, 2), get_vector(dots[i]))
        dots[i] = change_dot(get_rotate_matrix(45), get_vector(dots[i]))
        dots[i] = change_dot(get_move_matrix(50, 50), get_vector(dots[i]))

    for i in range(len(figures)):
        fig = figures[i]
        for j in range(-1, len(fig) - 1):
            bresenham(image, round(dots[fig[j] - 1].x), round(dots[fig[j] - 1].y),
                      round(dots[fig[j + 1] - 1].x), round(dots[fig[j + 1] - 1].y))

    plt.imshow(image)
    plt.show()
