package main

import "fmt"

var pow = []int {1,2,4,8,16,32,64,128}

func main() {
    for _, v := range pow {
        fmt.Println(v)
    }

    for i := range pow {
        fmt.Println(i)
    }
}
