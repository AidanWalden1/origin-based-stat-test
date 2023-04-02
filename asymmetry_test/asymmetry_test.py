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

from scipy.stats import ranksums, combine_pvalues

num_tests = 500

xmin, xmax = -10, 10
ymin, ymax = -8, 15
bounds = [[xmin, xmax], [ymin, ymax]]

cmaes = CMAESOptimizer()
woa = WoaOptimizer()
obj_fun = Obj_function(bounds)

random_individuals = np.empty(num_tests, dtype=object)
best_fit = np.empty(num_tests, dtype=object)


fig, (abv, bel) = plt.subplots(2, 1)

def asymmetry_test(optimizer):
    
    below_arr = []
    above_arr =[]

    for i in range(num_tests):
        random_individuals[i], best_fit[i] = optimizer(bounds, obj_fun.bimodal_objective)

    for i,(point) in enumerate(random_individuals):
        x = point[0]
        y = point[1]
        expected_y = obj_fun.get_expected_y(x)

        indices = range(len(best_fit[i]))
        log_arr = np.log(best_fit[i])

        # Add labels and title
        abv.set_ylabel('fitness')
        abv.set_title('Plot when optimzer tends to other maxima')

        bel.set_ylabel('fitness')
        bel.set_title('Plot when optimzer tends to 0,0')

        # Display the plot


        if y > expected_y:
            above_arr.append(log_arr)
            abv.plot(indices,log_arr)
        elif y < expected_y:
            below_arr.append(log_arr)
            bel.plot(indices, log_arr)







    _, p_value = ranksums(above_arr, below_arr)
    p_combined = combine_pvalues(p_value, method='fisher')[1]
    # print("Combined p-value:", p_combined)
    return p_combined
        

    # plt.show()

            

    # stat, p = stats.wilcoxon(above_arr[np.random.randint(len(above_arr))], below_arr[np.random.randint(len(below_arr))])

    # # print the test statistic and p-value
    # print("Test statistic:", stat)
    # print("p-value:", p)
for i in range(10):
    print(f"cmaes - {asymmetry_test(cmaes.cmaesOptimizer)}")
    print(f"woa - {asymmetry_test(woa.woaOptimizer)}")
