package main

import (
    "fmt"
    "math"
)

func Sqrt(x float64) float64 {
    z := 1.0
    for i := 0; i < 10; i++ {
        z = z - (z * z - x) / (2 * z)
        fmt.Printf("z = %g\n", z)
    }
    return z
}

func main() {
    fmt.Println(Sqrt(32))
    fmt.Println(math.Sqrt(32))
}
