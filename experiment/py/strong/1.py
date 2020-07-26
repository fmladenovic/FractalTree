import math
import time

def tree( x, y, base, resize, end, angle, fork_angle ):
    if base > end:
        base = resize*base

        angle1 =  fork_angle - angle
        angle2 =  fork_angle + angle

        y1 = y + base * math.cos(angle1)
        x1 = x + (base* math.sin(angle1))

        y2 = y + base * math.cos(angle2)
        x2 = x + (base * math.sin(angle2))

        tree( x1, y1, base, resize, end, angle, angle1 )
        tree( x2, y2, base, resize, end, angle, angle2 ) 

if __name__ == "__main__":
    x = 0
    y = 0
    base = 100
    resize = 0.84
    end = 1
    angle = 45

    start = time.perf_counter()

    y = y + base
    tree( x, y, base, resize, end, angle, 0 )

    end = time.perf_counter()
    print(f'Finish in {round(end-start, 5)} secounds(s)')
