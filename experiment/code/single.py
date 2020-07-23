import math
import matplotlib.pyplot as plt
import time

# Metoda se poziva rekurzivno sve dok se dužina grane ne smanji ispod određene granice
# Iz svake grane se proizvode dve nove (svaka metoda vrši dva rekurzivna poziva - za levu i za desnu granu)

# Parametri:
# x - x pozicija roditeljskog čvora
# y - y pozicija roditeljskog čvora
# base - dužina grane
# resize - koliko ostaje od grane nakon svake iteracije
# angle - ugao koji zaklapaju grane
def tree(x, y, base = 100, resize = 1/2, end = 10, angle = 45):
    if base > end:
        y = y + base
        x = x
        base = resize*base

        y1 = y + base * math.cos(angle)
        x1 = x - (base* math.sin(angle))

        y2 = y1
        x2 = x + (base * math.sin(angle))


        tree(x1, y1, base, resize, end, angle)
        tree(x2, y2, base, resize, end, angle)

if __name__ == "__main__":
    x = 0
    y = 0
    base = 100 
    resize = 0.84 
    end = 1
    angle = 45
    # Sa ovako nameštenim parametrima program izvrši 134217727 puta metodu 'tree'
    
    start = time.perf_counter()
    tree(x, y, base, resize, end, angle)
    end = time.perf_counter()
    print(f'Finish in {round(end-start, 5)} secounds(s)')
    # Vreme izvrsavanja ~130s




    # Napomena: testiranje je rađeno na procesoru: Intel i7-6700 3.40GHz


