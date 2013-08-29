package main

import (
    "fmt"
    "math"
)

func pow(x, n, lim float64) float64 {
    if v := math.Pow(x, n); v < lim {
        return v
    }
    // return v //fail
    return lim
}

func main() {
    fmt.Println(pow(3, 2, 10))
    fmt.Println(pow(3, 3, 20))
}
