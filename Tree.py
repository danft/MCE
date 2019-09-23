from typing import List, Dict
from sortedcollections import SortedDict


class Node:
    children: SortedDict
    leaf: bool

    def __init__(self):
        self.children = SortedDict()
        self.leaf = True


class Tree:
    root: Node
    wh: List[List[Node]]
    n: int

    def __init__(self, n: int):
        self.root = Node()
        self.wh = [[] for i in range(1+n)]
        self.n = n

    def add_nodes(self, I: List[int]):
        t = self.root

        for u in I:
            nxt = t.children.get(u)

            if nxt is None:
                c_node = Node()
                self.wh[u].append(c_node)
                t.children[u] = c_node

            t.leaf = False
            t = t.children[u]

    def has(self, I: List[int]):

        for t in self.wh[I[0]]:
            if self._has(I, t, 1):
                return True

        return False

    def _has(self, I: List[int], t: Node, k: int):
        if k == len(I):
            return True

        for u in t.children:
            if u > I[k]:
                return False

            if u == I[k]:
                return self._has(I, t.children[u], k+1)

            if self._has(I, t.children[u], k):
                return True

        return False

