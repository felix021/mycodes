package main

import "fmt"
import "code.google.com/p/go-tour/tree"

type Tree struct {
    Left *Tree
    Value int
    Right *Tree
}

func walk_rec(node *tree.Tree, ch chan int) {
    if node.Left != nil {
        walk_rec(node.Left, ch)
    }
    ch <- node.Value
    if node.Right != nil {
        walk_rec(node.Right, ch)
    }
}

func Walk(t *tree.Tree, ch chan int) {
    walk_rec(t, ch)
    close(ch)
}

func Same(t1, t2 *tree.Tree) bool {
    v1, v2 := make(chan int), make(chan int)
    go Walk(t1, v1)
    go Walk(t2, v2)
    for i := range v1 {
        j, ok := <-v2
        if !ok || i != j {
            return false
        }
    }
    return true
}

func main() {
    fmt.Println(Same(tree.New(1), tree.New(1)))
    fmt.Println(Same(tree.New(1), tree.New(2)))
}
