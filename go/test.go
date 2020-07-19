package main
 
type state struct {
  board [7][6]int;
  heights [7]int;
}
 
type move struct {
  column int;
  score int;
}

