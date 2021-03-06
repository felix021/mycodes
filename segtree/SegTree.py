#!/usr/bin/python
#coding:utf-8

import os
import sys
import time
try:
    import simplejson as json
except:
    import json

import ctypes
c_SegTree = ctypes.CDLL('./segtree.so')

class CSegTree(object):
    def __init__(self, length):
        self.st = c_SegTree.st_new(length)

    def add(self, left, right):
        c_SegTree.st_add(self.st, left, right)

    def count(self):
        return c_SegTree.st_count(self.st)

    def dump(self):
        return c_SegTree.st_dump(self.st)

    def iterate(self):
        st_result = c_SegTree.st_get_all_covered(self.st);
        while True:
            result = c_SegTree.st_next_result(st_result)
            if result < 0:
                break
            yield result

    def __del__(self):
        if c_SegTree:
            c_SegTree.st_free(self.st)

class Node(object):
    def __init__(self, left, right, covered=False):
        self.left = left
        self.right = right
        self.covered = covered

        """
        if left + 1 < right:
            middle = self.middle()
            self.child_left  = Node(left, middle, covered)
            self.child_right = Node(middle, right, covered)
        """
        self.child_left  = None
        self.child_right = None

    def middle(self):
        return (self.left + self.right) / 2

    def left_add(self, left, right):
        if self.child_left is None:
            self.child_left = Node(self.left, self.middle(), self.covered)
        self.child_left.add(left, right)

    def right_add(self, left, right):
        if self.child_right is None:
            self.child_right = Node(self.middle(), self.right, self.covered)
        self.child_right.add(left, right)

    def add(self, left, right):
        if left == self.left and right == self.right:
            self.covered = True
            return

        middle = self.middle()
        if right <= middle:
            self.left_add(left, right)
        elif left >= middle:
            self.right_add(left, right)
        else:
            self.left_add(left, middle)
            self.right_add(middle, right)

        if self.child_left and self.child_left.covered and self.child_right and self.child_right.covered:
            self.covered = True
            #maybe not necessary to shrink?
            self.child_left = None
            self.child_right = None
    
    def dump(self, depth = 0, i = 1):
        print "%s %d: [%d, %d) => %s" % ("  " * depth, i, self.left, self.right, self.covered)
        if self.left + 1 < self.right:
            if self.child_left:
                self.child_left.dump(depth + 1, i * 2)
            else:
                print "  " * (depth + 1), "[left]"
            if self.child_right:
                self.child_right.dump(depth + 1, i * 2 + 1)
            else:
                print "  " * (depth + 1), "[right]"

    def count(self):
        if self.covered:
            return self.right - self.left

        if self.left + 1 == self.right:
            return 0

        left_count  = self.child_left.count() if self.child_left else 0
        right_count = self.child_right.count() if self.child_right else 0
        return left_count + right_count

    def iterate(self):
        if self.covered:
            for i in range(self.left, self.right):
                yield i
            return

        if self.left + 1 == self.right:
            return

        if self.child_left:
            for i in self.child_left.iterate():
                yield i

        if self.child_right:
            for i in self.child_right.iterate():
                yield i

class PYSegTree(object):
    def __init__(self, length):
        self.length = length
        self.root = Node(0, length)

    def add(self, left, right):
        self.root.add(left, right)

    def count(self):
        return self.root.count()

    def dump(self):
        self.root.dump()

    def iterate(self):
        for i in self.root.iterate():
            yield i

SegTree = CSegTree
#SegTree = PYSegTree

#"""
begin_at = time.time()
for i in range(1):
    length = 262144
    seg = length / 16
    st = SegTree(length)
    for j in range(15):
        st.add(seg * j, seg * j + seg * 2)
    print st.count()
    print len([i for i in st.iterate()])
    #del st

print time.time() - begin_at
#"""


#"""
st = SegTree(7)
st.add(4, 7)
st.dump()
st.add(0, 3)
st.dump()
st.add(3, 4)
st.dump()
print 'count:', st.count()

print [i for i in st.iterate()]

del st
#"""
