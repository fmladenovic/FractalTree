import math
import matplotlib.pyplot as plt
import sys

def tree(x, y, base = 100, resize = 1/2, end = 10, angle = 45):
    if base < end:
        return
    else:
        y = y + base
        x = x
        base = resize*base

        y1 = y + base * math.cos(angle)
        x1 = x - (base* math.sin(angle))

        y2 = y1
        x2 = x + (base * math.sin(angle))

        plt.scatter([x, x1, x2], [y, y1, y2]) #TEST

        tree(x1, y1, base)
        tree(x2, y2, base)

if __name__ == "__main__":
    base = 50
    resize = 0.999
    end = 10
    angle = 30
    x = 0
    y = 0

    plt.scatter([x], [y]) #TEST
    tree(x, y, base, resize, end, angle)
    plt.show() #TEST
