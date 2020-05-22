import math
import time
import multiprocessing
from multiprocessing import Process
from itertools import product

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

        # print('(' + str(x1) + ', ' + str(y1) + ')')
        # print('(' + str(x2) + ', ' + str(y2) + ')')

        p1 = Process(target = tree, args = (x1, y1, base, resize, end, angle) )
        p2 = Process(target = tree, args = (x2, y2, base, resize, end, angle) )
        
        p1.start()
        p2.start()
        
        # p1.join()
        # p2.join()


def tree_s(x, y, base = 100, resize = 1/2, end = 10, angle = 45):
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

        tree_s(x1, y1, base, resize, end, angle)
        tree_s(x2, y2, base, resize, end, angle)
    


if __name__ == "__main__":
    x = 0
    y = 0
    base = 100
    resize = 1/2
    end = 10
    angle = 45


    start = time.perf_counter()

    p0 = Process(target = tree, args = (x, y, base, resize, end, angle) )
    p0.start()
    p0.join()
    
    print(f'Finish in {round(end-start, 5)} secounds(s)')



    start = time.perf_counter()
    tree_s(x, y)
    end = time.perf_counter()
    print(f'Finish in {round(end-start, 5)} secounds(s)')



    