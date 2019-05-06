from Ellipse import *
import numpy as np

class Cover:
    def __init__(self, cov:set, p:tuple[any,any]):
        self.cov=cov
        self.p=p

def MCE1(X, Y, e:Ellipse):
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
                    Z.append(Cover(covered, ))
                    covered.discard(ix)
                else:
                    Cnt+=1
                    iscovered[ix] = True
                if (Cnt>opt):
                    opt=Cnt

        return opt







