import os
import sys
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
sys.path.append(parent_dir)


import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import random

from optimizers.cma_es import CMAESOptimizer
from optimizers.woa import WoaOptimizer
from prettytable import PrettyTable
from obj_function import Obj_function

num_tests = 100

xmin, xmax = -10, 10
ymin, ymax = -8, 15
bounds = [[xmin, xmax], [ymin, ymax]]

cmaes = CMAESOptimizer()
woa = WoaOptimizer()
obj_fun = Obj_function(bounds)

random_individuals = np.empty(num_tests, dtype=object)
best_fit = np.empty(num_tests, dtype=object)

below_arr = []
above_arr =[]


def asymmetry_test(optimizer):
    for i in range(num_tests):
        random_individuals[i], best_fit[i] = optimizer(bounds, obj_fun.bimodal_objective)

    for i,(point) in enumerate(random_individuals):
        x = point[0]
        y = point[1]
        expected_y = obj_fun.get_expected_y(x)

        if y > expected_y:
            above_arr.append(best_fit[i])
        elif y < expected_y:
            below_arr.append(best_fit[i])
            

    stat, p = stats.wilcoxon(above_arr[np.random.randint(len(above_arr))], below_arr[np.random.randint(len(below_arr))])

    # print the test statistic and p-value
    print("Test statistic:", stat)
    print("p-value:", p)

asymmetry_test(cmaes.cmaesOptimizer)