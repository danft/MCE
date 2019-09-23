from math import cos, sin

# contains some utility functions


def distsq(X, Y):
    x = X[0] - X[1]
    y = Y[0] - Y[1]

    return x*x + y*y


def rot(theta, x, y):
    return x * cos(theta) + y * sin(theta), x * sin(theta) - y * cos(theta)


def area(X, Y):
    ux1 = X[1] - X[0]
    uy1 = Y[1] - Y[0]

    ux2 = X[2] - X[0]
    uy2 = Y[2] - Y[0]

    return .5 * abs(ux1 * uy2 - uy1 * ux2)


def bisec_inc(f, l, r, x):
    """
    Assumes that f is increasing
    :param f: the function
    :param l: defines the search interval.
    :param r: defines the search interval.
    :param x: the value to be found.
    :return: the point which most approximates x.
    """

    ans = (l+r)/2
    while r-l > 1e-13:
        mi = (l+r)/2
        ans = mi
        if f(mi) < x:
            l = mi
        else:
            r = mi

    return ans


def find_max(f, l, r):
    """
    Finds the maximum of function f using a ternary search.
    :param f: the function to be maximized, f is unimodal.
    :param l: defines the interval to search.
    :param r: defines the interval to search.
    :return: the point which maximizes the function f.
    """
    ans = (l + r) / 2

    while r - l > 1e-13:
        m1 = l + (r - l) / 3
        m2 = r - (r - l) / 3
        ans = (m1 + m2) / 2

        if f(m1) < f(m2):
            l = m1
        else:
            r = m2

    return ans


def find_min(f, l, r):
    return find_max(lambda theta: -f(theta), l, r)


def bisec_dec(f, l, r, x):
    return bisec_inc(lambda theta: -f(theta), l, r, -x)


def is_inc(f, x):
    """
    Returns True if the function is increasing
    """
    eps = 1e-9
    return f(x + eps) > f(x)
