import numpy as np
import matplotlib.pyplot as plt
from cma.fitness_functions import ff
from optimizers.cma_es import CMAESOptimizer
from optimizers.woa import WoaOptimizer

iterations = 150
num_tests = 100


random_individuals = np.empty(num_tests, dtype=object)


def dummy_objective_function(x):
    return 0


def bimodal_objective(x):
    """
    Computes the value of a bimodal objective function at point x.
    x: A numpy array of length 2, representing the coordinates (x, y) of the point.
    """
    x1, x2 = x
    f1 = (x1 - 0)**2 + (x2 - 0)**2
    f2 = (x1 - 5)**2 + (x2 + 5)**2
    f = np.minimum(f1, f2)
    return f


xmin, xmax = -5, 25
ymin, ymax = -8, 15

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

    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)
    
    m = (ymax - ymin)/(xmax-xmin)
    print('m = ', m)
    b = (ymax - (m*xmax))
    print('b = ', b)

    x = np.linspace(xmin, xmax)
    y = m * x + b
    plt.plot(x, y, color="green")

    # above = yes
    above_counter = 0

    # below = no
    below_counter = 0

    for point in random_individuals:

        x = point[0]
        y = point[1]

        if y > m * x + b:
            above_counter += 1
        elif y < m * x + b:
            below_counter += 1

    print("above=", above_counter)
    print("below=", below_counter)

    # print("p-val?=", abs_num_above / abs_num_below)
    # print("p-val?=", abs_num_below / abs_num_above)
    plt.show()


graph(woa.woaOptimizer(bounds,bimodal_objective))

# graph(cmaes.cmaesOptimizer(bimodal_objective,bounds))