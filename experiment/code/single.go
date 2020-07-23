package main
 
import (
	"math"
    "fmt"
    "time"
)


// Metoda se poziva rekurzivno sve dok se dužina grane ne smanji ispod određene granice
// Iz svake grane se proizvode dve nove (svaka metoda vrši dva rekurzivna poziva - za levu i za desnu granu)

// Parametri:
// x - x pozicija roditeljskog čvora
// y - y pozicija roditeljskog čvora
// base - dužina grane
// resize - koliko ostaje od grane nakon svake iteracije
// angle - ugao koji zaklapaju grane
func tree(x, y, base, resize float64, end float64, angle float64) {
    if base > end {
        y := y + base
        x := x
        base := resize*base

        y1 := y + base * math.Cos(angle)
        x1 := x - (base* math.Sin(angle))

        y2 := y1
		x2 := x + (base * math.Sin(angle))

        tree(x1, y1, base, resize, end, angle)
		tree(x2, y2, base, resize, end, angle)
	}
}

func main() {
	base := 100.0
    resize := 0.86
    end := 1.0
    angle := 45.0
    x := .0
    y := .0
    // Sa ovako nameštenim parametrima program izvrši 4294967295 puta metodu 'tree'


    start := time.Now()
    tree(x, y, base, resize, end, angle)
    duration := time.Since(start)
    fmt.Println(duration)
    // Vreme izvrsavanja ~85s


    // Napomena: testiranje je rađeno na procesoru: Intel i7-6700 3.40GHz
}
 
