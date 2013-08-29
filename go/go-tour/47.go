package main

import (
    "fmt"
    "math/cmplx"
)

func Cbrt(x complex128) complex128 {
    z := complex128(1)
    for {
        z3 := cmplx.Pow(z, 3)
        if real(cmplx.Pow(z3 - x, 2)) < 1e-5 {
            break
        }
        z = z - (z3 - x) / (3 * cmplx.Pow(z, 2))
    }
    return z
}

func main() {
    fmt.Println(Cbrt(2))
}
