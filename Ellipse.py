import numpy as np

class Ellipse:
    def __init__(self, a, b, cx=0, cy=0, weight=1):
        self.a=a
        self.b=b
        self.cx=cx
        self.cy=cy
        self.weight=weight
        self.dfx = lambda t: -self.a * np.cos(t)
        self.dfy = lambda t: self.b * np.sin(t)

    def fx(self, t):
        return self.a * np.cos(t)
    def fy(self, t):
        return self.b * np.sin(t)

    def angle(self, p):
        """
        Function to get the polar angle of a point.
        :param p: the point which one wants to find the angle.
        :return: the pollar angle of point p=(x,y) in respect to the ellipse.
        """
        return np.arctan2(self.a * (p.y - self.cy), self.b * (p.x - self.cx))

    def interangles(self, e2):
        ret = self.inter(e2)

        if ret == None:
            return None

        s1 = self.angle(ret[0])
        s2 = self.angle(ret[1])
        t1 = self.angle(ret[0])
        t2 = self.angle(ret[1])

        if np.cross([self.dfx(s1), self.dfy(s1)], [-e2.dfx(t1), -e2.dfy(t1)]) >= 0:
            return s1, s2

        return s2,s1

    def inter(self, e2):
        """
        Returns the intersection points between two ellipses
        >>> inter(e1, e2)
        :type e2: Ellipse
        """

        if self.a != e2.a:
            raise Exception("ERROR: For now, the ellipses have to be equal and parallel to the axis.")

        h = e2.cx - self.cx
        k = e2.cy - self.cy
        a = self.a
        b = e2.b

        aa = (-2*k*a**2) / (2*h*b**2)
        bb = (b**2*h**2 + a**2*k**2) / (2*h*b**2)

        ro = np.roots([b**2*aa**2+a**2, 2*bb*aa*b**2, b**2*bb**2 - a**2*b**2])

        if np.iscomplex(ro[0]):
            return None

        y1, y2 = ro

        x1 = y1 * aa + bb
        x2 = y2 * aa + bb

        return [(x1 + self.cx, y1 + self.cy), (x2 + self.cx, y2 + self.cy)]
