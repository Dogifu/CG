from math import sin, cos, pi
from PIL import Image
import matplotlib.pyplot as plt
import random
import time
from typing import List, Tuple

random.seed(time.time())


class Dot:
    def __init__(self, cordX: float, cordY: float, cordZ: float):
        self.x = cordX
        self.y = cordY
        self.z = cordZ


def change_dot(change_matrix: List[List[float]], vector: List[float]) -> Dot:
    new_vector = [0] * len(vector)

    for i in range(len(change_matrix)):
        for j in range(len(vector)):
            new_vector[i] += change_matrix[i][j] * vector[j]

    return Dot(new_vector[0], new_vector[1], new_vector[2])


def get_vector(D: Dot) -> List[float]:
    return [D.x, D.y, D.z, 1]


def to_radian(angle: float) -> float:
    return (angle * pi) / 180


def get_move_matrix(dx: float = 0, dy: float = 0, dz: float = 0) -> List[List[float]]:
    return [[1, 0, 0, dx],
            [0, 1, 0, dy],
            [0, 0, 1, dz],
            [0, 0, 0, 1]]


def get_scale_matrix(kx: float = 0, ky: float = 0, kz: float = 0) -> List[List[float]]:
    return [[kx, 0, 0, 0],
            [0, ky, 0, 0],
            [0, 0, kz, 0],
            [0, 0, 0, 1]]


def get_rotate_matrix(axis: str, angle: float, is_radian: bool = False) -> List[List[float]]:
    if not is_radian:
        angle = to_radian(angle)

    axis = axis.lower()
    cos_val = cos(angle)
    sin_val = sin(angle)

    if axis == 'x':
        return [[1, 0, 0, 0], [0, cos_val, -sin_val, 0], [0, sin_val, cos_val, 0], [0, 0, 0, 1]]
    elif axis == 'y':
        return [[cos_val, 0, sin_val, 0], [0, 1, 0, 0], [-sin_val, 0, cos_val, 0], [0, 0, 0, 1]]
    elif axis == 'z':
        return [[cos_val, -sin_val, 0, 0], [sin_val, cos_val, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]


class Figure:
    def __init__(self, dotA: Dot, dotB: Dot, dotC: Dot, colour: Tuple[int, int, int]):
        self.dotA = dotA
        self.dotB = dotB
        self.dotC = dotC
        self.colour = colour

    def get_z(self, xi: int, yi: int) -> float:
        coefA = (self.dotB.y - self.dotA.y) * (self.dotC.z - self.dotA.z) - \
                (self.dotB.z - self.dotA.z) * (self.dotC.y - self.dotA.y)
        coefB = (self.dotB.z - self.dotA.z) * (self.dotC.x - self.dotA.x) - \
                (self.dotB.x - self.dotA.x) * (self.dotC.z - self.dotA.z)
        coefC = (self.dotB.x - self.dotA.x) * (self.dotC.y - self.dotA.y) - \
                (self.dotB.y - self.dotA.y) * (self.dotC.x - self.dotA.x)
        coefD = -self.dotA.x * coefA - self.dotA.y * coefB - self.dotA.z * coefC

        if coefC != 0:
            return (-coefA * xi - coefB * yi - coefD) / coefC

        return -1

    def in_figure(self, xt: int, yt: int) -> bool:
        abV = ((self.dotB.x - self.dotA.x), (self.dotB.y - self.dotA.y))
        bcV = ((self.dotC.x - self.dotB.x), (self.dotC.y - self.dotB.y))
        caV = ((self.dotA.x - self.dotC.x), (self.dotA.y - self.dotC.y))

        Nab = (abV[1], -abV[0])
        Nbc = (bcV[1], -bcV[0])
        Nca = (caV[1], -caV[0])

        atV = (xt - self.dotA.x, yt - self.dotA.y)
        btV = (xt - self.dotB.x, yt - self.dotB.y)
        ctV = (xt - self.dotC.x, yt - self.dotC.y)

        if (
            (Nab[0] * atV[0] + Nab[1] * atV[1] >= 0) and
            (Nbc[0] * btV[0] + Nbc[1] * btV[1] >= 0) and
            (Nca[0] * ctV[0] + Nca[1] * ctV[1] >= 0)
        ) or (
            (Nab[0] * atV[0] + Nab[1] * atV[1] < 0) and
            (Nbc[0] * btV[0] + Nbc[1] * btV[1] < 0) and
            (Nca[0] * ctV[0] + Nca[1] * ctV[1] < 0)
        ):
            return True

        return False


dots: List[Dot] = []
figures: List[Figure] = []

xmin, xmax, ymin, ymax = 100, 0, 100, 0

with open(input("path_to_your_file: ")) as file:
    info = file.read().split('\n')

    for line in info:
        if line.startswith("v"):
            _, *line = line.split()
            line = list(map(float, line))
            D = Dot(line[0], line[1], line[2])
            dots.append(D)
        elif line.startswith("f"):
            _, *line = line.split()
            figures.append(list(map(int, line)))

with Image.new("RGB", (100, 100)) as image:
    for x in range(0, image.width):
        for y in range(0, image.height):
            if x % 2 == y % 2:
                image.putpixel((x, y), (54, 54, 54))

    for i in range(len(dots)):
        dots[i] = change_dot(get_scale_matrix(40, 40, 40), get_vector(dots[i]))
        dots[i] = change_dot(get_rotate_matrix('z', 35), get_vector(dots[i]))
        dots[i] = change_dot(get_rotate_matrix('x', 55), get_vector(dots[i]))
        dots[i] = change_dot(get_move_matrix(50, 50), get_vector(dots[i]))
        xmin = int(min(xmin, dots[i].x))
        xmax = int(max(xmax, dots[i].x))
        ymin = int(min(ymin, dots[i].y))
        ymax = int(max(ymax, dots[i].y))

    for i in range(len(figures)):
        figures[i] = Figure(dots[figures[i][0] - 1], dots[figures[i][1] - 1],
                            dots[figures[i][2] - 1],
                            (random.randrange(256), random.randrange(256), random.randrange(256)))

    for X in range(xmin, xmax + 1):
        for Y in range(ymin, ymax + 1):
            current_fig = None
            current_z = None
            for i in range(len(figures)):
                if figures[i].in_figure(X, Y):
                    fig_z = figures[i].get_z(X, Y)
                    if current_fig is None or fig_z >= current_z:
                        current_fig = figures[i]
                        current_z = fig_z

            if current_fig is not None:
                image.putpixel((X, Y), current_fig.colour)

    plt.imshow(image)
    plt.show()
