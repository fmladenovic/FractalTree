package main
 
import (
	"math"
	"time"
	"fmt"
	"sync"
)


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