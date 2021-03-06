package main
 
import (
	"math"
    "fmt"
)


func tree(x, y, base, resize float64, end float64, angle float64, forkAngle float64, index *int) {
    if base > end {

		base = resize*base
		angle1 :=  forkAngle - angle
		angle2 :=  forkAngle + angle
	
        y1 := y + base * math.Cos(angle1)
        x1 := x + base * math.Sin(angle1)

        y2 := y + base * math.Cos(angle2)
		x2 := x + base * math.Sin(angle2)

        *index++
        tree(x1, y1, base, resize, end, angle, angle1, index)
        *index++
        tree(x2, y2, base, resize, end, angle, angle2, index)
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

    var index = 2;
	tree(x, y, base, resize, end, angle, .0, &index)
    fmt.Printf("%d\n", index)
}