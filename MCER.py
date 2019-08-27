from Ellipse import *
from typing import NamedTuple
from E3PNT.ThreePntEllipse import *


class Cover:
    center: Point
    angle: float

    def __init__(self, ce, an):
        self.center = ce
        self.angle = an


def eval_cover(X, Y, e:Ellipse, c:Cover):
    val = 0
    e.set_angle(c.angle)
    e.set_center(c.center)

    for ix in range(len(X)):
        val += e.f(X[ix], Y[ix]) - 1e-9 < 1

    return val


def MCER1(X, Y, e: Ellipse) -> Cover:
    n = len(X)

    best_cover = Cover(Point(0, 0), 0)
    vbest_cover = 0

    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                sl = three_point_ellipse(e.a, e.b, X[i], Y[i], X[j], Y[j], X[k], Y[k])

                for s in sl:
                    c = Cover(s[0], s[1])

                    val = eval_cover(X, Y, e, c)

                    if val > vbest_cover:
                        vbest_cover = val
                        best_cover = c

    return best_cover