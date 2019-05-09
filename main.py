from Ellipse import *
from MCE import *
from plots import *
import numpy as np

E1 = Ellipse(2, 1.3, 0, 0)
E2 = Ellipse(2, 1.3, 0.7, 0.7)

#print(E1.inter(E2))

n=3
xs = 3 * np.random.rand(n)
ys = 3 * np.random.rand(n)

xs = [-0.1, 1, 2]
ys = [0, 1.4, 0]

#plot_max_clique_instance(xs,ys,E1)
#plot_ellipse_candidate_list(xs, ys, E1)

print(MCE(xs, ys, [E1]))

#plot_mce_instance(xs, ys, [E1])
#plot_ellipse_inter([E1, E2])
