import math
import uuid


def tree( x, y, base, resize, end, angle, fork_angle, index ):
    if base > end:
        base = resize*base

        angle1 =  fork_angle - angle
        angle2 =  fork_angle + angle

        y1 = y + base * math.cos(angle1)
        x1 = x + (base* math.sin(angle1))

        y2 = y + base * math.cos(angle2)
        x2 = x + (base * math.sin(angle2))

        index += 1

        index = tree( x1, y1, base, resize, end, angle, angle1, index )
        index += 1
        index = tree( x2, y2, base, resize, end, angle, angle2, index ) 

    return index



if __name__ == "__main__":
    x = 0
    y = 0
    base = 100
    resize = 0.84
    end = 1
    angle = 45

    y = y + base
    index = tree( x, y, base, resize, end, angle, 0, 2)

    print(index)

