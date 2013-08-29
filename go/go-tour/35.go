package main

//import "fmt"

/* to save the output as a png file, run:
go run 35.go | tail -c +7 | base64 -d > 1.png
*/

import "code.google.com/p/go-tour/pic"

func Pic(dx, dy int) [][]uint8 {
    //fmt.Println(dx, dy)
    ret := make([][]uint8, dy)
    for i := range ret {
        ret[i] = make([]uint8, dx)
    }
    return ret
}

func main() {
    pic.Show(Pic)
}
