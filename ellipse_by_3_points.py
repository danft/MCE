from Ellipse import *
from math import asin, atan, acos, atan2, sqrt, cos, sin, pi

def eq(x:float, y:float):
    return abs(x-y) < 1e-5

def ellipse_by_3_points(p1:Point, p2:Point, p3:Point, e:Ellipse)->Ellipse:
    p2 = Point(p2.x-p1.x, p2.y-p1.y)
    p3 = Point(p3.x-p1.x, p3.y-p1.y)

    den = (p3.y) * (p3.x-p2.x) - (p3.y-p2.y) * (p3.x)
    if (den == 0):
        raise Exception("The points cannot be colinear")

    q = e.a**2/e.b**2

    Det = (p3.x)*(p3.x-p2.x) + q * (p3.y)*(p3.y-p2.y)
    Det /= den

    A = (q**2 + Det**2)*p2.x**2 + q**2*(Det**2 + 1)*p2.y**2 + 2 * Det * (q - q**2)*p2.x*p2.y
    C = (q**2 + Det**2)*p2.y**2 + q**2*(Det**2 + 1)*p2.x**2 - 2 * Det * (q - q**2)*p2.x*p2.y
    B = Det*(q-q**2)*(p2.x**2 - p2.y**2) - (q**2 + Det**2)*p2.x*p2.y + q**2 * (Det**2+1)*p2.x*p2.y
    D = 4 * q**2 * e.a ** 2


    Ah = (A-C)/2
    Bh = B
    Ch = (A+C-2*D)/2

    theta = None

    if (eq(Ah,0) and eq(Bh,0)):
        theta = pi/2
    elif (eq(Ah,0)):
        theta = .5 * asin(-Ch / Bh)
    elif (eq(Bh, 0)):
        theta = .5 * acos(-Ch / Ah)
    else:
        theta = .5*atan((-sqrt(Ah**2 * Bh**2 + Bh**4 - Bh**2*Ch**2) - Ah*Ch)/ (Ah**2+Bh**2))

    #theta = atan((sqrt(Ah**2 * Bh**2 + Bh**4 - Bh**2*Ch**2) - Ah*Ch)/ (Ah**2+Bh**2))

    gamma = p2.x * cos(theta) - p2.y * sin(theta)
    delta = p2.x * sin(theta) + p2.y * cos(theta)

    cx = (gamma - Det * delta)/2
    cy = (q * delta + Det * gamma)/(2*q)

    print(cx, cy, theta)

    return e


ellipse_by_3_points(Point(0,0), Point(3, 2), Point(6,0), Ellipse(3, 2))
