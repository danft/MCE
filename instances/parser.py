from collections import namedtuple

instance = namedtuple('instance', ['n', 'm', 'X', 'Y', 'a', 'b', 'point_weight', 'ellipse_weight', 'k'])


def parse_input(filename: str):
    f = open(filename, 'r')
    m = int(f.readline())
    k = int(f.readline())

    ellipse_weight = []

    a = []
    b = []

    for i in range(m):
        ai, bi = f.readline().split()
        ai = float(ai)
        bi = float(bi)
        a.append(ai)
        b.append(bi)

    for i in range(m):
        w = float(f.readline())
        ellipse_weight.append(w)

    X = []
    Y = []
    n = int(f.readline())

    for i in range(n):
        x, y = f.readline().split()
        x = float(x)
        y = float(y)
        X.append(x)
        Y.append(y)

    point_weight = []

    for i in range(n):
        w = float(f.readline())
        point_weight.append(w)

    return instance(n, m, X, Y, a, b, point_weight, ellipse_weight, k)
