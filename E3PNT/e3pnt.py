import numpy as np
from math import sqrt, atan, cos, sin, pi
from E3PNT.poly_function import *
from E3PNT.circumradius import *
from typing import List


def _ccirc(x1, y1, x2, y2, x3, y3):
        A = np.array([[x3 - x1, y3 - y1], [x3 - x2, y3 - y2]])
        Y = np.array([(x3 ** 2 + y3 ** 2 - x1 ** 2 - y1 ** 2), (x3 ** 2 + y3 ** 2 - x2 ** 2 - y2 ** 2)])
        if np.linalg.det(A) == 0:
            return False
        Ainv = np.linalg.inv(A)
        X = 0.5 * np.dot(Ainv, Y)
        x, y = X[0], X[1]
        r = sqrt((x - x1) ** 2 + (y - y1) ** 2)
        return (x, y), r


def _tr(theta, q, x, y):
    return q * (x * cos(theta) + y * sin(theta)), -x * sin(theta) + y * cos(theta)


def _tri(theta, q, x, y):
    x = x/q
    return (x*cos(-theta) + y*sin(-theta)), -x * sin(-theta) + y * cos(-theta)


def _chk(theta, a, b, xc, yc, x, y):
        X = x - xc
        Y = y - yc
        return (X * cos(theta) + Y * sin(theta)) ** 2 / a ** 2 + (
                    X * sin(theta) - Y * cos(theta)) ** 2 / b ** 2 - 1e-9 < 1


def discard(a, b, X, Y):
    p = [np.array([X[i], Y[i]]) for i in range(3)]

    return np.linalg.norm(p[0]-p[1]) > 2*a or np.linalg.norm(p[0]-p[2]) > 2*a or np.linalg.norm(p[1]-p[2]) > 2*a


def get_input(X, Y):

    x0 = X[0]
    y0 = Y[0]
    x1 = X[1] - x0
    x2 = X[2] - x0
    y1 = Y[1] - y0
    y2 = Y[2] - y0

    return x0, y0, x1, y1, x2, y2


def get_cheb_poly(a: float, b: float, X: List[float], Y:List[float]):
    XX = [X[i] for i in range(3)]
    YY = [Y[i] for i in range(3)]

    f = np.vectorize(fradius, excluded=[1, 2, 3, 4])

    K = 1
    deg = 12
    Dm = pi / K
    ret = []

    for i in range(K):
        l = (i) * Dm
        r = (i+1) * Dm
        ret.append(np.polynomial.chebyshev.Chebyshev.interpolate(f, deg=deg, domain=(l, r), args=(a, b, XX, YY)))

    return ret


def e3pnt(a: float, b: float, X: List[float], Y: List[float]):

    return []


def e3pnt_poly(a: float, b: float, X: List[float], Y: List[float]):

    #if discard(a, b, X, Y):
    #    return []

    x0, y0, x1, y1, x2, y2 = get_input(X, Y)

    coeff = poly_coeff(a, b, x1, x2, y1, y2)
    m = max(coeff)
    coeff = list(map(lambda x: x/m, coeff))

    print(coeff)

    ret = []

    roo = np.roots(coeff)

    print(min(abs(roo.imag)))
    print("-----")

    #print(roo)
    #print()
    #print("--------------")
    #print()

    roots = list(filter(np.isreal, roo))

    for r in roots:
        theta = atan(r) * 2
        px1, py1 = _tr(theta, b / a, x1, y1)
        px2, py2 = _tr(theta, b / a, x2, y2)
        (xcc, ycc), r = _ccirc(0, 0, px1, py1, px2, py2)

        xc, yc = _tri(theta, b / a, xcc, ycc)

        if _chk(theta, a, b, xc, yc, x1, y1) and _chk(theta, a, b, xc, yc, x2, y2):
            ret.append(((xc + x0, yc + y0), theta))

    return ret
