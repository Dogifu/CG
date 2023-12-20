from PIL import Image
import matplotlib.pyplot as plt


def gauss(x0, y0, width, height, pix_vals):
    rgb = [0] * 3

    for i in range(3):
        for X in range(x0 - 1, x0 + 2):
            for Y in range(y0 - 1, y0 + 2):
                if 0 <= X < width and 0 <= Y < height:
                    coef = 4 if (X == x0 and Y == y0) else (
                        2 if X == x0 or Y == y0 else 1)
                    rgb[i] += coef * pix_vals[width * Y + X][i]

        rgb[i] = min(int(rgb[i] / 16), 255)

    return tuple([int(sum(rgb) / 3)] * 3)


def main():
    with Image.open("valve.png") as image:
        new_image = Image.new('RGB', (image.width, image.height))
        pixel_values = list(image.getdata())

        for x in range(image.width):
            for y in range(image.height):
                new_color = gauss(x, y, image.width,
                                  image.height, pixel_values)
                new_image.putpixel((x, y), new_color)

        new_image.save("ваше_изображение.png")

        plt.imshow(image)
        plt.show()

        plt.imshow(new_image)
        plt.show()


if __name__ == "__main__":
    main()
