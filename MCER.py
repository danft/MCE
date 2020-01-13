from E3PNT.e3pnt import *
from E2PNT.TwoPointEllipse import *
from Tree import *
import time


class Cover:
    center: Point
    angle: float
    cov: List[int]
    mask: int

    def __init__(self, ce=Point(0, 0), an=0):
        self.center = Point(ce[0], ce[1])
        self.angle = an
        self.cov = []
        self.mask = 0

    def __str__(self):
        return f"({self.center.x}, {self.center.y}) {self.angle}"

    def __repr__(self):
        return self.__str__()

    def add_cov(self, u: int):
        self.cov.append(u)
        self.mask |= 1 << u


def eval_cover(X, Y, e:Ellipse, c:Cover):
    val = 0
    e.set_angle(c.angle)
    e.set_center(c.center)

    for ix in range(len(X)):
        val += e.f(X[ix], Y[ix]) - 1e-13 < 1

    return val


def MCER1(X, Y, e: Ellipse) -> Cover:
    n = len(X)

    best_cover = Cover(Point(0, 0), 0)
    vbest_cover = 0

    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                sl = e3pnt(e.a, e.b, [X[i], X[j], X[k]], [Y[i],Y[j], Y[k]])

                for s in sl:
                    c = Cover(Point(s[0], s[1]), s[2])

                    val = eval_cover(X, Y, e, c)

                    if val > vbest_cover:
                        vbest_cover = val
                        best_cover = c

    for i in range(n):
        for j in range(i+1, n):

            sl = two_point_ellipse(e.a, e.b, X[i], Y[i], X[j], Y[j])

            for s in sl:
                c = Cover(s[0], s[1])
                val = eval_cover(X, Y, e, c)

                if val > vbest_cover:
                    vbest_cover = val
                    best_cover = c

    return best_cover


def _MCER1(X, Y, e:Ellipse) -> List[Cover]:

    n = len(X)

    covers = []

    T = Tree(n)

    def add_coverage(cc: Cover):
        e.set_center(cc.center)
        e.set_angle(cc.angle)

        for i in range(n):
            if e.f(X[i], Y[i]) - 1e-13 < 1:
                cc.add_cov(i)

    pr_cov = []

    for i in range(n):
        c = Cover(Point(X[i], Y[i]), 0)
        add_coverage(c)

        if not T.has(c.cov):
            T.add_nodes(c.cov)
            pr_cov.append(c)

        for j in range(i+1, n):
            sl = two_point_ellipse(e.a, e.b, X[i], Y[i], X[j], Y[j])

            for s in sl:
                c = Cover(s[0], s[1])
                add_coverage(c)

                if not T.has(c.cov):
                    T.add_nodes(c.cov)
                    pr_cov.append(c)

            for k in range(j+1, n):
                sl = e3pnt(e.a, e.b, [X[i], X[j], X[k]], [Y[i], Y[j], Y[k]])

                for s in sl:
                    c = Cover(Point(s[0], s[1]), s[2])
                    add_coverage(c)

                    if not T.has(c.cov):
                        T.add_nodes(c.cov)
                        pr_cov.append(c)

    pr_cov.sort(key=lambda x: len(x.cov), reverse=True)
    T = Tree(n)

    for c in pr_cov:
        if not T.has(c.cov):
            covers.append(c)
            T.add_nodes(c.cov)

    return covers


class _MCER:
    is_cov: List[int]
    X: List[float]
    Y: List[float]
    e: List[Ellipse]
    n: int
    m: int
    covers: List[List[Cover]]
    curr: List[Cover]
    best_val: float
    best_sol: List[Cover]
    dp: dict

    def __init__(self, X, Y, a, b):
        self.n = len(X)
        self.m = len(a)
        self.X = X
        self.Y = Y
        self.covers = [[] for i in range(self.m)]
        self.e = []

        for i in range(self.m):
            self.e.append(Ellipse(a[i], b[i]))

        self.a = a
        self.b = b
        self.is_cov = [0] * self.n
        self.curr = [Cover()] * self.m
        self.best_val = 0
        self.best_sol = [Cover()] * self.m
        self.nsols_eval = 0
        self.start_time = 0

        self.dp = [dict() for i in range(self.m)]

    def _f(self, i: int, mask):

        if i == self.m:

            cnt = bin(mask).count('1')

            if cnt > self.best_val:
                self.best_val = cnt
                self.best_sol = self.curr.copy()

            self.nsols_eval += 1
            if self.nsols_eval % 10000000 == 0:
                print(f"[{self.nsols_eval}] - best sol: {self.best_val}, time so far: {time.time() - self.start_time}")
                print(f"[0]: {len(self.dp[0])}, [1]: {len(self.dp[1])}")

            return cnt

        if self.dp[i].get(mask, -1) > 0:
            #print(f"AAAA: {i, mask}")
            return self.dp[i].get(mask, -1)

        bsol = 0

        for c in self.covers[i]:

            if c.mask | mask == mask:
                continue

            self.curr[i] = c
            bsol = max(bsol, self._f(i+1, mask | c.mask))

        if len(self.dp[i]) < 10000000:
            self.dp[i][mask] = bsol

        return bsol

    def f(self):
        start_time = time.time()

        tcov = 0
        for i in range(self.m):
            self.covers[i] = _MCER1(self.X, self.Y, self.e[i])
            print(f"ellipse[{i}]: {len(self.covers[i])}")
            tcov += len(self.covers[i])

        print(f"avg cov. size: {tcov/self.m}")

        second_stage = time.time()
        self.start_time = time.time()

        print(f"t1: {second_stage-start_time}")

        self._f(0, 0)

        third_stage = time.time()

        print(f"t2: {third_stage - start_time}")

        print(f"Size of DP: {len(self.dp)}")

        return self.best_val, self.best_sol


def MCER(X, Y, a, b):

    helper = _MCER(X, Y, a, b)

    return helper.f()


