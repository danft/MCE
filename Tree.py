from typing import List, Dict


class Node:
    children: Dict
    leaf: bool

    def __init__(self):
        self.children = dict()
        self.leaf = True


class Tree:
    root: Node

    def __init__(self):
        self.root = Node()

    def add_nodes(self, vlist: List[int]):
        t = self.root

        vlist.sort()

        for u in vlist:
            nxt = t.children.get(u)

            if nxt is None:
                t.children[u] = Node()
            t.leaf = False
            nxt = t.children[u]
            t = nxt

    def has(self, vlist: List[int]):
        t = self.root

        vlist.sort()

        for u in vlist:
            nxt = t.children.get(u)
            if nxt is None:
                return False

            t = nxt

        return True
