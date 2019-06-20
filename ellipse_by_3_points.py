from Ellipse import *
from math import asin, atan, acos, atan2, sqrt, cos, sin, pi, tan, fabs


def eq(x: float, y: float):
    return abs(x - y) < 1e-5


def ellipse_by_3_points(h: float, l: float, m: float, e: Ellipse, return_conic_equation = False) -> list:
    """
    For now it returns five parameters of the conic equation A,B,C,D,E
    Assumes that the three points are in the following order:
    p1p2 is the longest segment
    p1 is (0,0)
    p2 is (h, 0)
    p3 is (lh, lhm)
    :return: Five parameters of a conic with the same shape as the ellipse passed as parameter.
    """

    if l - 1e-9 < 0:
        raise Exception("The parameter `l` must be positive.")

    if m - 1e-9 < 0:
        raise Exception("The parameter `m` must be positive.")

    a = e.a
    b = e.b
    w = (a ** 2 - b ** 2) / (a ** 2 + b ** 2)

    # simple function that returns the conic equation given an angle of rotation
    def geteq(theta):
        t = tan(2 * theta)

        A = (-w + sqrt(t ** 2 + 1)) / (2 * t * w)
        B = -1
        C = A + 1 / t
        beta = (A * (1 - l) + l * m - C * m ** 2 * l) / m

        H = (4 * A * C - B ** 2) * (A + C - sqrt((A - C) ** 2 + B ** 2))
        h = (a ** 2 * H) / (2 * (A * beta ** 2 - A * beta + C * A ** 2))
        D = -A * h
        E = h * beta

        return A, B, C, D, E, 0


    # first lets define a function that returns the squared legnth of the triangle which is simillar to the one formed
    # by the points given and is inscribed in the ellipse rotated by an angle of theta, 0 < theta < pi/4
    def g(theta):
        if theta < 0 or theta > pi / 4:
            raise Exception("Angle of rotation is invalid.")

        t = tan(2 * theta)

        A = (-w + sqrt(t ** 2 + 1)) / (2 * t * w)
        B = -1
        C = A + 1 / t
        beta = (A * (1 - l) + l * m - C * m ** 2 * l) / m

        H = (4 * A * C - B ** 2) * (A + C - sqrt((A - C) ** 2 + B ** 2))

        return (a ** 2 * H) / (2 * (A * beta ** 2 - A * beta + C * A ** 2))

    tmax = ternary_search(g, 0, pi / 4)
    hmax = g(tmax)

    # If the maximum of the function is less than we are looking for we wont find any solution.
    if hmax < h ** 2:
        return []

    s1 = bissec(g, 0, tmax, h*h)
    hs1 = sqrt(g(s1))
    s2 = bissec(lambda theta: -g(theta), tmax, pi/4, -h*h)
    hs2 = sqrt(g(s2))

    print(f"s1: {s1} -> {sqrt(g(s1))}")
    print(f"s2: {s2} -> {sqrt(g(s2))}")

    Sols = []
    ss = [s1, s2]

    for s in ss:
        hs = sqrt(g(s))
        if (fabs(hs - h) < 1e-6):
            Sols.push(geteq(s))

    return Sols



    print(sqrt(g(tmax)))
    return tmax


def bissec(f, l, r, x):
    """
    Assumes that f is increasing
    :param f: the function
    :param l: defines the search interval.
    :param r: defines the search interval.
    :param x: the value to be found.
    :return: the point which most approximates x.
    """

    ans = (l+r)/2
    while (r-l > 1e-15):
        mi = (l+r)/2
        ans = mi
        if f(mi) < x:
            l = mi
        else:
            r = mi

    return ans


def ternary_search(f, l, r):
    """
    Finds the maximum of function f using a ternary search.
    :param f: the function to be maximized, f is unimodal.
    :param l: defines the interval to search.
    :param r: defines the interval to search.
    :return: the point which maximizes the function f.
    """
    ans = (l + r) / 2

    while r - l > 1e-9:
        m1 = l + (r - l) / 3
        m2 = r - (r - l) / 3
        ans = (m1 + m2) / 2

        if f(m1) < f(m2):
            l = m1
        else:
            r = m2

    return ans
