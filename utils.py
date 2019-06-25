# contains some utility functions

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