import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mp
from MCE import *

class _Plot:
    def __init__(self, fnum=1, xlim=[-5,5], ylim=[-5,5]):
        self.fig, self.ax = plt.subplots(fnum,subplot_kw={'aspect':'equal', 'xlim':xlim, 'ylim':ylim})

    def plot_points(self, X, Y, **kwargs):
        plt.scatter(X, Y, s=10, **kwargs)

    def plot_point(self, x:float, y:float):
        self.plot_points([x], [y])

    def plot_ellipse(self, E, color='black'):
        self.plot_points([E.cx], [E.cy], color=color)
        epatch = mp.patches.Ellipse([E.cx, E.cy], 2 * E.a, 2 * E.b, fill=False, color=color)
        self.ax.add_artist(epatch)

    def close(self):
        plt.close(self.fig)


def plot_mce_instance(X, Y, Elist):
    xplt = _Plot()

    xplt.plot_points(X,Y)

    for e in Elist:
        xplt.plot_ellipse(e)

    plt.show()

def plot_ellipse_inter(Elist:list):
    xplt = _Plot()

    for e in Elist:
        xplt.plot_ellipse(e)
        xplt.plot_point(e.cx, e.cy)

    m=len(Elist)
    for i in range(m):
        for j in range(i+1,m):
            r = Elist[i].interangles(Elist[j])
            if r == None:
                continue

            a1, a2 = r
            xplt.plot_points([Elist[i].fx(a1), Elist[i].fx(a2)], [Elist[i].fy(a1), Elist[i].fy(a2)], color='red')

            #xplt.plot_points([r[0].x, r[1].x], [r[0].y, r[1].y])

    plt.show()
    xplt.close()

def plot_ellipse_candidate_list(X, Y, E):

    xplt = _Plot(1)
    xplt.plot_points(X,Y)

    plt.show()

    for i in range(len(X)):
        xplt.plot_ellipse(Ellipse(E.a, E.b, X[i], Y[i]), color='black')

    zs = MCE1(X, Y, E)

    for z in zs:
        xplt.plot_ellipse(Ellipse(E.a, E.b, z.p.x, z.p.y), color='red')

    plt.show()
    xplt.close()

def plot_max_clique_instance(X, Y, E, fnum=None):
    xplt = _Plot(fnum)
    xplt.plot_points(X,Y)

    for i in range(len(X)):
        xplt.plot_ellipse(Ellipse(E.a, E.b, X[i], Y[i]), color='black')

    plt.show()
    xplt.close()
