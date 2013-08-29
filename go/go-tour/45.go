package main

import (
    "fmt"
    "time"
)

func main() {
    fmt.Println("Now:", time.Now())
    fmt.Println(time.Saturday)
    fmt.Println(time.Now().Weekday()+1)

    fmt.Println("When's Saturday?")
    today := time.Now().Weekday()
    switch time.Saturday {
    case today + 0:
        fmt.Println("Today")
    case today + 1:
        fmt.Println("Tomorrow")
    case today + 2:
        fmt.Println("In two days")
    default:
        fmt.Println("Too far away")
    }
}
