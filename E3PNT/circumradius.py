from utils import distsq, area
from math import cos, sin


def _tr(theta, q, x, y):
    return q * (x * cos(theta) + y * sin(theta)), -x * sin(theta) + y * cos(theta)


#@guvectorize([(float64, float64, float64, float64[:], float64[:])], '(),(),(),(n),(n)->()')
def fradius(theta, a, b, X, Y):
    ph = [_tr(theta, b / a, X[i], Y[i]) for i in range(3)]

    PX = [p[0] for p in ph]
    PY = [p[1] for p in ph]

    du = distsq([PX[0], PX[1]], [PY[0], PY[1]])
    dv = distsq([PX[1], PX[2]], [PY[1], PY[2]])
    dw = distsq([PX[0], PX[2]], [PY[0], PY[2]])

    A = area(PX, PY)

    return b ** 2 * 16 * A ** 2 - du * dv * dw
