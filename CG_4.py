from PIL import Image
import matplotlib.pyplot as plt
from math import sqrt


def Sobel_Operator(x0, y0, width, height, pix_list):
    Sx = [0] * 3
    Sy = [0] * 3
    rgb = [0] * 3

    def update_sx_sy_coef(x, y, i):
        nonlocal Sx, Sy
        coef = 2 if (y == y0) else 1
        Sx[i] += coef * (pix_list[width * y + x + 1][i] -
                         pix_list[width * y + x - 1][i])
        coef = 2 if (x == x0) else 1
        Sy[i] += coef * (pix_list[width * (y - 1) + x][i] -
                         pix_list[width * (y + 1) + x][i])

    if x0 == y0 == 0:
        update_sx_sy_coef(x0, y0 + 1, i=0)
        update_sx_sy_coef(x0, y0 + 1, i=1)
        update_sx_sy_coef(x0, y0 + 1, i=2)
    elif x0 == 0 and y0 == height:
        update_sx_sy_coef(x0, y0 - 1, i=0)
        update_sx_sy_coef(x0, y0 - 1, i=1)
        update_sx_sy_coef(x0, y0 - 1, i=2)
    elif x0 == width and y0 == 0:
        update_sx_sy_coef(x0 - 1, y0, i=0)
        update_sx_sy_coef(x0 - 1, y0, i=1)
        update_sx_sy_coef(x0 - 1, y0, i=2)
    elif x0 == width and y0 == height:
        update_sx_sy_coef(x0 - 1, y0 - 1, i=0)
        update_sx_sy_coef(x0 - 1, y0 - 1, i=1)
        update_sx_sy_coef(x0 - 1, y0 - 1, i=2)
    else:
        for Y in range(y0 - 1, y0 + 2):
            if 0 <= Y < height:
                update_sx_sy_coef(x0, Y, i=0)
                update_sx_sy_coef(x0, Y, i=1)
                update_sx_sy_coef(x0, Y, i=2)

        for X in range(x0 - 1, x0 + 2):
            if 0 <= X < width:
                update_sx_sy_coef(X, y0, i=0)
                update_sx_sy_coef(X, y0, i=1)
                update_sx_sy_coef(X, y0, i=2)

    for i in range(3):
        rgb[i] += int(sqrt(Sx[i] * Sx[i] + Sy[i] * Sy[i]))
        rgb[i] = min(255, rgb[i])

    return tuple([int(sum(rgb) / 3)] * 3)


def main():
    with Image.open("valve.png") as image:
        new_image = Image.new('RGB', (image.width, image.height))
        pixel_values = list(image.getdata())

        for x in range(image.width - 1):
            for y in range(image.height - 1):
                new_color = Sobel_Operator(
                    x, y, image.width, image.height, pixel_values)
                new_image.putpixel((x, y), new_color)

        new_image.save("ваше_изображение")

        plt.imshow(image)
        plt.show()

        plt.imshow(new_image)
        plt.show()


if __name__ == "__main__":
    main()
