import math


def angle(point):
    if point[0] == 0:
        if point[1] > 0:
            ang = math.pi / 2
        else:
            ang = math.pi * 3 / 2
    elif point[0] >= 0:
        r = point[1] / point[0]
        ang = math.atan(r)
    else:
        r = point[1] / point[0]
        ang = math.atan(r) + math.pi

    if ang < 0:
        ang += math.pi * 2
    return ang * 180 / math.pi


print(angle((-2, 3)) - angle((-6, 2)))
