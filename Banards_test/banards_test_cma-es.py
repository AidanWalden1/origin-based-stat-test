import numpy as np
import matplotlib.pyplot as plt

from optimizers.cma_es import CMAESOptimizer
from optimizers.woa import WoaOptimizer


num_tests = 500


random_individuals = np.empty(num_tests, dtype=object)


xmin, xmax = -1, 7
ymin, ymax = -3, 5


def dummy_objective_function(x):
    return 0


plt.xlim(xmin, xmax)
plt.ylim(ymin, ymax)
    
m = (ymax - ymin)/(xmax-xmin)
b = (ymax - (m*xmax))

x = np.linspace(xmin, xmax)
y = m * x + b
plt.plot(x, y, color="green")
    
m2 = -1 *m
b2 = 0
x2 = np.linspace(xmin, xmax)
y2 = m2 * x2 + b2
#plt.plot(x2, y2, color="blue")
    

x3 = (b2-b)/(m-m2)
y3 = m*x3 +b

x3 = x3*2
y3 = y3*2




def bimodal_objective(x):
    """
    Computes the value of a bimodal objective function at point x.
    x: A numpy array of length 2, representing the coordinates (x, y) of the point.
    """
    x1, x2 = x
    f1 = (x1 - 0)**2 + (x2 - 0)**2
    f2 = (x1 - x3)**2 + (x2 - y3)**2
    f = np.minimum(f1, f2)
    return f


bounds = [[xmin, xmax], [ymin, ymax]]
cmaes = CMAESOptimizer()
woa = WoaOptimizer()


def graph(optimizer):
    
    
    

    for z in range(num_tests):
        # random_individuals[z] = woa.woaOptimizer(bounds,bimodal_objective)
        random_individuals[z] = cmaes.cmaesOptimizer(bounds,bimodal_objective)
        
        
    solutions = np.stack(random_individuals)

    x = solutions[:, 0]
    y = solutions[:, 1]
    plt.scatter(x, y)



    # above = yes
    above_counter = 0

    # below = no
    below_counter = 0
    range_counter = 0

    for point in random_individuals:

        x = point[0]
        y = point[1]

        if y > m * x + b:
            above_counter += 1
        elif y < m * x + b:
            below_counter += 1
        else:
            print("not in range")
            range_counter += 1

    print("above=", above_counter)
    print("below=", below_counter)
    print("not in range =", range_counter)

    # print("p-val?=", abs_num_above / abs_num_below)
    # print("p-val?=", abs_num_below / abs_num_above)
    plt.show()


graph(woa.woaOptimizer(bounds,bimodal_objective))

# graph(cmaes.cmaesOptimizer(bimodal_objective,bounds))
