package main
 
import (
	"math"
	"time"
	"fmt"
	"sync"
)

// Metoda se poziva rekurzivno sve dok se dužina grane ne smanji ispod određene granice
// Iz svake grane se proizvode dve nove (svaka metoda vrši dva rekurzivna poziva - za levu i za desnu granu)

// Parametri:
// wg - služi da sinhronizuje main metode sa goroutinama
// spawnedAsRoutine - govori da je data metoda goroutina i da treba da se označi kao završena nakon njenog izvršavanja
// spawnControle - parametar je dodat kako bi se na osnovu njega aktivirali dodatni procesi
// x - x pozicija roditeljskog čvora
// y - y pozicija roditeljskog čvora
// base - dužina grane
// resize - koliko ostaje od grane nakon svake iteracije
// angle - ugao koji zaklapaju grane
// forAngle - ugao pod kojim je prethodna grana došla do sadašnjeg čvora
func tree(wg *sync.WaitGroup, spawnedAsRoutine bool, spawnControle, x, y, base, resize float64, end float64, angle float64, forkAngle float64) {
	if spawnedAsRoutine {
		defer wg.Done()
	}
    if base > end {

		base = resize*base
		angle1 :=  forkAngle - angle
		angle2 :=  forkAngle + angle
	
        y1 := y + base * math.Cos(angle1)
        x1 := x + base * math.Sin(angle1)

        y2 := y + base * math.Cos(angle2)
		x2 := x + base * math.Sin(angle2)

		// Nulti proces generiše levi proces čija je oznaka -1, nakon toga 0ti proces se preimenuje u
		// 1 kako bismo znali do kog račvanja smo stigli - proces 0 (1) nastavlja da obrađuje desnu granu.
		// Iz procesa 1 i -1 generišemo procese za njihove leve grane. Ponavlja se logika sa početka grananja...

		if spawnControle == 0 {
			wg.Add(1)
			go tree(wg, true, -1, x1, y1, base, resize, end, angle, angle1)
		} else if spawnControle == -1 {
			wg.Add(1)
			go tree(wg, true, -2, x1, y1, base, resize, end, angle, angle1)
		} else if spawnControle == 1 {
			wg.Add(1)
			go tree(wg, true, 2, x1, y1, base, resize, end, angle, angle1)
		} else {
			tree(wg, false, -20, x1, y1, base, resize, end, angle, angle1)
        }

        if spawnControle == 0 {
			tree(wg, false, 1, x2, y2, base, resize, end, angle, angle2)
		} else {
			tree(wg, false, 20, x2, y2, base, resize, end, angle, angle2)
		}
	}
}

func main() {
	base := 100.0
    resize := 0.86
    end := 1.0
    angle := 45.0
    x := .0
	y := .0
	
    y = y + base

	start := time.Now()

	var wg sync.WaitGroup
	tree(&wg, false, 0, x, y, base, resize, end, angle, .0)
	wg.Wait()

	duration := time.Since(start)
	fmt.Println(duration)
}

// Napomena: Testiranje je rađeno na procesoru: Intel i7-6700 3.40GHz
