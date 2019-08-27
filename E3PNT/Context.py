from Ellipse import *
from math import asin, atan, acos, atan2, sqrt, cos, sin, pi, tan, fabs
from enum import Enum


class Tr(Enum):
    Translation = 1,
    Rotation = 2,
    Mirror = 3


def apply_inverse_tr(t, x: float, y: float):
    tr, xh, yh = t

    if tr == Tr.Mirror:
        if xh > 0:
            return -x, y
        return x, -y

    if tr == Tr.Rotation:
        p = rotate(Point(x, y), -xh)
        return p.x, p.y

    if tr == Tr.Translation:
        return x-xh, y-yh


class Context:

    def __init__(self, a: float, b: float, x1, y1, x2, y2, x3, y3):
        self.a = a
        self.b = b
        self.p = [Point(x1, y1), Point(x2, y2), Point(x3, y3)]
        self.sort_points()
        self.d = distsq(self.p[0], self.p[1])
        self.h = 0
        self.transformations = []
        self.prep()

    def sort_points(self):
        d1 = dist(self.p[0], self.p[1])
        d2 = dist(self.p[0], self.p[2])
        d3 = dist(self.p[1], self.p[2])

        if d2 > d1 and d2 > d3:
            self.p[1], self.p[2] = self.p[2], self.p[1]
        elif d3 > d1 and d3 > d2:
            self.p[0], self.p[2] = self.p[2], self.p[0]

    def output_center(self, xc, yc):
        for t in reversed(self.transformations):
            xc, yc = apply_inverse_tr(t, xc, yc)

        return Point(xc, yc)

    def output_angle(self, theta):
        for t in reversed(self.transformations):

            if t[0] == Tr.Rotation:
                theta += -t[1]

            elif t[0] == Tr.Mirror:
                if t[1] == 1:
                    theta = pi - theta
                else:
                    theta = -theta

        return theta

    def x_mirror(self):
        self.p[2] = Point(-self.p[2].x, self.p[2].y)
        self.transformations.append((Tr.Mirror, 1, 0))

    def y_mirror(self):
        self.p[2] = Point(self.p[2].x, -self.p[2].y)
        self.transformations.append((Tr.Mirror, 0, 1))

    def px(self, theta):
        return self.h * cos(theta)

    def py(self, theta):
        return self.h * sin(theta)

    def prep(self):

        # translations
        xt = self.p[0].x

        yt = self.p[0].y
        self.transformations.append((Tr.Translation, -xt, -yt))

        self.p[1] = Point(self.p[1].x - xt, self.p[1].y - yt)
        self.p[2] = Point(self.p[2].x - xt, self.p[2].y - yt)
        self.p[0] = Point(self.p[0].x - xt, self.p[0].y - yt)

        # rotation
        rot = -atan2(self.p[1].y, self.p[1].x)
        self.transformations.append((Tr.Rotation, rot, 0))

        self.p[1] = rotate(self.p[1], rot)
        self.p[2] = rotate(self.p[2], rot)

        self.h = sqrt(self.d) / 2

        self.transformations.append((Tr.Translation, -self.h, 0))
        for i in range(3):
            self.p[i] = Point(self.p[i].x - self.h, self.p[i].y)

        # mirroring
        if self.p[2].y > 0:
            self.transformations.append((Tr.Mirror, 0, 1))
            self.p[2] = Point(self.p[2].x, -self.p[2].y)

        if self.p[2].x > 0:
            self.transformations.append((Tr.Mirror, 1, 0))
            self.p[2] = Point(-self.p[2].x, self.p[2].y)

    def formatPoints(self):
        return f"(0, 0)\n({self.p[1].x}, {self.p[1].y})\n({self.p[2].x}, {self.p[2].y})"

# ip=Input(3, 2, Point(1, 1), Point(1, 20), Point(-6, 7))
# print(ip.formatPoints())
# print(ip.rot)
