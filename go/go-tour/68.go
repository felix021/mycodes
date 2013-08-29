package main

import "fmt"

type Tree struct {
    Left *Tree
    Value int
    Right *Tree
}

func traverse(node *Tree, v chan int) {
    traverse_rec(node, v)
    close(v)
}

func traverse_rec(node *Tree, v chan int) {
    if node.Left != nil {
        traverse_rec(node.Left, v)
    }
    v <- node.Value
    if node.Right != nil {
        traverse_rec(node.Right, v)
    }
}


func make_tree1() *Tree {
    var Left, Right *Tree
    Left = &Tree{&Tree{nil, 1, nil}, 1, &Tree{nil, 2, nil}}
    Right = &Tree{&Tree{nil, 5, nil}, 8, &Tree{nil, 13, nil}}
    return &Tree{Left, 3, Right}
}

func make_tree2() *Tree {
    var Left *Tree
    Left = &Tree{&Tree{nil, 1, nil}, 1, &Tree{nil, 2, nil}}
    Left = &Tree{Left, 3, &Tree{nil, 5, nil}}
    return &Tree{Left, 8, &Tree{nil, 13, nil}}
}

func main() {

    tree1, tree2 := make_tree1(), make_tree2()
    v1, v2 := make(chan int), make(chan int)

    go traverse(tree1, v1)
    go traverse(tree2, v2)

    same := true
    for i := range v1 {
        j, jok := <-v2
        if !jok || i != j {
            same = false
            break
        }
    }
    fmt.Println(same)

}
