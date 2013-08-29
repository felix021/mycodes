package main

import "fmt"

var x, y, z int = 1, 2, 3
var c, python, java bool = true, false, "no!" //error here

func main() {
    fmt.Println(x, y, z, c, python, java)
}
