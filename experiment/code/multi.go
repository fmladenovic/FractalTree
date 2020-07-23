package main
 
import (
	"math"
	"fmt"
	"time"
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
func tree(wg *sync.WaitGroup, spawnedAsRoutine bool, spawnControle, x, y, base, resize float64, end float64, angle float64) {
	if spawnedAsRoutine {
		defer wg.Done()
	}
    if base > end {
        y := y + base
        x := x
        base := resize*base

        y1 := y + base * math.Cos(angle)
        x1 := x - (base* math.Sin(angle))

        y2 := y1
		x2 := x + (base * math.Sin(angle))

		// Nulti proces generiše levi proces čija je oznaka -1, nakon toga 0ti proces se preimenuje u
		// 1 kako bismo znali do kog račvanja smo stigli - proces 0 (1) nastavlja da obrađuje desnu granu.
		// Iz procesa 1 i -1 generišemo procese za njihove leve grane. Ponavlja se logika sa početka grananja...
		// * pogledati sliku processes-tree

		if spawnControle == 0 {
			wg.Add(1)
			go tree(wg, true, -1, x1, y1, base, resize, end, angle)
		} else if spawnControle == -1 {
			wg.Add(1)
			go tree(wg, true, -2, x1, y1, base, resize, end, angle)
		} else if spawnControle == -2 {
			wg.Add(1)
			go tree(wg, true, -4, x1, y1, base, resize, end, angle)
		} else if spawnControle == -3 {
			wg.Add(1)
			go tree(wg, true, -6, x1, y1, base, resize, end, angle)
		} else if spawnControle == 1 {
			wg.Add(1)
			go tree(wg, true, 2, x1, y1, base, resize, end, angle)
		} else if spawnControle == 2 {
			wg.Add(1)
			go tree(wg, true, 4, x1, y1, base, resize, end, angle)
		} else if spawnControle == 3 {
			wg.Add(1)
			go tree(wg, true, 6, x1, y1, base, resize, end, angle)
		} else {
			tree(wg, false, -20, x1, y1, base, resize, end, angle)
        }


        if spawnControle == 0 {
			tree(wg, false, 1, x2, y2, base, resize, end, angle)
		} else if spawnControle == -1 {
			tree(wg, false, -3, x2, y2, base, resize, end, angle)
		} else if spawnControle == -3 {
			tree(wg, false, -5, x2, y2, base, resize, end, angle)
		} else if spawnControle == 1 {
			tree(wg, false, 3, x2, y2, base, resize, end, angle)
		} else if spawnControle == 3{
			tree(wg, false, 5, x2, y2, base, resize, end, angle)
		} else {
			tree(wg, false, 20, x2, y2, base, resize, end, angle)
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

	start := time.Now()
	var wg sync.WaitGroup
	tree(&wg, false, 0, x, y, base, resize, end, angle)
	wg.Wait()
	duration := time.Since(start)
	fmt.Println(duration)
}
 
// Kada se koristi 7 + 1 goroutina brzina izvršavanja je ~21s
// Kada se koristi 5 + 1 goroutina brzina izvršavanja je ~30s
// Kada se koristi 3 + 1 goroutine brzina izvršavanja je ~24s
// Kada se koristi 1 + 1 goroutine brzina izvršavanja je ~48s

// Podsetnik: Bez paralelizacije brzina izvršavanja je ~85s
//  metoda 'tree' se izvrši 4294967295 puta  


// Napomena: Testiranje je rađeno na procesoru: Intel i7-6700 3.40GHz


// Zaključak - golang je u stanju čak ~1.86 puta brže da odradi 
//	četrdeset puta veći posao nego python