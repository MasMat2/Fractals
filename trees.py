from PIL import Image, ImageDraw
import math

w, h, zoom = 800, 600, 1
image = Image.new("RGB", (w,h), "white")
draw = ImageDraw.Draw(image)

lenght = 200
k = [0.65, 0.75]
teta = [math.radians(20), -math.radians(10)]

def a(line, angle, it=1):
    max = 15
    if it > max:
        return 0
    if it> 7*max//10:
        draw.line(line, (71,148,71))
    else:
        draw.line(line, (102,51,0), width=int(2*it/max)+1)

    for i in range(2):
        x = lenght*(k[i]**it)*math.cos(angle + teta[i]) + line[-1][0]
        y = -lenght*(k[i]**it)*math.sin(angle + teta[i]) + line[-1][1]
        a([line[-1], (x,y)], angle+teta[i], it+1)

a([(w/2, h), (w/2, h*3/4)], math.pi/2)


image.show()
