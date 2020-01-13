import numpy as np
from math import sqrt, atan, cos, sin, pi
from E3PNT.poly_function import *
from E3PNT.circumradius import *
from typing import List
from numba import *
import time


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
    x = x / q
    return (x * cos(-theta) + y * sin(-theta)), -x * sin(-theta) + y * cos(-theta)


def eval_ellipse(theta, a, b, xc, yc, x, y):
    X = x - xc
    Y = y - yc

    return (X * cos(theta) + Y * sin(theta)) ** 2 / a ** 2 + (
            X * sin(theta) - Y * cos(theta)) ** 2 / b ** 2


def _chk(theta, a, b, xc, yc, x, y):
    return eval_ellipse(theta, a, b, xc, yc, x, y) - 1e-5 < 1


def discard(a, b, X, Y):
    p = [np.array([X[i], Y[i]]) for i in range(3)]

    return np.linalg.norm(p[0] - p[1]) > 2 * a or np.linalg.norm(p[0] - p[2]) > 2 * a or np.linalg.norm(
        p[1] - p[2]) > 2 * a


def get_input(X, Y):
    x0 = X[0]
    y0 = Y[0]
    x1 = X[1] - x0
    x2 = X[2] - x0
    y1 = Y[1] - y0
    y2 = Y[2] - y0

    return x0, y0, x1, y1, x2, y2


def refine_root(f, cheb_poly, xroot, max_iter):
    pprime = cheb_poly.deriv()

    for i in range(max_iter):
        xroot -= cheb_poly(xroot) / pprime(xroot)

    return xroot


def get_cheb_poly(a: float, b: float, X: List[float], Y: List[float], deg=12, K=10):
    XX = [0, X[1]-X[0], X[2]-X[0]]
    YY = [0, Y[1]-Y[0], Y[2]-Y[0]]

    f = np.vectorize(fradius, excluded=[1, 2, 3, 4])

    Dm = pi / K
    ret = []

    for i in range(K):
        l = i * Dm
        r = (i + 1) * Dm
        ret.append(np.polynomial.chebyshev.Chebyshev.interpolate(f, deg=deg, domain=(l, r), args=(a, b, XX, YY)))

    return ret


def angle_error(theta, a, b, X, Y):
    px1, py1 = _tr(theta, b / a, X[1] - X[0], Y[1] - Y[0])
    px2, py2 = _tr(theta, b / a, X[2] - X[0], Y[2] - Y[0])
    (_, _), r = _ccirc(0, 0, px1, py1, px2, py2)

    return abs(r-b)


def get_center_from_angle(theta, a, b, X, Y):
    px1, py1 = _tr(theta, b / a, X[1] - X[0], Y[1] - Y[0])
    px2, py2 = _tr(theta, b / a, X[2] - X[0], Y[2] - Y[0])
    (xcc, ycc), r = _ccirc(0, 0, px1, py1, px2, py2)

    xc, yc = _tri(theta, b / a, xcc, ycc)

    return xc + X[0], yc + Y[0]


def e3pnt(a: float, b: float, X: List[float], Y: List[float]):

    t1 = time.time()
    pcoeff = exp_poly_coeff_t(a, b, X[1]-X[0], X[2]-X[0], Y[1]-Y[0], Y[2]-Y[0])

    #print(f'get_coeff_time: {time.time() - t1}')

    t1 = time.time()

    roo = np.roots(pcoeff)

    #print(pcoeff)

    roo = list(filter(lambda t: abs(np.absolute(t) - 1) < 1e-13, roo))
    roo = list(map(lambda t: np.angle(t)/2, roo))

    sols = []

    for theta in roo:
        xc, yc = get_center_from_angle(theta, a, b, X, Y)
        sols.append((xc, yc, theta))

    return sols


def e3pnt_cheb(a: float, b: float, X: List[float], Y: List[float]):
    if discard(a, b, X, Y):
        return []

    x0 = X[0]
    y0 = Y[0]
    X[0] -= x0
    Y[0] -= y0
    X[1] -= x0
    Y[1] -= y0
    X[2] -= x0
    Y[2] -= y0

    chebps = get_cheb_poly(a, b, X, Y, deg=32, K=1)
    angles = []

    for chebpoly in chebps:
        be = chebpoly.domain[0]
        en = chebpoly.domain[-1]

        roots = chebpoly.roots()
        roo = []
        for t in roots:
            if np.isreal(t) and be <= t.real <= en:
                roo.append(t.real)

        for r in roo:
            angles.append(refine_root(lambda tt: fradius(tt, a, b, X, Y), chebpoly, r.real, 0))

    ret = []

    for theta in angles:

        xc, yc = get_center_from_angle(theta, a, b, X, Y)

        ret.append((xc + x0, yc + y0, theta))

    return ret


def e3pnt_poly(a: float, b: float, X: List[float], Y: List[float]):
    # if discard(a, b, X, Y):
    #    return []

    x0, y0, x1, y1, x2, y2 = get_input(X, Y)

    coeff = poly_coeff(a, b, x1, x2, y1, y2)
    m = max(coeff)
    coeff = list(map(lambda x: x / m, coeff))

    print(coeff)

    ret = []

    roo = np.roots(coeff)

    print(min(abs(roo.imag)))
    print("-----")

    # print(roo)
    # print()
    # print("--------------")
    # print()

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
