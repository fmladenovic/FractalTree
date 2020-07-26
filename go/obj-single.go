package main
 
import (
	"math"
	"time"
	"fmt"
	"strconv"
	"os"
)

const PATH = "../pharo/go-single.txt"


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

func tree( x, y, base, resize float64, end float64, angle float64, forkAngle float64, parent *Node, nodes *[]*Node) {
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

		tree(x1, y1, base, resize, end, angle, angle1, &node1, nodes)
		tree(x2, y2, base, resize, end, angle, angle2, &node2, nodes)
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
	tree(x, y, base, resize, end, angle, .0, &node1, &nodes)
	duration := time.Since(start)
	fmt.Println(duration)

	connectNodes( nodes )
	flip( nodes )
	writeToFile( nodes )
}