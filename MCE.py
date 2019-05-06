from Ellipse import *
import numpy as np

class Cover:
    def __init__(self, cov:set, p:tuple[any,any]):
        self.cov=cov
        self.p=p

def MCE1(X, Y, e:Ellipse):
    """
    :param X: X coordinates of points
    :param Y: Y coordinates of points
    :param e: Axis-parallel Ellipse
    :return: A list of coverage candidates.
    """
    n = len(X)

    E=[Ellipse(e.a, e.b, X[i], Y[i]) for i in range(n)]
    Z = []

    for i in range(n):
        A = []
        Z.append(Cover({i}, (X[i],Y[i])))

        for j in range(n):
            if (i==j):
                continue

            a1, a2 = E[i].interangles(E[j])
            A.append((a1, j, 1))
            A.append((a2, j, -1))

        A.sort()
        covered={i}

        Cnt = 0

        for tmp in range(2):
            for (a, ix, o) in A:
                if o==-1:
                    Z.append(Cover(covered.copy(), (E[j].fx(a),E[j].fy(a))))
                    covered.discard(ix)
                else:
                    Cnt+=1
                    covered.add(ix)

        return Z

class _MCE:
    def __init__(self, X, Y, E):
        m=len(E)
        n=len(X)
        self.sol = {j:(0,0) for j in range(m)}
        self.cover = set()
        self.Zs = [MCE1(X,Y,E[i]) for i in range(m)]

    def f(self, j):
        if j == self.m:
            return 0

        for op in self.Zs[j]:
            self.sol[j]=op.p
            self.cover.union(op.cov)

def _MCE(X,Y,E, sol:dict, j):
    if j==len(E):
        return 0







