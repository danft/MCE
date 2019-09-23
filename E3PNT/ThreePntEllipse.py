from E3PNT.Context import *
from math import asin, atan, acos, atan2, sqrt, cos, sin, pi, tan, fabs
from utils import *


class Helper:
    def __init__(self, ctx: Context):
        self.ctx = ctx

    def get_center(self, theta):
        m = tan(theta)
        a = self.ctx.a
        b = self.ctx.b
        B = a * a * m * m + b * b
        A = 4 * a * a * b * b * (1 + m * m)
        try:
            c = sqrt((B * A - self.ctx.d * B * B) / A)
            xd = (-a ** 2 * m * c + a * b * sqrt(a ** 2 * m ** 2 + b ** 2 - c ** 2)) / (a ** 2 * m ** 2 + b ** 2)
        except:
            print(theta, "DEBUG: ", (B * A - self.ctx.d * B ** 2) / A)
            raise Exception("ctc", self.ctx)

        yd = xd * m + c

        ppx = self.ctx.px(theta)
        ppy = self.ctx.py(theta)
        bx = xd - ppx
        by = yd - ppy

        xc = bx * cos(theta) + by * sin(theta)
        yc = bx * sin(theta) - by * cos(theta)
        return xc, yc

    def g(self, theta):

        xc, yc = self.get_center(theta)

        x, y = self.ctx.p[2].x, self.ctx.p[2].y

        return (((x - xc) * cos(theta) + (y - yc) * sin(theta)) / self.ctx.a) ** 2 + (((x - xc) * sin(theta) - (y - yc) * cos(theta)) / self.ctx.b) ** 2


def get_upper_limit(ctx: Context):
    a = ctx.a
    b = ctx.b
    D = ctx.d

    if D > 4 * a * a:
        return 0

    if D < 4 * b * b:
        return pi / 2

    # print((D/4-b**2)/(a*a-b*b), "bla")

    t1 = acos(sqrt((D - 4 * b * b) / (4 * a * a - 4 * b * b)))
    if t1 < 1e-11:
        return 0

    return atan((b * sin(t1)) / (a * cos(t1)))


def get_transitions(ctx: Context):
    ga = -ctx.d * ctx.a ** 4
    gb = 2 * ctx.a ** 2 * ctx.b ** 2 * (2 - ctx.d)
    gc = 4 * ctx.a ** 2 * ctx.b ** 4 - ctx.d * ctx.b ** 4

    if gb ** 2 - 4 * ga * gc < 0:
        m1 = 0
    else:
        m1 = (-gb - sqrt(gb ** 2 - 4 * ga * gc)) / (2 * ga)

    ga = 4 * ctx.a ** 4 * ctx.b ** 2 - ctx.d * ctx.a ** 4
    gb = 4 * ctx.a ** 4 * ctx.b - 2 * ctx.d * ctx.a ** 2 * ctx.b ** 2
    gc = - ctx.d * ctx.b ** 2

    if gb ** 2 - 4 * ga * gc < 0:
        m2 = 0
    else:
        m2 = (-gb + sqrt(gb ** 2 - 4 * ga * gc)) / (2 * ga)

    return [atan(sqrt(m1)), atan(sqrt(m2))]


def three_point_ellipse_i(ctx: Context):
    # tr = get_transitions(ctx)
    tu = get_upper_limit(ctx)

    # ta = min(tr[0], tr[1], tu)
    # tb = min(tu, max(tr[0], tr[1]))
    ta = tu * 1 / 3
    tb = tu * 2 / 3

    f1 = f_range(ctx, 0, ta)
    f2 = f_range(ctx, ta, tb)
    f3 = f_range(ctx, tb, tu)
    f1.extend(f2)
    f1.extend(f3)

    return f1


def three_point_ellipse(a: float, b: float, x1, y1, x2, y2, x3, y3):
    ret = []
    ctx = Context(a, b, x1, y1, x2, y2, x3, y3)
    helper = Helper(ctx)

    solutions = []

    def get_solution(s):
        xc, yc = helper.get_center(s)
        ctr = ctx.output_center(xc, yc)
        ang = ctx.output_angle(s)
        return ctr, ang

    s1 = three_point_ellipse_i(ctx)
    for s in s1:
        solutions.append(get_solution(s))

    ctx.x_mirror()
    s2 = three_point_ellipse_i(ctx)
    for s in s2:
        solutions.append(get_solution(s))

    ctx.y_mirror()
    s3 = three_point_ellipse_i(ctx)
    for s in s3:
        solutions.append(get_solution(s))

    ctx.x_mirror()
    s4 = three_point_ellipse_i(ctx)
    for s in s4:
        solutions.append(get_solution(s))

    return solutions


def f_range(ctx: Context, l: float, r: float) -> list:
    helper = Helper(ctx)

    if r - 1e-9 < l:
        return []

    if is_inc(helper.g, l):
        return f_range_inc(ctx, l, r)
    return f_range_dec(ctx, l, r)


def f_range_inc(ctx: Context, l, r):
    helper = Helper(ctx)
    tmax = find_max(helper.g, l, r)

    s = [bisec_inc(helper.g, l, tmax, 1), bisec_dec(helper.g, tmax, r, 1)]
    ret = []
    for xs in s:
        if fabs(helper.g(xs) - 1) < 1e-9:
            ret.append(xs)

    return ret


def f_range_dec(ctx: Context, l, r):
    helper = Helper(ctx)
    tmin = find_min(helper.g, l, r)
    s = [bisec_dec(helper.g, l, tmin, 1), bisec_inc(helper.g, tmin, r, 1)]
    # print(tmin)
    ret = []
    for xs in s:
        if fabs(helper.g(xs) - 1) < 1e-9:
            ret.append(xs)

    return ret

# Testing
# ctx = Context(2.7, 1, Point(-0.95, 0), Point(0.95, 0), Point(-2.18, -1.8))
# ss = ThreePntEllipse(ctx)
# print(ss)

# arr = np.linspace(0.0001, pi / 2 - 0.00001, 2000)
# helper = Helper(ctx)
# ds = [helper.g(x) for x in arr]


# ThreePntEllipse(ctx)
