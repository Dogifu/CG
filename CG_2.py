from PIL import Image
import matplotlib.pyplot as plt
image = Image.new ('RGB', (100,100), (255,255,255))
print('x')
x = int(input())
print('y')
y = int(input())
print('r')
r = int(input())

disp_x = x
disp_y = y
x = 0
y = r
delta = (1 - 2 * r)
error = 0
while y >= 0:
    image.putpixel((disp_x + x, disp_y + y), 255)
    image.putpixel((disp_x + x, disp_y - y), 255)
    image.putpixel((disp_x - x, disp_y + y), 255)
    image.putpixel((disp_x - x, disp_y - y), 255)

    error = 2 * (delta + y) - 1
    if ((delta < 0) and (error <= 0)):
        x += 1
        delta = delta + (2 * x + 1)
        continue
    error = 2 * (delta - x) - 1
    if ((delta > 0) and (error > 0)):
        y -= 1
        delta = delta + (1 - 2 * y)
        continue
    x += 1
    delta = delta + (2 * (x - y))
    y -= 1

image.save("a.png")
plt.imshow(image)
plt.show()