package main
 
import (
	"math";
	"strconv";
	"fmt";
)

func main() {
	base := 50.0
    resize := 0.5
    end := 10.0
    angle := 30.0
    x := .0
    y := .0

	tree(x, y, base, resize, end, angle)
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
		
		fmt.Println("(" + strconv.FormatFloat(x,  'f', 6, 64) + ", " + strconv.FormatFloat(y,  'f', 6, 64) + ")")
		fmt.Println("(" + strconv.FormatFloat(x1, 'f', 6, 64) + ", " + strconv.FormatFloat(y1, 'f', 6, 64) + ")")
		fmt.Println("(" + strconv.FormatFloat(x2, 'f', 6, 64) + ", " + strconv.FormatFloat(y2, 'f', 6, 64) + ")")

        tree(x1, y1, base, resize, end, angle)
		tree(x2, y2, base, resize, end, angle)
	}
}