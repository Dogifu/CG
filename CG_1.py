from PIL import Image
import matplotlib.pyplot as plt
image = Image.new('RGB', (100,100), (255,255,255))

x0 = int(input("x_0 = "))

y0 = int(input("y_0 = "))

x1 = int(input("x_1 = "))

y1 = int(input("y_1 = "))

alfa_x = abs(x1 - x0) # значение для определения градусоной меры угла

alfa_y = abs(y1 - y0) # значение для определения градусной меры угла 

error = 0

diff = 1

if (x0 - x1 > 0):
    x0, x1 = x1, x0

    y0, y1 = y1, y0

if (y0 - y1 > 0):
    diff = -1


if (alfa_x >= alfa_y): # для угла менее 45 градусов
    y_i = y0
    for x in range(x0, x1 + 1):
        image.putpixel((x, y_i), (0, 255, 255))
        error = error + 2 * alfa_y
        if error >= alfa_x:
            y_i += diff
            error -= 2 * alfa_x

elif (alfa_x < alfa_y): # для угла более 45 градусов
    if (diff == -1):
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    x_i = x0
    for y in range(y0, y1 + 1):
        image.putpixel((x_i, y), (0, 255, 255))
        error = error + 2 * alfa_x
        if error >= alfa_y:
            x_i += diff
            error -= 2 * alfa_y

image.save("picture.png")
plt.imshow(image)
plt.show()