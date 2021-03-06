package main
 
import (
	"math"
	"time"
	"fmt"
	"sync"
	"strconv"
	"os"
)

const PATH = "../pharo/go-multi.txt"

// Mоže da se desi da skripta ponekad ne izgeneriše dobar file ali to nije zato što je algoritam loš
//	već zato što go-routine dele isti memorijski prostor pa dođe do prepisivanja u listi čvorova.
// Dovoljno je pokrenuti skriptu par puta i izgenerisaće se dobar file.



type Node struct {
	x float64
	y float64
	parent *Node

	index int
	parentIndex int
}

func (n Node) ToString() string {
	return strconv.FormatFloat(n.x,  'f', 6, 64) + " " + strconv.FormatFloat(n.y,  'f', 6, 64) + " " + strconv.Itoa(n.index) + " " + strconv.Itoa(n.parentIndex)
}

func tree(wg *sync.WaitGroup, spawnedAsRoutine bool, spawnControle, x, y, base, resize float64, end float64, angle float64, forkAngle float64, parent *Node, nodes *[]*Node) {
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

		node1 := Node { x: x1, y: y1 }
		node1.parent = parent

		node2 := Node { x: x2, y: y2 }
		node2.parent = parent

		*nodes = append( *nodes, &node1 )
		*nodes = append( *nodes, &node2 )


		if spawnControle == 0 {
			wg.Add(1)
			go tree(wg, true, -1, x1, y1, base, resize, end, angle, angle1, &node1, nodes)
		} else if spawnControle == -1 {
			wg.Add(1)
			go tree(wg, true, -2, x1, y1, base, resize, end, angle, angle1, &node1, nodes)
		} else if spawnControle == -2 {
			wg.Add(1)
			go tree(wg, true, -4, x1, y1, base, resize, end, angle, angle1, &node1, nodes)
		} else if spawnControle == -3 {
			wg.Add(1)
			go tree(wg, true, -6, x1, y1, base, resize, end, angle, angle1, &node1, nodes)
		} else if spawnControle == 1 {
			wg.Add(1)
			go tree(wg, true, 2, x1, y1, base, resize, end, angle, angle1, &node1, nodes)
		} else if spawnControle == 2 {
			wg.Add(1)
			go tree(wg, true, 4, x1, y1, base, resize, end, angle, angle1, &node1, nodes)
		} else if spawnControle == 3 {
			wg.Add(1)
			go tree(wg, true, 6, x1, y1, base, resize, end, angle, angle1, &node1, nodes)
		} else {
			tree(wg, false, -20, x1, y1, base, resize, end, angle, angle1, &node1, nodes)
        }

        if spawnControle == 0 {
			tree(wg, false, 1, x2, y2, base, resize, end, angle, angle2, &node2, nodes)
		} else if spawnControle == -1 {
			tree(wg, false, -3, x2, y2, base, resize, end, angle, angle2, &node2, nodes)
		} else if spawnControle == -3 {
			tree(wg, false, -5, x2, y2, base, resize, end, angle, angle2, &node2, nodes)
		} else if spawnControle == 1 {
			tree(wg, false, 3, x2, y2, base, resize, end, angle, angle2, &node2, nodes)
		} else if spawnControle == 3{
			tree(wg, false, 5, x2, y2, base, resize, end, angle, angle2, &node2, nodes)
		} else {
			tree(wg, false, 20, x2, y2, base, resize, end, angle, angle2, &node2, nodes)
		}
	}
}


func writeToFile( nodes []*Node ) {

	var toWrite = ""
	for i, n := range nodes {
		if i == 0 {
			toWrite = (*n).ToString()
		} else {
			toWrite = toWrite + "|" + (*n).ToString()
		}
	}

	f, err := os.Create(PATH)
    if err != nil {
        fmt.Println(err)
        return
    }
    l, err := f.WriteString(toWrite)
    if err != nil {
        fmt.Println(err)
        f.Close()
        return
    }
    fmt.Println(l, "bytes written successfully")
    err = f.Close()
    if err != nil {
        fmt.Println(err)
        return
    }
}

func connectNodes( nodes []*Node ) {
	for i := 0; i < len(nodes); i++ {
		nodes[i].index = i + 1;	
	}
	for i := 1; i < len(nodes); i++ {
		(*nodes[i]).parentIndex = parentPosition( nodes, (*nodes[i]).parent ) + 1
	}
}

func parentPosition( nodes []*Node , parent *Node ) int {
	for i :=  range nodes {
		if parent == nodes[i] {
			return i;
		}
	}
	return 0;
}

func flip( nodes []*Node ) {
    for _, n := range nodes {
		(*n).y = -(*n).y
	}
}


func main() {
	base := 100.0
    resize := 0.666
    end := 20.0
    angle := 45.0
    x := .0
	y := .0
	
	nodes := []*Node{}

	node := Node{x: x, y: y, index: 1, parentIndex: 0}
    y = y + base
	node1 := Node{x: x, y: y, index: 2, parentIndex: 1}
	node1.parent = &node

	nodes = append( nodes, &node )
	nodes = append( nodes, &node1 )

	start := time.Now()
	var wg sync.WaitGroup
	tree(&wg, false, 0, x, y, base, resize, end, angle, .0, &node1, &nodes)
	wg.Wait()
	duration := time.Since(start)
	fmt.Println(duration)

	connectNodes( nodes )
	flip( nodes )
	writeToFile( nodes )

}