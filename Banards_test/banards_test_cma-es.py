import os
import sys
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
sys.path.append(parent_dir)

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

from optimizers.cma_es import CMAESOptimizer
from optimizers.woa import WoaOptimizer
from prettytable import PrettyTable
from obj_function import Obj_function

num_tests = 500

xmin, xmax = -10, 10
ymin, ymax = -8, 15
bounds = [[xmin, xmax], [ymin, ymax]]

random_individuals = np.empty(num_tests, dtype=object)

cmaes = CMAESOptimizer()
woa = WoaOptimizer()
obj_fun = Obj_function(bounds)



def banard_test(optimizer):

    for i in range(num_tests):
        random_individuals[i], best_fit = optimizer(bounds, obj_fun.bimodal_objective)
    # above = yes
    above_counter = 0

    # below = no
    below_counter = 0
    range_counter = 0

    above_points = np.empty((0, 2), float)
    below_points = np.empty((0, 2), float)

    for point in random_individuals:
        x = point[0]
        y = point[1]
        expected_y = obj_fun.get_expected_y(x)

        if y > expected_y:
            above_counter = above_counter + 1
            above_points = np.append(above_points, [[x, y]], axis=0)
        elif y < expected_y:
            below_counter = below_counter + 1
            below_points = np.append(below_points, [[x, y]], axis=0)
        else:
            print("not in range")
            range_counter += 1

    solutions = np.stack(random_individuals)
    xpoints = solutions[:, 0]
    ypoints = solutions[:, 1]

    plt.scatter(xpoints, ypoints)

    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)
    plt.plot(obj_fun.x1, obj_fun.y1, color="green")

    a = len(below_points)
    b = num_tests/2
    c = len(above_points)
    d = num_tests/2

    table = PrettyTable()
    table.field_names = ["", "optimizer", "norm"]
    table.add_row(["below", a, b])
    table.add_row(["above", c, d])


    p_val = stats.barnard_exact([[a, b], [c, d]])
    print(table)
    print("p-value= ", p_val.pvalue)



    plt.show()

    return np.array([below_points, above_points], dtype=object)

banard_test(cmaes.cmaesOptimizer)
banard_test(woa.woaOptimizer)


