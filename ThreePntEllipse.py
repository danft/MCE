from Ellipse import *
from math import asin, atan, acos, atan2, sqrt, cos, sin, pi, tan, fabs
from utils import *



class ThreePntEllipseCtx:
    def __init__(self, a:float, b:float, p1:Point, p2:Point, p3:Point):
        self.a=a
        self.b=b
        self.p=[p1,p2,p3]
        self.rearrangeByDist()
        self.rot=0
        self.ymirror = False
        self.xt=0
        self.yt=0
        self.prep()
        self.m=1
        self.l=0

    def rearrangeByDist(self):
        d1 = dist(self.p[0], self.p[1])
        d2 = dist(self.p[0], self.p[2])
        d3 = dist(self.p[1], self.p[2])

        if d2 > d1 and d2 > d3:
            self.p[1], self.p[2] = self.p[2], self.p[1]
        elif d3 > d1 and d3 > d2:
            self.p[0], self.p[2] = self.p[2], self.p[0]

    def prep(self):

        # translations
        self.xt = self.p[0].x
        self.yt = self.p[0].y
        self.p[1] = Point(self.p[1].x - self.xt, self.p[1].y-self.yt)
        self.p[2] = Point(self.p[2].x - self.xt, self.p[2].y-self.yt)
        self.p[0] = Point(0,0)

        # rotation
        self.rot = -atan2(self.p[1].y, self.p[1].x)
        self.p[1] = Point(dist(self.p[0], self.p[1]), 0)
        self.p[2] = rotate(self.p[2], self.rot)

        # mirroring
        if (self.p[2].y < 0):
            self.ymirror = True
            self.p[2].y = -self.p[2].y

        self.m = self.p[2].y/self.p[2].x
        self.l = self.p[2].x/self.p[1].x
        self.h = self.p[1].x

    def formatPoints(self):
        return f"(0, 0)\n({self.p[1].x}, {self.p[1].y})\n({self.p[2].x}, {self.p[2].y})"


class ThreePntEllipseHelper():
    def __init__(self, ctx:ThreePntEllipseCtx):
        self.ctx = ctx
        self.w = (self.ctx.a ** 2 - self.ctx.b ** 2) / (self.ctx.a ** 2 + self.ctx.b ** 2)

    def getEq(self, theta):
        t = tan(2 * theta)

        A = (-self.w + sqrt(t ** 2 + 1)) / (2 * t * self.w)
        B = -1
        C = A + 1 / t
        beta = (A * (1 - self.ctx.l) + self.ctx.l * self.ctx.m - C * self.ctx.m ** 2 * self.ctx.l) / self.ctx.m

        H = (4 * A * C - B ** 2) * (A + C - sqrt((A - C) ** 2 + B ** 2))
        h = (self.ctx.a ** 2 * H) / (2 * (A * beta ** 2 - A * beta + C * A ** 2))
        D = -A * h
        E = h * beta

        return A, B, C, D, E, 0


    def getEqStr(self, theta):
        A, B, C, D, E, F = self.getEq(theta)
        return f"{A}x^2 + {B}xy + {C}y^2 + {D}x + {E}y + {F} = 0"


    def g(self, theta):
        if theta < 0 or theta > pi / 4:
            raise Exception("Angle of rotation is invalid.")

        t = tan(2 * theta)

        A = (-self.w + sqrt(t ** 2 + 1)) / (2 * t * self.w)
        B = -1
        C = A + 1 / t
        beta = (A * (1 - self.ctx.l) + self.ctx.l * self.ctx.m - C * self.ctx.m ** 2 * self.ctx.l) / self.ctx.m

        H = (4 * A * C - B ** 2) * (A + C - sqrt((A - C) ** 2 + B ** 2))

        return (self.ctx.a ** 2 * H) / (2 * (A * beta ** 2 - A * beta + C * A ** 2))




def ThreePntEllipse(ctx:ThreePntEllipseCtx):
    helper = ThreePntEllipseHelper(ctx)

    # first case a > b
    tmax = ternary_search(helper.g, 0, pi / 4)
    hmax = helper.g(tmax)

    print(f"tmax:{tmax}, hmax:{sqrt(hmax)}")
    h = ctx.h

    # If the maximum of the function is less than we are looking for we wont find any solution.
    if hmax < h ** 2:
        return []

    s1 = bissec(helper.g, 0, tmax, h*h)
    hs1 = sqrt(helper.g(s1))
    s2 = bissec(lambda theta: -helper.g(theta), tmax, pi/4, -h*h)
    hs2 = sqrt(helper.g(s2))

    print(f"s1: {s1} -> {sqrt(helper.g(s1))}")
    print(f"s2: {s2} -> {sqrt(helper.g(s2))}")

    Sols = []
    ss = [s1, s2]

    print(ctx.formatPoints())

    for s in ss:
        hs = sqrt(helper.g(s))
        print(hs, h)
        if (fabs(hs - h) < 1e-6):
            Sols.append(helper.getEq(s))
            print(helper.getEqStr(s))

    return Sols

def _verticalMajor(ctx:ThreePntEllipseCtx):

    if ctx.a > ctx.b:
        ctx.a, ctx.b = ctx.b, ctx.a

    helper = ThreePntEllipseHelper(ctx)

### Testing
ctx=ThreePntEllipseCtx(3, 2, Point(1, 1), Point(2.2, 2), Point(3.5, 1))
ThreePntEllipse(ctx)
