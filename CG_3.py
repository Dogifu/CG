from PIL import Image


def draw_line(image, x0, y0, x1, y1):
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    if x1 == x0:
        for i in range(y0, y1):
            image.putpixel((x1, i), (0, 0, 255))
    else:
        k = abs((y1 - y0) / (x1 - x0))
        e = 0

        if k <= 1:
            y = y0
            step_y = 1 if y1 >= y0 else -1

            for x in range(x0, x1 + 1):
                image.putpixel((x, y), (0, 0, 255))
                e += 2 * (y1 - y0)
                if e > (x1 - x0):
                    y += step_y
                    e -= 2 * (x1 - x0)
        else:
            x = x0
            step_x = 1 if x1 >= x0 else -1

            for y in range(y0, y1 + 1):
                image.putpixel((x, y), (0, 0, 255))
                e += 2 * (x1 - x0)
                if e > (y1 - y0):
                    x += step_x
                    e -= 2 * (y1 - y0)


def main():
    print("Введите количество вершин выпуклого многоугольника")
    n = int(input())

    print("Введите последовательно вершины многоугольника.")
    print("Вершины вводятся по часовой стрелке. Координаты в формате X Y через пробел")
    vertices = [tuple(map(int, input().split())) for _ in range(n)]

    print("Введите отрезок, который должен отсечь многоугольник")
    print("Введите координаты первой точки в формате X Y через пробел")
    xa, ya = map(int, input().split())
    print("Введите координаты второй точки в формате X Y через пробел")
    xb, yb = map(int, input().split())

    image = Image.new('RGB', (100, 100))

    for i in range(n):
        x0, y0 = vertices[i]
        x1, y1 = vertices[(i + 1) % n]
        draw_line(image, x0, y0, x1, y1)

    draw_line(image, xa, ya, xb, yb)

    image.save("a.png")
    print("Изображение сохранено")


if __name__ == "__main__":
    main()
