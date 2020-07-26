import math
import time
from multiprocessing import Process
from itertools import product

CONTINUE_WITH_CURRENT_PROCESS = -20



def tree(spawn_controle, x, y, base, resize, end, angle, fork_angle):
    if base > end:
        base = resize*base

        angle1 =  fork_angle - angle
        angle2 =  fork_angle + angle

        y1 = y + base * math.cos(angle1)
        x1 = x + (base* math.sin(angle1))

        y2 = y + base * math.cos(angle2)
        x2 = x + (base * math.sin(angle2))

        spawned = False 
        if spawn_controle == 0:
            p1 = Process(target = tree, args = (-1, x1, y1, base, resize, end, angle, angle1) )
            p1.start()
            spawned = True
        elif spawn_controle == -1:
            p1 = Process(target = tree, args = (-2, x1, y1, base, resize, end, angle, angle1) )
            p1.start()
            spawned = True
        elif spawn_controle == 1:
            p1 = Process(target = tree, args = (2, x1, y1, base, resize, end, angle, angle1) )
            p1.start()
            spawned = True
        else:
            tree(CONTINUE_WITH_CURRENT_PROCESS, x1, y1, base, resize, end, angle, angle1)
        
        if spawn_controle == 0:
            tree(1, x2, y2, base, resize, end, angle, angle2)  
        else:
            tree(CONTINUE_WITH_CURRENT_PROCESS, x2, y2, base, resize, end, angle, angle2) 

        if spawned: p1.join()


if __name__ == "__main__":
    x = 0
    y = 0
    base = 100
    resize = 0.84
    end = 1
    angle = 45

    start = time.perf_counter()

    y = y + base
    tree( 0, x, y, base, resize, end, angle, 0 )

    end = time.perf_counter()
    print(f'Finish in {round(end-start, 5)} secounds(s)')
