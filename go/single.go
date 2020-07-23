package main
 
import (
	"math"
    "fmt"
    "time"
)

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

}
 

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