from math import sqrt, cos, sin, atan, pi
from Ellipse import *

def rot(x, y, theta):
    return x * cos(theta) - y * sin(theta), x * sin(theta) + y * cos(theta)


def distsq(X, Y):
    return (X[0]-X[1])**2 + (Y[0]-Y[1])**2


def two_point_ellipse(a, b, x1, y1, x2, y2, do_rot=True):
    X = [x1, x2]
    Y = [y1, y2]

    if X[1] == X[0]:
        theta = pi/2
    else:
        m = (Y[1] - Y[0]) / (X[1] - X[0])
        theta = atan(m)

    if do_rot:
        for i in range(len(X)):
            X[i], Y[i] = rot(X[i], Y[i], -theta)
    else:
        theta = 0

    m = (Y[1] - Y[0]) / (X[1] - X[0])
    D = distsq(X, Y)
    A = 4 * a ** 2 * b ** 2 + 4 * a ** 2 * b ** 2 * m ** 2
    B = a ** 2 * m ** 2 + b ** 2

    if B * A - D * B ** 2 < 0:
        return []

    c = sqrt((B * A - D * B ** 2) / A)

    ret = []

    for i in range(2):

        x1 = (-a ** 2 * m * c - a * b * sqrt(a ** 2 * m ** 2 + b ** 2 - c ** 2)) / (a ** 2 * m ** 2 + b ** 2)
        x2 = (-a ** 2 * m * c + a * b * sqrt(a ** 2 * m ** 2 + b ** 2 - c ** 2)) / (a ** 2 * m ** 2 + b ** 2)
        if x1 > x2:
            x2, x1 = x1, x2

        y2 = x2 * m + c
        y1 = x1 * m + c

        if X[0] < X[1]:
            xc = -x1 + X[0]
            yc = -y1 + Y[0]
        else:
            xc = -x2 + X[0]
            yc = -y2 + Y[0]

        xc, yc = rot(xc, yc, theta)
        ret.append((Point(xc, yc), theta))
        c *= -1

    return ret
