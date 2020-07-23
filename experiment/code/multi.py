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
def tree(spawn_controle, x, y, base = 100, resize = 1/2, end = 10, angle = 45):
    if base > end:
        y = y + base
        x = x
        base = resize*base

        y1 = y + base * math.cos(angle)
        x1 = x - (base* math.sin(angle))

        y2 = y1
        x2 = x + (base * math.sin(angle))


        # Nulti proces generiše levi proces čija je oznaka -1, nakon toga 0ti proces se preimenuje u
        #     1 kako bismo znali do kog račvanja smo stigli - proces 0 (1) nastavlja da obrađuje desnu granu.
        # Iz procesa 1 i -1 generišemo procese za njihove leve grane. Ponavlja se logika sa početka grananja...
        # * pogledati sliku processes-tree



        spawned = False # Obezbeđuje se sinrhonizacija na mestu polaska
        if spawn_controle == 0:
            p1 = Process(target = tree, args = (-1, x1, y2, base, resize, end, angle) )
            p1.start()
            spawned = True

        elif spawn_controle == -1:
            p1 = Process(target = tree, args = (-2, x1, y2, base, resize, end, angle) )
            p1.start()
            spawned = True
        # elif spawn_controle == -2:
        #     p1 = Process(target = tree, args = (-4, x2, y2, base, resize, end, angle) )
        #     p1.start()
        #     spawned = True
        # elif spawn_controle == -3:
        #     p1 = Process(target = tree, args = (-6, x2, y2, base, resize, end, angle) )
        #     p1.start()
        #     spawned = True

        elif spawn_controle == 1:
            p1 = Process(target = tree, args = (2, x2, y2, base, resize, end, angle) )
            p1.start()
            spawned = True
        # elif spawn_controle == 2:
        #     p1 = Process(target = tree, args = (4, x2, y2, base, resize, end, angle) )
        #     p1.start()
        #     spawned = True
        # elif spawn_controle == 3:
        #     p1 = Process(target = tree, args = (6, x2, y2, base, resize, end, angle) )
        #     p1.start()
        #     spawned = True


        else:
            tree(CONTINUE_WITH_CURRENT_PROCESS, x2, y2, base, resize, end, angle)
        



        if spawn_controle == 0:
            tree(1, x2, y2, base, resize, end, angle)


        # elif spawn_controle == -1:
        #     tree(-3, x2, y2, base, resize, end, angle)  
        # elif spawn_controle == -3:
        #     tree(-5, x2, y2, base, resize, end, angle) 


        # elif spawn_controle == 1:
        #     tree(3, x2, y2, base, resize, end, angle)  
        # elif spawn_controle == 3:
        #     tree(5, x2, y2, base, resize, end, angle)  

        else:
            tree(CONTINUE_WITH_CURRENT_PROCESS, x2, y2, base, resize, end, angle) 

        if spawned: p1.join()




if __name__ == "__main__":
    x = 0
    y = 0
    base = 100
    resize = 0.84
    end = 1
    angle = 45

    start = time.perf_counter()
    tree(0, x, y, base, resize, end, angle)
    end = time.perf_counter()
    print(f'Finish in {round(end-start, 5)} secounds(s)')

    # Kada se koristi 7 + 1 procesa brzina izvršavanja je ~44s
    # Kada se koristi 5 + 1 procesa brzina izvršavanja je ~56s
    # Kada se koristi 3 + 1 procesa brzina izvršavanja je ~41s
    # Kada se koristi 1 + 1 procesa brzina izvršavanja je ~78s

    # Podsetnik: Bez paralelizacije brzina izvršavanja je ~130s
    #  metoda 'tree' se izvrši 134217727 puta  

    # Napomena: Testiranje je rađeno na procesoru: Intel i7-6700 3.40GHz
