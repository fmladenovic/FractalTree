import math
import time
from multiprocessing import Process
from itertools import product

CONTINUE_WITH_CURRENT_PROCESS = -20


# Metoda se poziva rekurzivno sve dok se dužina grane ne smanji ispod određene granice
# Iz svake grane se proizvode dve nove (svaka metoda vrši dva rekurzivna poziva - za levu i za desnu granu)

# Parametri:
# spawn_controle - parametar je dodat kako bi se na osnovu njega aktivirali dodatni procesi
# x - x pozicija roditeljskog čvora
# y - y pozicija roditeljskog čvora
# base - dužina grane
# resize - koliko ostaje od grane nakon svake iteracije
# angle - ugao koji zaklapaju grane
# for_angle - ugao pod kojim je prethodna grana došla do sadašnjeg čvora
def tree(spawn_controle, x, y, base, resize, end, angle, fork_angle):
    if base > end:
        base = resize*base

        angle1 =  fork_angle - angle
        angle2 =  fork_angle + angle

        y1 = y + base * math.cos(angle1)
        x1 = x + (base* math.sin(angle1))

        y2 = y + base * math.cos(angle2)
        x2 = x + (base * math.sin(angle2))

        # Nulti proces generiše levi proces čija je oznaka -1, nakon toga 0ti proces se preimenuje u
        #     1 kako bismo znali do kog račvanja smo stigli - proces 0 (1) nastavlja da obrađuje desnu granu.
        # Iz procesa 1 i -1 generišemo procese za njihove leve grane. Ponavlja se logika sa početka grananja...
        # * pogledati sliku processes-tree


        spawned = False # Obezbeđuje se sinrhonizacija na mestu polaska
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

    # Napomena: Testiranje je rađeno na procesoru: Intel i7-6700 3.40GHz
