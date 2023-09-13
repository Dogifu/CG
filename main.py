from PIL import Image
import matplotlib.pyplot as plt
import random
image = Image.new ('RGB', (100,100), (255,255,255))
print("x_0")
x_0 = int(input())
print("y_0")
y_0 = int(input())
print("x_1")
x_1 = int(input())
print("y_1")
y_1 = int(input())
c = 0
l = 0
d = 0
if x_0 > x_1:
    a = x_0
    x_0 = x_1
    x_1 = a
    b = y_0
    y_0 = y_1
    y_1 = b
k = (y_1 - y_0)/(x_1 - x_0)
e = 0
if k <= 1:
    y = y_0
    for x in range(x_0, (x_1 + 1)):
        if e > (x_1 - x_0):
           y+=1
           e-=2*(x_1 - x_0)
        e += 2*(y_1 - y_0)
        image.putpixel((x,y), (0, l, d))
        l = random.choice([255, 0, 128, 165])
        d = random.choice([255, 0, 128])



else:
    x = x_0
    for y in range(y_0, (y_1+1)):
        if e>(y_1 - y_0):
           x+=1
           e-=2*(y_1 - y_0)
        e += 2*(x_1 - x_0)
        image.putpixel((x,y), (0, l, d))
        l = random.choice([255, 0, 128, 165])
        d = random.choice([165, 0, 128])










image.save("a.png")

plt.imshow(image)

plt.show()