package main
 
import (
	"math"
	"time"
	"fmt"
)


func tree(x, y, base, resize float64, end float64, angle float64, forkAngle float64) {
    if base > end {

		base = resize*base
		angle1 :=  forkAngle - angle
		angle2 :=  forkAngle + angle
	
        y1 := y + base * math.Cos(angle1)
        x1 := x + base * math.Sin(angle1)

        y2 := y + base * math.Cos(angle2)
		x2 := x + base * math.Sin(angle2)

		tree(x1, y1, base, resize, end, angle, angle1)
		tree(x2, y2, base, resize, end, angle, angle2)
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

	tree(x, y, base, resize, end, angle, .0)

	duration := time.Since(start)
	fmt.Println(duration)
}