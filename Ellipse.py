from __future__ import annotations
import numpy as np
import matplotlib as mp
from collections import namedtuple
from typing import Optional, List, Tuple
from math import sqrt, sin, cos

Point = namedtuple('Point', ['x', 'y'])


def dist(p: Point, q: Point):
    return sqrt((p.x - q.x) ** 2 + (p.y - q.y) ** 2)


def distsq(p: Point, q: Point):
    return (p.x - q.x) ** 2 + (p.y - q.y) ** 2


def rotate(p: Point, ang: float) -> Point:
    return Point(p.x * cos(ang) - p.y * sin(ang), p.x * sin(ang) + p.y * cos(ang))


class Ellipse:
    def __init__(self, a: float, b: float, cx=0, cy=0, weight=1, angle=0):
        self.a: float = a
        self.b: float = b
        self.cx: float = cx
        self.cy: float = cy
        self.weight: float = weight
        self.angle: float = angle
        self.is_rot = False

        if abs(angle) > 1e-9:
            self.is_rot = True

        self.dfx = lambda t: -self.a * np.cos(t)
        self.dfy = lambda t: self.b * np.sin(t)

    def fx(self, t: float):
        return self.cx + self.a * np.cos(t)

    def fy(self, t: float):
        return self.cy + self.b * np.sin(t)

    def set_center(self, p: Point):
        self.cx = p.x
        self.cy = p.y

    def set_angle(self, ang: float):
        self.is_rot = abs(ang) > 1e-9
        self.angle = ang

    def f(self, x: float, y: float):

        if self.is_rot:
            h = x - self.cx
            k = y - self.cy
            t = self.angle
            return (h * cos(t) + k * sin(t)) ** 2 / self.a ** 2 + (h * sin(t) - k * cos(t)) ** 2 / self.b ** 2

        return (x - self.cx) ** 2 / self.a ** 2 + (y - self.cy) ** 2 / self.b ** 2

    def inter(self, e2: Ellipse) -> Optional[List[Point, Point]]:
        """
        Returns the intersection points between two ellipses (axes parallel)
        >>> inter(e1, e2)
        :type e2: Ellipse
        """

        if self.a != e2.a or self.b != e2.b:
            raise Exception("ERROR: For now, the ellipses have to be equal and parallel to the axis.")

        h = e2.cx - self.cx
        k = e2.cy - self.cy
        a = self.a
        b = self.b

        d = 2 * h * b ** 2

        al = (-2 * k * a ** 2) / d
        be = (b ** 2 * h ** 2 + a ** 2 * k ** 2) / d

        ea = b ** 2 * al ** 2 + a ** 2
        eb = 2 * be * al * b ** 2
        ec = b ** 2 * be ** 2 - a ** 2 * b ** 2

        ro = np.roots([ea, eb, ec])

        if np.iscomplex(ro[0]):
            return None

        y1, y2 = ro
        # print("{}, {}".format(y1, y2))

        x1 = y1 * al + be
        x2 = y2 * al + be

        return [Point(x1 + self.cx, y1 + self.cy), Point(x2 + self.cx, y2 + self.cy)]
