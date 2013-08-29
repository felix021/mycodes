package main

import (
    "strings"
    "code.google.com/p/go-tour/wc"
)

func WordCount(s string) map[string]int {
    ret := make(map[string]int)
    for _, x := range strings.Fields(s) {
        ret[x] += 1
    }
    return ret
    //return map[string]int{"x": 1}
}

func main() {
    wc.Test(WordCount)
}
