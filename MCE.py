from Ellipse import *
import numpy as np

class Cover:
    def __init__(self, cov: set, p: Point):
        self.cov = cov
        self.p = p


def MCE1(X, Y, e: Ellipse):
    """
    :param X: X coordinates of points
    :param Y: Y coordinates of points
    :param e: Axis-parallel Ellipse
    :return: A list of coverage candidates.
    """
    n = len(X)

    el = [Ellipse(e.a, e.b, X[i], Y[i]) for i in range(n)]
    zret = []

    for i in range(n):
        actset = []
        zret.append(Cover({i}, (X[i], Y[i])))

        for j in range(n):
            if (i == j):
                continue

            a1, a2 = el[i].interangles(el[j])
            actset.append((a1, j, 1))
            actset.append((a2, j, -1))

        actset.sort()
        covered = {i}

        Cnt = 0

        for tmp in range(2):
            for (a, ix, o) in actset:
                if o == -1:
                    zret.append(Cover(covered.copy(), (el[j].fx(a), el[j].fy(a))))
                    covered.discard(ix)
                else:
                    Cnt += 1
                    covered.add(ix)

        return zret


class _MCE:

    def __init__(self, X, Y, E):
        """
        Does the backtracking
        :param X: The x-coord of the point set
        :param Y: The y-coord of the point set
        :param E: The array of ellipses
        """
        self.m = len(E)
        self.n = len(X)

        # the current solution
        self.sol = {j: (0, 0) for j in range(self.m)}

        # the opt solution
        self.opt = dict()

        # The number of points covered in the optimal solution
        self.fopt = 0

        # the set of points covered currently
        self.cover = set()

        self.Zs = [MCE1(X, Y, E[i]) for i in range(self.m)]

    def f(self, j):
        if j == self.m:
            if len(self.cover) > self.fopt:
                self.opt = self.sol.copy()
                self.fopt = len(self.cover)

            return

        for op in self.Zs[j]:
            self.sol[j] = op.p
            self.cover.union(op.cov)
            self.f(j+1)
            self.cover.discard(op.cov)

def MCE(X, Y, E):
    _mc = _MCE(X,Y,E)
    _mc.f(0)

    return _mc.fopt, _mc.opt
