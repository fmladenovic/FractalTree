package main
 
import (
	"math"
	"fmt"
	"time"
	"sync"
)


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


		if spawnControle == 0 {
			wg.Add(1)
			go tree(wg, true, -1, x1, y1, base, resize, end, angle)
		} else if spawnControle == -1 {
			wg.Add(1)
			go tree(wg, true, -2, x1, y1, base, resize, end, angle)
		} else if spawnControle == 1 {
			wg.Add(1)
			go tree(wg, true, 2, x1, y1, base, resize, end, angle)
		} else {
			tree(wg, false, -20, x1, y1, base, resize, end, angle)
		}
		
        if spawnControle == 0 {
			tree(wg, false, 1, x2, y2, base, resize, end, angle)
		} else if spawnControle == -1 {
			tree(wg, false, -3, x2, y2, base, resize, end, angle)
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

