import math
import matplotlib.pyplot as plt

def tree(x, y, base = 100, resize = 1/2, end = 10, angle = 45):
    if base > end:
        y = y + base
        x = x
        base = resize*base

        y1 = y + base * math.cos(angle)
        x1 = x - (base* math.sin(angle))

        y2 = y1
        x2 = x + (base * math.sin(angle))

        # plt.scatter([x, x1, x2], [y, y1, y2]) #TEST
        print("(" + str(x) + ", " + str(y) + ")")
        print("(" + str(x1) + ", " + str(y1) + ")")
        print("(" + str(x2) + ", " + str(y2) + ")")

        tree(x1, y1, base, resize, end, angle)
        tree(x2, y2, base, resize, end, angle)

if __name__ == "__main__":
    base = 50
    resize = 1/2
    end = 10
    angle = 30
    x = 0
    y = 0

    tree(x, y, base, resize, end, angle)

    # plt.scatter([x], [y]) #TEST
    # plt.show() #TEST

