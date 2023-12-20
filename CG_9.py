from PIL import Image, ImageOps
import matplotlib.pyplot as plt


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


def on_click(event):
    global points
    if event.button == 1:
        points.append((int(event.xdata), int(event.ydata)))


def fill_bpm(begin: int, end: int, filler_color: tuple):
    global sides
    for Y in range(begin, end+1):
        current_layer = []
        for side in sides:
            if min(side[0][1], side[1][1]) <= Y <= max(side[0][1], side[1][1])+1:
                X = round(side[0][0] + (((Y - side[0][1]) * (side[1]
                          [0] - side[0][0])) / (side[1][1] - side[0][1])))
                current_layer.append((X, Y))

        current_layer.sort()

        for i in range(0, len(current_layer), 2):
            if i+1 == len(current_layer):
                break
            for X in range(current_layer[i][0], current_layer[i+1][0]):
                image.putpixel((X, Y), filler_color)


points = []
sides = []

with Image.new("RGB", (5, 5)) as image:
    cid = plt.connect("button_press_event", on_click)

    for x in range(0, image.width):
        for y in range(0, image.height):
            if x % 2 == y % 2:
                image.putpixel((x, y), (54, 54, 54))

    plt.imshow(image)
    plt.show()

    filler_color = tuple(int(val)
                         for val in input("цвет заливки: ").strip().split())

    y_begin, y_end = image.height, 0

    for i in range(-1, len(points)-1):
        if points[i][1] != points[i+1][1]:
            sides.append(((points[i][0], points[i][1]),
                         (points[i+1][0], points[i+1][1])))
        y_begin = min(y_begin, points[i][1])
        y_end = max(y_end, points[i][0])

    fill_bpm(y_begin, y_end, filler_color)

    for i in range(len(sides)):
        bresenham(image, sides[i][0][0], sides[i][0][1],
                  sides[i][1][0], sides[i][1][1], filler_color)

    plt.imshow(image)
    plt.show()
