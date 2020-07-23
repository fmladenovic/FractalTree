package main
 
import (
	"math"
	"time"
	"strconv"
	"fmt"
)

type Node struct {
	id string
	parenId string

	x float64
	y float64
	angle float64

	index int
	ct_index int
}

func (n *Node) ToString() string {
	return strconv.FormatFloat(n.x,  'f', 6, 64) + " " + strconv.FormatFloat(n.y,  'f', 6, 64) + " " + strconv.FormatInt(n.index, 64) + " " + strconv.FormatInt(n.ct_index, 64)
}

func (n *Node) Produce( base: float64, angle: float64 ) []Node {
	nodes := []Node

	angle1 :=  n.angle + angle
	angle2 :=  n.angle - angle

	x1 := n.x - base * math.Sin(angle1)
	y1 := n.y - base * math.Cos(angle1)

	x2 := n.x - base * math.Sin(angle2)
	y2 := n.y - base * math.Cos(angle2)

	nodes = append(nodes, Node( x: x1, y: y1, angle: angle1 ) )
	nodes = append(nodes, Node( x: x2, y: y2, angle: angle2 ) )

	return nodes


}



func main() {
	base := 100.0
    resize := 0.75
    end := 1.0
    angle := 45.0
    x := .0
    y := .0

    start := time.Now()
    tree(x, y, base, resize, end, angle)
    duration := time.Since(start)
    fmt.Println(duration)

}
 

func tree(x, y, base, resize float64, end float64, angle float64) [][]Node {

	n0 := Node( x: x, y: y, index: 0, ct_index: 0)
	n1 := Node( x: x, y: y - base, index: 2, ct_index: 1)
	gen0 := []Node{n0}
	gen1 := []Node{n1}

	generations := [][]Node

	generations = append(generations, []Node)
	generations[0] = append(generations[0], gen0)

	generations = append(generations, []Node)
	generations[1] = append(generations[1], gen1)


	i := 1
    for base > end {
		base = resize * base
		generations = append(generations, []Node)
		i++

        new_nodes := process_job( generations[(len(generations)-1)], base, angle )
        generations[i] = append( generations[i], new_nodes )
	}

    return generations
}