import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mp

def plot_mce_instance(X,Y,E):
    #plt.figure()
    fig, ax = plt.subplots(subplot_kw={'aspect': 'equal'})
    ax.set_xlim(-10,10)
    ax.set_ylim(-10,10)

    plt.scatter(X,Y)
    elpatches = [mp.patches.Ellipse([e.cx, e.cy], e.a, e.b, fc='orange', fill=False) for e in E]

    for e in elpatches:
        ax.add_artist(e)

    plt.show()


def plot_ellipse_inter(E:list):
    fig, ax = plt.subplots(subplot_kw={'aspect':'equal', 'xlim':[-2,2], 'ylim':[-2,2]})

    for e in E:
        ax.add_artist(mp.patches.Ellipse([e.cx, e.cy], e.a, e.b, fc='orange', fill=False))
        plt.scatter(e.cx, e.cy)

    m=len(E)
    for i in range(m):
        for j in range(i+1,m):
            r = E[i].inter(E[j])
            if r is None:
                continue

            print(r)
            plt.scatter([r[0].x, r[1].x], [r[0].y, r[1].y])

    plt.show()
