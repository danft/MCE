from Ellipse import *
from MCE import *
from plots import *
import numpy as np

E1 = Ellipse(2, 1, 0, 0)
E2 = Ellipse(2, 1, 0.6, 0.6)

#print(E1.inter(E2))

n=3
xs = np.random.rand(n)
ys = np.random.rand(n)

#print(MCE(xs, ys, [E1]))

#plot_mce_instance(xs, ys, [E1])
plot_ellipse_inter([E1, E2])
