package main

import "fmt"

func main() {
    c := make(chan int, 2)
    c <- 1
    c <- 2
    //c <- 3 //cache full -> dead lock
    fmt.Println(<-c)
    fmt.Println(<-c)
}
